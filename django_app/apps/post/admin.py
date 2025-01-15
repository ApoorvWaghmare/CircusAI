from django.contrib import admin

#----------#

from .models.mysql_models import Post, GenMediaRef, PromptedMediaRef

#----------#

admin.site.register(Post)
admin.site.register(GenMediaRef)
admin.site.register(PromptedMediaRef)