from rest_framework import permissions

class IsOwnerOrReadOnly(permissions.BasePermission):
    """
    自定义权限，只允许对象的所有者进行编辑。
    对于安全的HTTP方法（GET, HEAD, OPTIONS），总是允许访问。
    """
    def has_object_permission(self, request, view, obj):
        # 读取权限允许任何请求(GET, HEAD, OPTIONS)
        if request.method in permissions.SAFE_METHODS:
            return True

        # 写入权限只给予该物品的发布者
        # obj 是正在被访问的数据库对象实例（在这里就是Item实例）
        # request.user 是通过Token认证后的当前用户实例
        return obj.user == request.user