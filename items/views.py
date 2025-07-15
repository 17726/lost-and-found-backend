from rest_framework import generics, permissions
from .models import Item
from .serializers import ItemSerializer

# ListAPIView 专门用于处理“获取对象列表”的 GET 请求
class ItemListView(generics.ListAPIView):
    """
    获取所有物品信息列表。
    无需认证即可访问。
    """
    queryset = Item.objects.all().order_by('-created_at') # 默认按创建时间倒序排列
    serializer_class = ItemSerializer
    permission_classes = [permissions.AllowAny] # 允许任何人访问