from django.contrib.auth.models import User
from django.db import models

def auth_image_directory_path(instance: "AuthImage", filename: str) -> str:
    return "auth/auth_{id}/avatar/{filename}".format(
        id=instance.user.id,
        filename=filename,
    )

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    bio = models.TextField(max_length=500, blank=True)
    agreement_accepted = models.BooleanField(default=False)
    avatar = models.ImageField(null=True, blank=True, upload_to=auth_image_directory_path)
