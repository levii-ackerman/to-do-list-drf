from django.db import models
from django.contrib.auth import get_user_model
from shared.models import BaseModel

User = get_user_model()

LOW, MEDIUM, HIGH = "low", "medium", "high"

class Tag(models.Model):
    name = models.CharField(max_length=30, unique=True)

    def __str__(self):
        return f"tag-name -> {self.name}"
    
class Task(models.Model):
    TASK_LEVEL = (
        (LOW, LOW),
        (MEDIUM, MEDIUM),
        (HIGH, HIGH)
    )
    title = models.CharField(max_length=30, null=False, blank=False)
    description = models.TextField()
    deadline = models.DateTimeField(null=False, blank=False)
    is_done = models.BooleanField(default=False)
    tag = models.ForeignKey(Tag, on_delete=models.SET_NULL, null=True, blank=True)
    task_level = models.CharField(max_length=10, choices=TASK_LEVEL, default=LOW)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_time = models.DateTimeField(auto_now=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='tasks')

    def __str__(self):
        return f"task_name - {self.title}"