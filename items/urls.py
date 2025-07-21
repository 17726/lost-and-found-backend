from django.urls import path
from .views import ItemListCreateView 

urlpatterns = [
    # 将 GET /api/items/ 请求路由到 ItemListView
    path('items/', ItemListCreateView.as_view(), name='item-list-create'),
]