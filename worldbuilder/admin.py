from django.contrib import admin
from worldbuilder.models import *
# Register your models here.

models_list = [
    Campaign,
    Area,
    GameMaster,
]
admin.site.register(models_list)
