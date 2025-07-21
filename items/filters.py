import django_filters
from .models import Item

class ItemFilter(django_filters.FilterSet):
    # 【核心】自定义地理位置筛选逻辑
    # 我们定义了三个参数：lat, lon, radius，并将筛选逻辑绑定到 'lat' 字段上
    lat = django_filters.NumberFilter(method='filter_by_distance', label="Latitude")
    lon = django_filters.NumberFilter(method='filter_by_distance', label="Longitude")
    radius = django_filters.NumberFilter(method='filter_by_distance', label="Radius (in degrees)")

    class Meta:
        model = Item
        # 定义其他字段的默认筛选行为
        fields = {
            'type': ['exact'],         # 精确匹配, 如 ?type=LOST
            'item_class': ['exact'],  # ?item_class=电子产品
            'is_resolved': ['exact'], # ?is_resolved=false
        }

    def filter_by_distance(self, queryset, name, value):
        """
        根据经纬度和半径（近似）筛选物品。
        这是一个简化的矩形范围筛选，性能较高。
        """
        # 从查询参数中获取所有需要的值
        lat = self.data.get('lat')
        lon = self.data.get('lon')
        radius = self.data.get('radius') # API文档约定，这三个参数总是一起提供

        # 只有当三个参数都存在且有效时，才进行筛选
        if lat and lon and radius:
            try:
                lat_f = float(lat)
                lon_f = float(lon)
                radius_f = float(radius)

                # 计算经纬度的边界
                lat_min = lat_f - radius_f
                lat_max = lat_f + radius_f
                lon_min = lon_f - radius_f
                lon_max = lon_f + radius_f

                # 应用筛选条件
                return queryset.filter(
                    latitude__gte=lat_min,
                    latitude__lte=lat_max,
                    longitude__gte=lon_min,
                    longitude__lte=lon_max
                )
            except (ValueError, TypeError):
                # 如果参数无法转换为浮点数，则不进行筛选
                return queryset
        
        # 如果参数不完整，不进行筛选
        return queryset