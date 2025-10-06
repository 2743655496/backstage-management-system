from rest_framework import serializers
from user_permission.models import User, Permission


class PermissionSerializer(serializers.ModelSerializer):
    creator = serializers.SerializerMethodField()

    class Meta:
        model = Permission
        fields = [
            'id',
            'name',
            'code',
            'description',
            'type',
            'menu_id',
            'parent_id',
            'api_method',
            'api_path',
            'status',
            'creator_id',
            'creator',
            'create_time',
            'update_time',
        ]

    def get_creator(self, obj):
        try:
            user = User.objects.get(id=obj.creator_id)
            return {
                "id": user.id,
                "username": user.username,
                "real_name": user.real_name,
            }
        except User.DoesNotExist:
            return None