from django.contrib import admin

#----------#

from .models.mysql_models import User, UserFollowing, UserBlock

#----------#

admin.site.register(User)
admin.site.register(UserFollowing)
admin.site.register(UserBlock)
