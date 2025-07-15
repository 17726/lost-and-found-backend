from django.urls import path
from .views import ItemListView

urlpatterns = [
    # 将 GET /api/items/ 请求路由到 ItemListView
    path('items/', ItemListView.as_view(), name='item-list'),
]