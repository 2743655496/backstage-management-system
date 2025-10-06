import base64, uuid, os
from django.conf import settings

def save_avatar_file(avatar_data):
    """保存 base64 图片到文件并返回 UUID 文件名"""
    try:
        if not avatar_data or not avatar_data.startswith('data:image'):
            return None

        format, imgstr = avatar_data.split(';base64,')
        ext = format.split('/')[-1]
        filename = f"{uuid.uuid4().hex}.{ext}"
        avatar_dir = os.path.join(settings.MEDIA_ROOT, 'avatars')
        os.makedirs(avatar_dir, exist_ok=True)
        file_path = os.path.join(avatar_dir, filename)

        with open(file_path, 'wb') as f:
            f.write(base64.b64decode(imgstr))

        return filename
    except Exception as e:
        print(f"保存头像失败: {str(e)}")
        return None
