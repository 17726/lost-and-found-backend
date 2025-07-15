from rest_framework import generics, permissions
from .models import Item
from .serializers import ItemSerializer
from .permissions import IsOwnerOrReadOnly # 我们稍后会创建这个权限类

# 这个视图处理两种请求:
# GET /api/items/ : 获取物品列表
# POST /api/items/ : 发布新物品
class ItemListCreateView(generics.ListCreateAPIView):
    queryset = Item.objects.all().order_by('-created_at') # 默认按创建时间倒序
    serializer_class = ItemSerializer
    # 【重要】设置权限：任何人都可以看(GET)，但只有登录用户才能发(POST)
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def perform_create(self, serializer):
        # 当创建新物品时，自动将当前登录用户设置为发布者
        serializer.save(user=self.request.user)

# 这个视图处理三种请求:
# GET /api/items/<id>/ : 获取单个物品详情
# PATCH /api/items/<id>/ : 修改物品
# DELETE /api/items/<id>/ : 删除物品
class ItemDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Item.objects.all()
    serializer_class = ItemSerializer
    # 【重要】设置权限：任何人都可以看，但只有物品的主人才能修改或删除
    permission_classes = [permissions.IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly]