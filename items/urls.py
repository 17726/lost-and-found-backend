from django.urls import path
from .views import ItemListCreateView ,ItemDetailView

urlpatterns = [
    # 将 GET /api/items/ 请求路由到 ItemListView
    path('items/', ItemListCreateView.as_view(), name='item-list-create'),
    # 新增的路径，处理 /api/items/<id>/
    # <int:pk> 是一个路径转换器，它会：
    # 1. 匹配路径中一个或多个数字。
    # 2. 将匹配到的数字转换成一个整数。
    # 3. 将这个整数以关键字参数 'pk' (Primary Key) 的形式传递给视图。
    path('items/<int:pk>/', ItemDetailView.as_view(), name='item-detail'),
]