from django.urls import path
from api.views import RegisterUser, SearchUserView, FriendRequestView, ListPendingRequestView, ManageFriendRequestView, ListAllFriends

urlpatterns = [
    path('register/', RegisterUser.as_view(), name='create_user_api'),
    path('search-user/', SearchUserView.as_view(), name='search_user'),
    path('send-request/', FriendRequestView.as_view(), name='send_request'),
    path('list-requests/', ListPendingRequestView.as_view(), name='list_friend_request'),
    path('manage-requests/', ManageFriendRequestView.as_view(), name='manage-requests'),
    path('lists-friends/', ListAllFriends.as_view(), name='lists-friends')
]