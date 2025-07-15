from django.db import models

# Create your models here.
from django.db import models
from users.models import User  # 从我们的 users app 导入刚刚定义的 User 模型

class Item(models.Model):
    """
    物品模型，用于存储失物和拾物信息。
    """

    # --- 基础信息 ---
    title = models.CharField(max_length=50, verbose_name="物品标题")
    description = models.TextField(blank=True, null=True, verbose_name="详细描述")

    # --- 分类信息 ---
    # 定义一个元组列表作为选项，提高代码可读性和可维护性
    ITEM_TYPE_CHOICES = [
        ('LOST', '失物'),
        ('FOUND', '拾物'),
    ]
    type = models.CharField(max_length=10, choices=ITEM_TYPE_CHOICES, verbose_name="信息类型")

    ITEM_CLASS_CHOICES = [
        ('电子产品', '电子产品'),
        ('证件卡片', '证件卡片'),
        ('学习用品', '学习用品'),
        ('生活用品', '生活用品'),
        ('其他', '其他'),
    ]
    item_class = models.CharField(
        max_length=20, 
        choices=ITEM_CLASS_CHOICES, 
        default='其他', 
        verbose_name="物品类别"
    )

    # --- 位置信息 (文本和坐标都是可选的) ---
    location = models.CharField(max_length=100, blank=True, null=True, verbose_name="地点描述")
    latitude = models.DecimalField(max_digits=9, decimal_places=6, null=True, blank=True, verbose_name="纬度")
    longitude = models.DecimalField(max_digits=10, decimal_places=6, null=True, blank=True, verbose_name="经度")

    # --- 联系与状态 ---
    contact = models.EmailField(verbose_name="联系邮箱")
    is_resolved = models.BooleanField(default=False, verbose_name="是否已处理")
    time = models.DateField(null=True, blank=True, verbose_name="事件日期")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="发布时间")

    # --- 关联信息 ---
    # 图片上传后会保存在 'media/item_images/' 目录下
    image = models.ImageField(upload_to='item_images/', null=True, blank=True, verbose_name="物品图片")
    
    # 外键关联到 User 模型，一个用户可以发布多个物品
    # on_delete=models.CASCADE 表示如果用户被删除，他发布的物品也一并删除
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='items', verbose_name="发布者")

    # 在Django后台显示时，用标题作为对象的表示
    def __str__(self):
        return self.title