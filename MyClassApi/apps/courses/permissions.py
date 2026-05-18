from rest_framework import permissions

class IsTeacherOrReadOnly(permissions.BasePermission):
    """
    自定义权限：只有课程教师或管理员可以修改/删除课程，其他用户只能查看。
    """
    def has_permission(self, request, view):
        # 列表/详情展示：所有用户均可访问
        if view.action in ['list', 'retrieve']:
            return True
        # 其他操作（创建、更新、删除）需要登录
        return request.user and request.user.is_authenticated

    def has_object_permission(self, request, view, obj):
        # 读取权限始终允许
        if view.action in ['retrieve']:
            return True
        # 写入权限：只有该课程的教师或管理员可以修改/删除
        return obj.teacher == request.user or request.user.is_staff
