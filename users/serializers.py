from rest_framework import serializers
from .models import User

# 这个序列化器专门用于“注册”
# 它会接收'username'和'password'，并进行基本的验证
class UserRegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, required=True, style={'input_type': 'password'})

    class Meta:
        model = User
        # 我们只关心这三个字段的传入
        fields = ('username', 'password', 'email')

    def create(self, validated_data):
        # 这是创建用户的核心逻辑
        # 我们使用Django内置的create_user方法，它会自动处理密码哈希
        user = User.objects.create_user(
            username=validated_data['username'],
            password=validated_data['password'],
            email=validated_data.get('email', '') # email是可选的
        )
        return user

# 这个序列化器用于在各种API响应中，安全地展示用户信息
# 它只包含我们想暴露给外界的字段
class UserDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'username', 'email') # 只返回id, username, email