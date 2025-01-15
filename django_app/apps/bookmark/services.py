from django.db.models.query import QuerySet

#----------#

from .models import Bookmark

#----------#

from utilities.custom import Service
from apps.user.services import UserQueryService
from apps.post.models.mysql_models import Post

#======================================================================================================================#
# BookmarkQueryService
#======================================================================================================================#

@Service.wrap
class BookmarkQueryService:

    service_type = 'Query'

    #------------------------------------------------------------------------------------------------------------------#

    @staticmethod
    def get_all_bookmarks(user_id: int) -> QuerySet:
        user = UserQueryService.get_user(user_id)
        # Retrieve all bookmarks for the user
        bookmarks = Bookmark.objects.filter(user_id = user)
        # Return the posts related to the bookmarks
        return Post.objects.filter(id__in = bookmarks.values('post_id'))

#======================================================================================================================#
# End of BookmarkQueryService
#======================================================================================================================#

#======================================================================================================================#
# BookmarkAtomicService
#======================================================================================================================#

@Service.wrap
class BookmarkAtomicService:

    service_type = 'Atomic'

    #------------------------------------------------------------------------------------------------------------------#

    @staticmethod
    def add_bookmark(user: object, post: object) -> None:
        bookmark = Bookmark(user_id = user, post_id = post)
        bookmark.save()
    
    #------------------------------------------------------------------------------------------------------------------#

    @staticmethod
    def delete_bookmark(user: object, post: object) -> None:
        bookmark = Bookmark.objects.get(user_id = user, post_id = post)
        bookmark.delete()

#======================================================================================================================#
# End of BookmarkAtomicService
#======================================================================================================================#