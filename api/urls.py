from django.urls import path
from api.views import RegisterUser

urlpatterns = [
    path('register/', RegisterUser.as_view(), name='create_user_api'),
]