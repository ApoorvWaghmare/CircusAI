from rest_framework.pagination import PageNumberPagination

#----------#

#======================================================================================================================#
# HomeFeedPagination
#======================================================================================================================#

class HomeFeedPagination(PageNumberPagination):
    page_size = 10  # Items per page
    max_page_size = 10  # Maximum items per page
    max_page_number = 10  # Maximum number of pages

#======================================================================================================================#
# HomeFeedPagination
#======================================================================================================================#

#======================================================================================================================#
# SearchFeedPagination
#======================================================================================================================#

class SearchFeedPagination(PageNumberPagination):
    page_size = 20  # Items per page
    max_page_size = 20  # Maximum items per page
    max_page_number = 10  # Maximum number of pages

#======================================================================================================================#
# SearchFeedPagination
#======================================================================================================================#

#======================================================================================================================#
# ProfileFeedPagination
#======================================================================================================================#

class ProfileFeedPagination(PageNumberPagination):
    page_size = 20  # Items per page
    max_page_size = 20  # Maximum items per page
    max_page_number = 10  # Maximum number of pages

#======================================================================================================================#
# ProfileFeedPagination
#======================================================================================================================#
