from rest_framework import serializers
from .models import Item
from users.serializers import UserDetailSerializer # 从users app导入用户序列化器

class ItemSerializer(serializers.ModelSerializer):
    # 使用我们之前在users app里定义的UserDetailSerializer
    # 来处理user字段，实现嵌套显示
    user = UserDetailSerializer(read_only=True)
    
    # 【重要】根据API文档，我们需要一个完整的图片URL
    # image_url是只读的，它的值由下面的 get_image_url 方法动态生成
    image_url = serializers.SerializerMethodField()

    class Meta:
        model = Item
        # fields = '__all__' 是一个快捷方式，表示包含所有模型字段
        fields = '__all__'

    def get_image_url(self, obj):
        # 'obj' 是当前的Item实例
        if obj.image:
            # self.context['request'] 可以获取到当前的请求对象
            request = self.context.get('request')
            # request.build_absolute_uri 可以将相对路径拼接成完整的URL
            return request.build_absolute_uri(obj.image.url)
        return None # 如果没有图片，返回null

    def validate(self, data):
        # 实现“位置信息二选一”的后端校验
        location = data.get('location')
        latitude = data.get('latitude')
        
        # 在部分更新(PATCH)时，这些字段可能不存在，所以要用 .get()
        # 并且只有在两者都明确为空时才报错
        if not location and not latitude:
            raise serializers.ValidationError("请至少提供地点描述或在地图上选点。")
        return data