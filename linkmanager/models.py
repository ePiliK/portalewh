from django.db import models
from django.contrib.auth.models import User

class Client(models.Model):
    name = models.CharField(max_length=255)
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True, blank=True)

    def __str__(self):
        return self.name

class Link(models.Model):
    client = models.ForeignKey(Client, on_delete=models.CASCADE)
    site_link = models.URLField()
    article_link = models.URLField()
    cost = models.DecimalField(max_digits=10, decimal_places=2)
    za = models.CharField(max_length=50)
    da = models.CharField(max_length=50)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.client.name} - {self.site_link}"