from .serializers import ItemSerializer, ItemCreateSerializer 
from rest_framework import generics, permissions, filters 
import django_filters 
from .models import Item
from .filters import ItemFilter
from .permissions import IsOwnerOrReadOnly

# ListAPIView 专门用于处理“获取对象列表”的 GET 请求
# 【修改】将视图基类从 ListAPIView 更改为 ListCreateAPIView
class ItemListCreateView(generics.ListCreateAPIView):
    """
    【任务 2.1】 获取物品列表 (GET /items/)
        获取所有物品信息列表。
        无需认证即可访问。
    【任务 2.2】 发布新物品 (POST /items/)
    """
    # queryset 属性对 GET 和 POST 都有效，保持不变
    queryset = Item.objects.all().order_by('-created_at') # 默认按创建时间倒序排列

    # 筛选和搜索配置只对 GET 请求有效，保持不变

     # 在这里添加筛选和搜索的配置
    filterset_class = ItemFilter
    # 启用DRF内置的搜索功能和我们配置的django-filter
    filter_backends = [filters.SearchFilter, django_filters.rest_framework.DjangoFilterBackend]
    # 指定可以按哪些字段进行 ?search=... 的模糊搜索
    search_fields = ['title', 'description', 'location']

    def get_serializer_class(self):
        """
        重写此方法，根据请求类型动态选择序列化器。
        """
        # self.request.method 会返回当前请求的HTTP方法名，如 'GET', 'POST'
        if self.request.method == 'POST':
            # 如果是创建操作，使用我们专为“写”设计的 ItemCreateSerializer
            return ItemCreateSerializer
        
        # 对于所有其他情况（主要是GET），使用为“读”设计的 ItemSerializer
        return ItemSerializer

    def get_permissions(self):
        """
        重写此方法，根据请求类型动态设置权限。
        """
        if self.request.method == 'POST':
            # 如果是创建操作，必须是已认证用户。
            # IsAuthenticated 会检查请求头中是否有有效的Token。
            return [permissions.IsAuthenticated()]
        
        # 对于GET请求，允许任何人访问。
        return [permissions.AllowAny()]
class ItemDetailView(generics.RetrieveUpdateDestroyAPIView):
    """
    【任务 2.3】 获取单个物品详情 (GET)
    【任务 2.4】 修改物品信息 (PATCH)
    【任务 2.5】 删除物品 (DELETE)
    """
    # queryset 和 serializer_class 是必须的，DRF会用它们来获取和序列化对象
    queryset = Item.objects.all()
    serializer_class = ItemSerializer
    
    # 将权限类设置为我们自定义的 IsOwnerOrReadOnly
    # 它已经包含了对GET方法的判断，所以我们不再需要 get_permissions 方法了
    permission_classes = [IsOwnerOrReadOnly]
    # 这个视图默认对所有HTTP方法都要求认证。
    # def get_permissions(self):
    #     if self.request.method == 'GET':
    #         return [permissions.AllowAny()]
    #     return [permissions.IsAuthenticated()]