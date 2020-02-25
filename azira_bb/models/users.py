from django.db import models
from django.contrib.auth.models import User

from .utils import TimeStamp
from .organizations import Organizations
from .designations import Designations


class Users(models.Model, TimeStamp):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=30)
    hobbies = models.CharField(max_length=100)
    city = models.CharField(max_length=50, blank=True, null=True)
    organization = models.ForeignKey(Organizations, on_delete=models.CASCADE, blank=True, null=True)
    designation = models.ForeignKey(Designations, on_delete=models.CASCADE)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['email']

    def __str__(self):
        return self.user.get_full_name() if self.user.get_full_name() else f"{self.id}: name_not_set"

    class META:
        verbose_name = "Az_User"
        verbose_name_plural = "Az_Users"
