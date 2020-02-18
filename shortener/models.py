from django.db import models


class FullURL(models.Model):
    url = models.URLField(unique=True)
    
    def __str__(self):
        return self.url


class Shortcut(models.Model):
    value = models.CharField(primary_key=True, unique=True, max_length=50)
    full_url = models.ForeignKey(FullURL, on_delete=models.CASCADE, related_name='shortcuts')

    def __str__(self):
        return self.value