import logging
import uuid
import jwt
import json
from rest_framework import viewsets
from .models import Department, Role, User,UserRole, RolePermission, Permission, Menu
from .serializers import DepartmentSerializer, RoleSerializer, UserSerializer, PermissionSerializer, UserLoginSerializer
from .utils.jwt_utils import JWTUtils
from django.utils import timezone
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.conf import settings
from utils.redis_client import RedisClient


# 获取审计日志 logger
audit_logger = logging.getLogger('audit')
class DepartmentViewSet(viewsets.ModelViewSet):
    queryset = Department.objects.all()
    serializer_class = DepartmentSerializer


class RoleViewSet(viewsets.ModelViewSet):
    queryset = Role.objects.all()
    serializer_class = RoleSerializer


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer


class PermissionViewSet(viewsets.ModelViewSet):
    queryset = Permission.objects.all()
    serializer_class = PermissionSerializer


class SliderVerifyView(APIView):
    def post(self, request):
        trail = request.data.get('trail', [])
        if not trail or not isinstance(trail, list):
            return Response({'error': '轨迹数据无效'}, status=400)

        if not self._is_human_like(trail):
            return Response({'error': '滑动行为异常'}, status=403)

        # 验证通过，生成一次性 token
        token = str(uuid.uuid4())
        RedisClient.set(f"slider_token:{token}", "1", ex=300)  # 5分钟有效

        return Response({'success': True, 'token': token}, status=200)

    def _is_human_like(self, trail):
        if len(trail) < 6:
            return False

        duration = trail[-1]['time'] - trail[0]['time']
        jitter_count = sum(
            1 for i in range(1, len(trail))
            if abs(trail[i]['x'] - trail[i - 1]['x']) > 2
        )
        jitter_ratio = jitter_count / len(trail)

        return duration >= 250 or jitter_ratio >= 0.3
class LoginView(APIView):
    def post(self, request):
        slider_token = request.data.get('slider_token')
        if not slider_token or not RedisClient.get(f"slider_token:{slider_token}"):
            return Response({'error': '滑块验证未通过'}, status=403)

        # 验证通过后删除 token，防止复用
        RedisClient.delete(f"slider_token:{slider_token}")

        ip = self.get_client_ip(request)
        serializer = UserLoginSerializer(data=request.data, context={'ip': ip})
        remember = request.data.get('remember')
        if serializer.is_valid():
            user = serializer.validated_data['user']

            # 更新最后登录信息
            user.last_login_time = timezone.now()
            user.last_login_ip = self.get_client_ip(request)
            user.save(update_fields=['last_login_time', 'last_login_ip'])

            # 生成 token
            access_token = JWTUtils.create_access_token(user)
            if remember:
                refresh_token = JWTUtils.create_refresh_token(user, 7)
            else:
                refresh_token = JWTUtils.create_refresh_token(user, 1)

            # 审计日志 - 登录成功
            audit_logger.info({
                "event": "login_success",
                "username": user.username,
                "ip": user.last_login_ip,
                "ua": request.META.get('HTTP_USER_AGENT'),
                "time": timezone.now().strftime("%Y-%m-%d %H:%M:%S")
            })

            # 构造响应
            response = Response({
                'user': {
                    'id': user.id,
                    'username': user.username,
                    'avatar': user.avatar,
                    'email': user.email,
                }
            })
            # 设置 HttpOnly Cookie
            response.set_cookie(
                key='access_token',
                value=access_token,
                httponly=True,
                secure=not settings.DEBUG,  # 生产环境启用 HTTPS
                # samesite='Lax',
                samesite='Strict',
                # samesite='None',
                max_age=3600  # 1小时有效期
            )
            response.set_cookie(
                key='refresh_token',
                value=refresh_token,
                httponly=True,
                secure=not settings.DEBUG,
                # samesite='Lax',
                samesite='Strict',
                # samesite='None',
                max_age=7 * 24 * 3600 if remember else 24 * 3600
            )

            return response
        # 审计日志 - 登录失败
        audit_logger.info({
            "event": "login_failed",
            "username": request.data.get('username'),
            "ip": self.get_client_ip(request),
            "ua": request.META.get('HTTP_USER_AGENT'),
            "errors": serializer.errors,
            "time": timezone.now().strftime("%Y-%m-%d %H:%M:%S")
        })
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def get_client_ip(self, request):
        x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
        if x_forwarded_for:
            ip = x_forwarded_for.split(',')[0].strip()
        else:
            ip = request.META.get('REMOTE_ADDR').strip()
        return ip


