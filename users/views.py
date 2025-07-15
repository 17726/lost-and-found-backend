from rest_framework import generics, permissions, status
from rest_framework.response import Response
from rest_framework.authtoken.models import Token
from rest_framework.authtoken.views import ObtainAuthToken
from .serializers import UserRegisterSerializer, UserDetailSerializer

# 注册视图
# generics.CreateAPIView 提供了一个只处理POST请求（创建）的基类
class UserRegisterView(generics.CreateAPIView):
    serializer_class = UserRegisterSerializer
    permission_classes = [permissions.AllowAny]

    # 【核心修改】重写整个 create 方法
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        
        # self.perform_create(serializer) 会调用 serializer.save()
        # serializer.save() 会调用 serializer.create()，用户在这里被创建
        self.perform_create(serializer)
        
        # 创建成功后，新创建的用户实例存储在 serializer.instance 中
        user_instance = serializer.instance
        
        # 使用 UserDetailSerializer 来生成我们想要的、包含id的响应
        user_response_data = UserDetailSerializer(user_instance).data
        
        # 构建最终的成功响应
        return Response({
            "message": "注册成功！",
            "user": user_response_data
        }, status=status.HTTP_201_CREATED) # 返回正确的 201 状态码

# 登录视图
# 我们继承DRF自带的ObtainAuthToken视图，但重写它的post方法
# 以便返回我们API文档中约定的、更丰富的用户信息
class UserLoginView(ObtainAuthToken):
    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data, context={'request': request})
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        # 使用 get_or_create 来获取或创建Token
        token, created = Token.objects.get_or_create(user=user)
        
        # 返回自定义的响应体
        return Response({
            'token': token.key,
            'user': UserDetailSerializer(user).data
        })