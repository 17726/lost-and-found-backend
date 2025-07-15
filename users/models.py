from django.contrib.auth.models import AbstractUser
from django.db import models

# 我们继承Django的AbstractUser，它已经包含了username, password, email等所有基础字段。
class User(AbstractUser):
    """
    自定义用户模型。
    通过重新定义groups和user_permissions字段并提供自定义的related_name，
    解决了与Django原生auth.User模型可能产生的反向访问器冲突。
    这是在项目中启用自定义用户模型的最佳实践。
    """
    
    # 为 'groups' 字段添加一个不会冲突的 related_name
    groups = models.ManyToManyField(
        'auth.Group',
        verbose_name='groups',
        blank=True,
        help_text='The groups this user belongs to.',
        related_name="custom_user_set",  # 核心修改：起一个不会冲突的新名字
        related_query_name="user",
    )
    
    # 为 'user_permissions' 字段也添加一个不会冲突的 related_name
    user_permissions = models.ManyToManyField(
        'auth.Permission',
        verbose_name='user permissions',
        blank=True,
        help_text='Specific permissions for this user.',
        related_name="custom_user_permissions_set", # 核心修改：起一个不会冲突的新名字
        related_query_name="user",
    )

    # 重写__str__方法，让它在后台或调试时显示用户名，更友好
    def __str__(self):
        return self.username
