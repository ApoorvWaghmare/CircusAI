from django.db import models
from django.contrib.auth.models import AbstractUser, UserManager as DefaultUserManager
from django.db.models import CharField, EmailField, DateField, FloatField, ForeignKey, DateTimeField
from django.utils.dateparse import parse_date
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.models import User


#======================================================================================================================#
# UserManager
#======================================================================================================================#

# Extend the default UserManager
class UserManager(DefaultUserManager):
    
    #------------------------------------------------------------------------------------------------------------------#

    def create_user(self):
        pass

#======================================================================================================================#
# End of UserManager
#======================================================================================================================#

#======================================================================================================================#
# User
#======================================================================================================================#

class User(AbstractUser):
    
    #------------------------------------------------------------------------------------------------------------------#

    class Meta:
        db_table = 'user'

    #------------------------------------------------------------------------------------------------------------------#
     
    class Gender(models.TextChoices):
        MALE = 'M', _('Male')
        FEMALE = 'F', _('Female')
        OTHER = 'O', _('Other')
        NOT_SPECIFIED = 'N', _('Not Specified')

    #------------------------------------------------------------------------------------------------------------------#

    objects = UserManager()

    #------------------------------------------------------------------------------------------------------------------#

    first_name = CharField(max_length = 255)
    last_name = CharField(max_length = 255)
    email = EmailField(max_length = 255, unique = True, null = False)
    birth_date = DateField(null = True)
    username = CharField(max_length = 255, unique = True, null = False)
    gender = CharField(max_length = 1, choices = Gender.choices, default = Gender.NOT_SPECIFIED.value)
    latitude = FloatField(null = True)
    longitude = FloatField(null = True)
    profile_pic_ref = CharField(max_length = 255, null = True, unique = True)
    bio_ref = CharField(max_length = 255, null = True, unique = True)
    is_active = models.BooleanField(default = False)

    USERNAME_FIELD = 'username'
    EMAIL_FIELD = 'email'

#======================================================================================================================#
# End of User
#======================================================================================================================#

#======================================================================================================================#
# UserFollowingManager
#======================================================================================================================#

class UserFollowingManager(models.Manager):
    
    #------------------------------------------------------------------------------------------------------------------#

    def create_user_following(self):
        pass

#======================================================================================================================#
# End of UserFollowingManager
#======================================================================================================================#

#======================================================================================================================#
# UserFollowing
#======================================================================================================================#

class UserFollowing(models.Model):
    
    #------------------------------------------------------------------------------------------------------------------#

    class Meta:
        db_table = 'user_following'
        unique_together = ('follower_id', 'followee_id')

    #------------------------------------------------------------------------------------------------------------------#

    objects = UserFollowingManager()

    #------------------------------------------------------------------------------------------------------------------#

    follower_id = ForeignKey(User, on_delete = models.CASCADE, null = False, related_name = 'follower')
    followee_id = ForeignKey(User, on_delete = models.CASCADE, null = False, related_name = 'followee')
    request_timestamp = DateTimeField(auto_now_add = True)

    FOLLWER_ID = 'follower_id'
    FOLLWEE_ID = 'followee_id'

#======================================================================================================================#
# End of UserFollowing
#======================================================================================================================#

#======================================================================================================================#
# UserBlockManager
#======================================================================================================================#

class UserBlockManager(models.Manager):
    
    #------------------------------------------------------------------------------------------------------------------#

    def create_user_block(self):
        pass

#======================================================================================================================#
# End of UserBlockManager
#======================================================================================================================#

#======================================================================================================================#
# UserBlock
#======================================================================================================================#

class UserBlock(models.Model):
    
    #------------------------------------------------------------------------------------------------------------------#

    class Meta:
        db_table = 'user_block'
        unique_together = ('blocked_by_user_id', 'blocked_user_id')

    #------------------------------------------------------------------------------------------------------------------#

    objects = UserBlockManager()

    #------------------------------------------------------------------------------------------------------------------#

    blocked_user_id = ForeignKey(User, on_delete = models.CASCADE, null = False, related_name = 'blocked_user_id')
    blocked_by_user_id = ForeignKey(User, on_delete = models.CASCADE, null = False, related_name = 'blocked_by_user_id')
    timestamp = DateTimeField(auto_now_add = True, null = False)

    BLOCKED_USER_ID = 'blocked_user_id'
    BLOCKED_BY_USER_ID = 'blocked_by_user_id'

#======================================================================================================================#
# End of UserBlock
#======================================================================================================================#