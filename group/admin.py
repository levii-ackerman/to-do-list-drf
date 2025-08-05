from django.contrib import admin
from .models import Group, GroupMember, GroupSubTask, GroupTask

@admin.register(Group)
class GroupAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'owner']

@admin.register(GroupMember)
class GroupMemberAdmin(admin.ModelAdmin):
    list_display = ['id', 'user_id', 'group_id']

@admin.register(GroupTask)
class GroupTaskAdmin(admin.ModelAdmin):
    list_display = ['id', 'title', 'is_done', 'group_id']

@admin.register(GroupSubTask)
class GroupSubTaskAdmin(admin.ModelAdmin):
    list_display = ['id', 'title', 'is_done', 'gr_task', 'member_id']