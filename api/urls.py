from django.urls import path
from api.views import RegisterUser, SearchUserView, FriendRequestView

urlpatterns = [
    path('register/', RegisterUser.as_view(), name='create_user_api'),
    path('search-user/', SearchUserView.as_view(), name='search_user'),
    path('send-request/', FriendRequestView.as_view(), name='send_request'),
]