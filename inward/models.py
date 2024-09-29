from django.db import models
from users.models import Department

class UploadedFile(models.Model):
    inward_from = models.CharField(max_length=225, null=True, blank=True)
    inward_to = models.ManyToManyField(Department)
    subject = models.CharField(max_length=225)
    content = models.TextField(null=True, blank=True)
    file = models.FileField(upload_to='uploads/')
    created_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now=True)

