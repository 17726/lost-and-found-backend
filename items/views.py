from rest_framework import generics, permissions
from .models import Item
from .serializers import ItemSerializer
from rest_framework import generics, permissions, filters 
import django_filters 
from .filters import ItemFilter

# ListAPIView 专门用于处理“获取对象列表”的 GET 请求
class ItemListView(generics.ListAPIView):
    """
    获取所有物品信息列表。
    无需认证即可访问。
    """
    queryset = Item.objects.all().order_by('-created_at') # 默认按创建时间倒序排列
    serializer_class = ItemSerializer
    permission_classes = [permissions.AllowAny] # 允许任何人访问

     # --- 【核心修改】在这里添加筛选和搜索的配置 ---
    filterset_class = ItemFilter
    
    # 启用DRF内置的搜索功能和我们配置的django-filter
    filter_backends = [filters.SearchFilter, django_filters.rest_framework.DjangoFilterBackend]
    
    # 指定可以按哪些字段进行 ?search=... 的模糊搜索
    search_fields = ['title', 'description', 'location']