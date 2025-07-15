from rest_framework import serializers
from .models import Item
from users.serializers import UserDetailSerializer # 导入我们之前创建的用户序列化器

class ItemSerializer(serializers.ModelSerializer):
    # 【核心】嵌套序列化器：用 UserDetailSerializer 来序列化 user 字段
    # read_only=True 表示这个字段在反序列化（创建/更新）时是只读的
    user = UserDetailSerializer(read_only=True)
    
    # 【核心】自定义字段：根据模型的 image 字段生成完整的 URL
    # SerializerMethodField 允许我们自定义字段的输出
    image_url = serializers.SerializerMethodField()

    class Meta:
        model = Item
        # fields = '__all__' 表示序列化所有模型字段
        fields = '__all__' 
        # depth = 1 # 这是一个快捷但不灵活的嵌套方式，我们用嵌套序列化器代替

    def get_image_url(self, obj):
        """
        生成图片的完整访问URL。
        obj 是当前的 Item 实例。
        """
        request = self.context.get('request')
        if request and obj.image and hasattr(obj.image, 'url'):
            # request.build_absolute_uri 会将相对URL（如 /media/item_images/foo.jpg）
            # 转换为完整的URL（如 http://127.0.0.1:8000/media/item_images/foo.jpg）
            return request.build_absolute_uri(obj.image.url)
        return None # 如果没有图片，返回 null