from rest_framework import status
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.views import TokenRefreshView
from django_redis import get_redis_connection

from apps.users.serializers import (
    LoginSerializer,
    RegisterSerializer,
    UserInfoSerializer,
)

class CustomTokenRefreshView(TokenRefreshView):
    """自定义 TokenRefreshView，返回完整数据结构"""

    def post(self, request, *args, **kwargs):
        old_refresh=request.data.get("refresh")
        conn=get_redis_connection("default")
        from rest_framework_simplejwt.tokens import RefreshToken
        old_token=RefreshToken(old_refresh)
        if not conn.exists(f"refresh_token:{old_token['jti']}"):
            return Response(
                {"code": 401, "msg": "refresh token 已过期"},
                status=status.HTTP_401_UNAUTHORIZED,
            )
        response = super().post(request, *args, **kwargs)
        # 删除旧的
        conn.delete(f"refresh_token:{old_token['jti']}")
        new_refresh=response.data.get("refresh")
        if new_refresh:
            new_token=RefreshToken(new_refresh)
            conn.set(f"refresh_token:{new_token['jti']}", old_token["user_id"], ex=3600*24*7)
        return Response(
            {
                "code": 200,
                "msg": "刷新成功",
                "data": {
                    "access": response.data.get("access"),
                    "refresh": response.data.get("refresh"),
                }
            }
        )


class RegisterView(APIView):
    """用户注册
    POST /api/v1/auth/register/
    Body: {username, password, email, mobile}
    Return: {code, msg, data: {user, access, refresh}}
    """

    permission_classes = [AllowAny]

    def post(self, request):
        serializer = RegisterSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(
                {"code": 400, "msg": "参数错误", "errors": serializer.errors},
                status=status.HTTP_400_BAD_REQUEST,
            )

        user = serializer.save()

        # 生成 JWT token
        refresh = RefreshToken.for_user(user)
        access = str(refresh.access_token)

        # 处理 refresh token 的存储（Redis 白名单）
        store_refresh_token(refresh,user)

        return Response(
            {
                "code": 200,
                "msg": "注册成功",
                "data": {
                    "user": UserInfoSerializer(user).data,
                    "access": access,
                    "refresh": str(refresh),
                },
            },
            status=status.HTTP_201_CREATED,
        )


class LoginView(APIView):
    """用户登录

    POST /api/v1/auth/login/
    Body: {username, password}
    Return: {code, msg, data: {user, access, refresh}}
    """

    permission_classes = [AllowAny]


    def post(self, request):
        serializer = LoginSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(
                {"code": 400, "msg": "参数错误", "errors": serializer.errors},
                status=status.HTTP_400_BAD_REQUEST,
            )
        user = serializer.validated_data["user"]

        # 生成 JWT token
        refresh = RefreshToken.for_user(user)
        access = str(refresh.access_token)

        # 处理 refresh token 的存储策略（Redis 白名单 或 客户端存储）
        store_refresh_token(refresh,user)

        return Response(
            {
                "code": 200,
                "msg": "登录成功",
                "data": {
                    "user": UserInfoSerializer(user).data,
                    "access": access,
                    "refresh": str(refresh),
                },
            },
        )

def store_refresh_token(refresh, user):
  conn = get_redis_connection("default")
  conn.set(f"refresh_token:{refresh['jti']}", user.id, ex=3600*24*7)