from rest_framework import serializers
from .models import Item
from users.serializers import UserDetailSerializer # 导入用户序列化器

class ItemSerializer(serializers.ModelSerializer):
    # 【核心】使用 UserDetailSerializer 序列化 user 字段，实现嵌套对象
    user = UserDetailSerializer(read_only=True)
    
    # 【核心】自定义 image_url 字段，生成完整的图片URL
    image_url = serializers.SerializerMethodField()

    class Meta:
        model = Item
        fields = '__all__' # 序列化所有模型字段

    def get_image_url(self, obj):
        """
        生成图片的完整访问URL。 obj 是当前的 Item 实例。
        """
        request = self.context.get('request')
        if request and obj.image and hasattr(obj.image, 'url'):
            return request.build_absolute_uri(obj.image.url)
        return None # 如果没有图片，返回 null

class ItemCreateSerializer(serializers.ModelSerializer):
    # 这个字段对用户隐藏，它的值会自动设置为当前登录的用户。
    # 这样可以防止恶意用户伪造发布者身份。
    user = serializers.HiddenField(default=serializers.CurrentUserDefault())

    class Meta:
        model = Item
        # 'fields' 列表只包含我们允许前端在创建时提交的字段。
        # 'is_resolved' 和 'created_at' 等字段由后端自动处理，不应由用户提交。
        fields = [
            'user', 'title', 'description', 'type', 'item_class', 
            'location', 'latitude', 'longitude', 'contact', 'time', 'image'
        ]

    def validate(self, data):
        """
        对象级别的自定义验证钩子。
        在基础的字段验证（如 title 是否为空）通过后，DRF会调用此方法。
        """
        location = data.get('location')
        latitude = data.get('latitude')
        longitude = data.get('longitude')

        # 实现API文档中约定的“位置信息二选一”的校验规则。
        if not location and not (latitude is not None and longitude is not None):
            # 如果验证失败，必须抛出 serializers.ValidationError 异常。
            # DRF会捕获这个异常，并生成一个标准的400 Bad Request错误响应。
            raise serializers.ValidatnEiorror("地点描述和地图坐标至少需要提供一项。")
        
        # 如果验证通过，必须返回 data 字典。
        return data