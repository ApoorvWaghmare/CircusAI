from django.contrib import admin

#----------#

from .models.mysql_models import Comment

#----------#

admin.site.register(Comment)