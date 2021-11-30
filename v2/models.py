from django.db import models

class cropModel(models.Model):
    primaryKey = models.BigAutoField(verbose_name='pk', db_column='pk', primary_key=True)
    name = models.CharField(max_length=30, default='작물', null=False, unique=False, blank=True)
    info = models.TextField(default='', null=False, blank=True)
    image = models.ImageField(default='v2/default_Crop.png')


class currCrop(models.Model):
    crop = models.ForeignKey('cropModel', on_delete=models.CASCADE, null=False, blank=True)
