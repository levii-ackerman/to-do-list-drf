from django.db import models
from django.contrib.auth import get_user_model
from shared.models import BaseModel

User = get_user_model()

class Group(BaseModel, models.Model):
    name = models.CharField(max_length=30)
    description = models.TextField(null=True, blank=True)
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name='group_admin', null=True, blank=True)

    def __str__(self):
        return f"group name - {self.name}"
    
class GroupMember(BaseModel, models.Model):
    user_id = models.ForeignKey(User, on_delete=models.CASCADE, related_name='gorup_members')
    group_id = models.ForeignKey(Group, on_delete=models.CASCADE)

    def __str__(self):
        return f"group_id - {self.group_id.id}"
    
class GroupTask(BaseModel, models.Model):
    title = models.CharField(max_length=30)
    description = models.TextField(null=True, blank=True)
    deadline = models.DateTimeField(null=True, blank=True)
    is_done = models.BooleanField(default=False)

    group_id = models.ForeignKey(Group, on_delete=models.CASCADE)

    def __str__(self):
        return f"task of group - {self.title} (Group - {self.group_id.name})"
    
class GroupSubTask(BaseModel, models.Model):
    title = models.CharField(max_length=30)
    description = models.TextField(null=True, blank=True)
    is_done = models.BooleanField(default=False)
    deadline = models.DateTimeField(null=True, blank=True)

    gr_task = models.ForeignKey(GroupTask, on_delete=models.CASCADE, related_name='subtasks')
    member_id = models.ForeignKey(GroupMember, on_delete=models.CASCADE)

    def __str__(self):
        return f"Subtask - {self.title} -> {self.member_id.user_id.username} ({self.member_id.group_id.name})"
