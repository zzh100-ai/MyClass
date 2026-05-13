from rest_framework import serializers
from apps.users.models import User
from utils import constant
import re
from django_redis import get_redis_connection


class RegisterSerializer(serializers.ModelSerializer):
    """注册序列化器"""

    password2 = serializers.CharField(write_only=True, label="确认密码")
    password = serializers.CharField(write_only=True, label="密码")

    # 添加手机号格式验证（正则匹配中国大陆手机号 1[3-9]\d{9}）
    def validate_mobile(self, value):
        if not constant.MOBILE_RE.match(value):
            raise serializers.ValidationError("手机号格式错误")
        return value

    # 添加密码强度验证（至少8位，包含字母和数字）
    def validate_password(self, value):
        if len(value) < 8:
            raise serializers.ValidationError("密码长度不能小于8位")
        # 必须同时包含字母和数字
        if not re.search(r'[A-Za-z]', value):
            raise serializers.ValidationError("密码必须包含字母")
        if not re.search(r'\d', value):
            raise serializers.ValidationError("密码必须数字")
        return value

    # 添加确认密码字段（password2），比较 password == password2
    def validate_password2(self, value):
        if self.initial_data.get("password") != value:
            raise serializers.ValidationError("两次输入的密码不一致")
        return value

    def create(self, validated_data):
        """创建用户，密码使用 set_password 加密"""
        password = validated_data.pop("password")
        # 删除password2
        validated_data.pop("password2")
        user = User(**validated_data)
        user.set_password(password)
        user.save()
        return user

    class Meta:
        model = User
        fields = ["id", "username", "password2", "password", "email", "mobile"]
        extra_kwargs = {
            "email": {"required": True},
        }


class LoginSerializer(serializers.Serializer):
    """登录序列化器"""

    # 添加手机号+密码登录支持（不仅限 username）
    def validate(self, attrs):
        identifier = attrs.get("identifier")
        password = attrs.get("password")
        if not identifier or not password:
            raise serializers.ValidationError("用户名或密码不能为空")
        conn = get_redis_connection("default")
        fail_key = f'login_fail:{identifier}'
        fail_count = int(conn.get(fail_key) or 0)

        # 达到上限，直接拦截
        if fail_count >= 5:
            ttl = conn.ttl(fail_key)
            raise serializers.ValidationError(f"登录失败次数过多，请{ttl // 60}分钟后再试")
        # 认证
        from django.db.models import Q

        user = User.objects.filter(Q(username=identifier) | Q(mobile=identifier) | Q(email=identifier)).first()
        if not user or not user.check_password(password):
            # 失败，计数+1
            new_count = conn.incr(fail_key)
            if new_count == 1:
                conn.expire(fail_key, 3600)
            remaining = 5 - new_count
            if remaining > 0:
                msg = f"用户名或密码错误，剩余{remaining}次尝试"
            else:
                msg = "登录失败次数过多，已锁定15分钟"
            raise serializers.ValidationError(msg)

        # 登录成功，清除计数
        conn.delete(fail_key)
        attrs["user"] = user
        attrs["username"] = user.username
        attrs["password"] = password
        return attrs

    identifier = serializers.CharField(label="用户名/电话/邮箱")
    password = serializers.CharField(write_only=True, label="密码")


class UserInfoSerializer(serializers.ModelSerializer):
    """用户信息（用于返回登录/注册成功后的用户数据）"""

    class Meta:
        model = User
        fields = ["id", "username", "email", "mobile", "date_joined"]
