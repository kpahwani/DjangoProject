from django.db import models
from django.utils import timezone
# Create your models here.


class Users(models.Model):
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    email_id = models.EmailField(max_length=50)
    secondary_email_id = models.EmailField(max_length=50,null=True)
    password = models.CharField(max_length=50)
    country = models.CharField(max_length=50)

    def __str__(self):
        return "{} {}".format(self.first_name, self.last_name)


class Logins(models.Model):
    user = models.OneToOneField(Users, on_delete=models.CASCADE,null=True)
    failed_attempts = models.IntegerField(default=0)
    last_login = models.DateTimeField(default=timezone.now())
    ip_address = models.GenericIPAddressField(null=True)
