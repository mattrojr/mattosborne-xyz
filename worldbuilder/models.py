from django.db import models
from django.contrib.auth.models import User
from mptt.models import MPTTModel, TreeForeignKey
# Create your models here.


class Campaign(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField()
    def __str__(self):
        return self.name


class GameMaster(models.Model):
    user = models.ForeignKey(User,
                             on_delete=models.CASCADE)
    campaign = models.ForeignKey(Campaign,
                                 on_delete=models.CASCADE)
    def __str__(self):
        return self.user.username + ', ' + self.campaign.name


class Area(MPTTModel):
    name = models.CharField(max_length=255)
    description = models.TextField()
    notes = models.TextField()
    code = models.CharField(max_length=32, null=True)
    campaign = models.ForeignKey(Campaign,
                                 on_delete=models.CASCADE)
    unique_together = ("code", "campaign")
    parent = TreeForeignKey('self',
                            on_delete=models.CASCADE,
                            related_name='children',
                            blank=True,
                            null=True,
                            db_index=True)

    class MPTTMeta:
        order_insertion_by = ['code']

    def __str__(self):
        return self.name

