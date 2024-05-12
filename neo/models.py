from django.db import models

'''
用户表
@ username: 用户名
@ password: 密码
@ email: 邮箱
@ permission: 权限，0为普通用户，1为养殖户，2为管理员
'''
class User(models.Model):
    username = models.CharField(max_length=20)
    password = models.CharField(max_length=20)
    email = models.EmailField()
    permission = models.IntegerField(default=0)