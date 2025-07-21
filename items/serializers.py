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