class AuthStatusView(APIView):
    def get(self, request):
        user = getattr(request, 'my_user', None)
        if user:
            return Response({
                'is_authenticated': True,
                'user': {
                    'id': user.id,
                    'username': user.username,
                    'avatar': user.avatar,
                    'email': user.email,
                }
            })
        else:
            return Response({
                'is_authenticated': False,
                'error': '未登录或令牌无效'
            }, status=status.HTTP_401_UNAUTHORIZED)


class TokenRefreshView(APIView):
    def post(self, request):
        refresh_token = request.COOKIES.get('refresh_token')
        if not refresh_token:
            return Response({'code':401,'error': '缺少 Refresh Token'})
        try:
            payload = JWTUtils.verify_token(refresh_token)
            user = User.objects.get(id=payload['user_id'], is_deleted=0, status=1)
        except Exception:
            return Response({'code':401,'error': 'Refresh Token 无效或已过期'})

        new_access_token = JWTUtils.create_access_token(user)
        response = Response({'code':200,'message': 'Token 已刷新'})
        response.set_cookie('access_token', new_access_token, httponly=True, secure=not settings.DEBUG, samesite='Strict', max_age=3600)
        return response



class UserProfileView(APIView):
    def get(self, request):
        # 用户信息可以从 request.user 获取（通过认证中间件）
        user = request.my_user
        return Response({
            'id': user.id,
            'username': user.username,
            'avatar': user.avatar,
            'email': user.email,
        })


class LogoutView(APIView):
    def post(self, request):
        refresh_token = request.COOKIES.get('refresh_token')

        if refresh_token:
            try:
                payload = JWTUtils.verify_token(refresh_token)
                exp_timestamp = payload['exp']
                current_timestamp = int(timezone.now().timestamp())
                ttl = exp_timestamp - current_timestamp
                if ttl > 0:
                    RedisClient.add_to_blacklist(refresh_token, ttl)
            except jwt.ExpiredSignatureError:
                pass  # 已过期，无需拉黑
            except Exception:
                pass  # 非法 token，忽略处理

        response = Response({'message': '已退出登录'})

        # 清除 Cookie
        response.delete_cookie('access_token')
        response.delete_cookie('refresh_token')

        return response


from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from .models import UserRole, RolePermission, Permission, Menu
from utils.redis_client import RedisClient
import json

class UserPermissionView(APIView):

    def get(self, request):
        user_id = request.my_user.id
        cache_key = f"user:permissions:tree:{user_id}"

        # 尝试从 Redis 获取缓存
        cached = RedisClient.get(cache_key)
        if cached:
            return Response(json.loads(cached))

        # 获取用户角色
        role_ids = UserRole.objects.filter(user_id=user_id).values_list('role_id', flat=True)

        # 获取角色权限
        permission_ids = RolePermission.objects.filter(role_id__in=role_ids).values_list('permission_id', flat=True)

        # 获取所有权限
        permissions = Permission.objects.filter(
            id__in=permission_ids,
            status=1,
            is_deleted=0
        )

        # 菜单权限（type=1）
        menu_ids = permissions.filter(type=1).values_list('menu_id', flat=True)
        menus = Menu.objects.filter(id__in=menu_ids, status=1, is_deleted=0).order_by('sort')
        menus_list = []
        # 构建菜单树
        def build_tree(menu_list, parent_id=0):
            tree = []
            for menu in menu_list:
                if menu.parent_id == parent_id:
                    item = {
                        'id': menu.id,
                        'name': menu.name,
                        'path': menu.path,
                        'component': menu.component,
                        'icon': menu.icon,
                        'children': build_tree(menu_list, menu.id)
                    }
                    tree.append(item)
                    if parent_id != 0:
                        menus_list.append({
                        'id': menu.id,
                        'name': menu.name,
                        'path': menu.path,
                        'component': menu.component,
                    })
            return tree

        menu_permissions = build_tree(list(menus))

        # 接口权限（type=2），按菜单 path 分组
        permission_map = {}
        for perm in permissions.filter(type=2):
            menu = Menu.objects.filter(id=perm.menu_id, is_deleted=0).first()
            if not menu or not menu.path:
                continue
            path = menu.path
            if path not in permission_map:
                permission_map[path] = []
            permission_map[path].append({
                'id': perm.id,
                'name': perm.name,
                'code': perm.code,
                'method': perm.api_method,
                'path': perm.api_path
            })

        result = {
            "menus_list":menus_list,
            'menu_permissions': menu_permissions,
            'permission_map': permission_map
        }

        # 缓存结果（5分钟）
        RedisClient.set(cache_key, json.dumps(result), ex=300)

        return Response(result)

