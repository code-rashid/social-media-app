from django.shortcuts import render
from api.models import User, FriendRequest, UserActivityConstraints
from rest_framework.views import APIView
from rest_framework.response import Response
import rest_framework.status as status
from rest_framework.permissions import AllowAny, IsAuthenticated
from django.core.validators import validate_email
from django.core.exceptions import ValidationError
from django.db.models import Q
from utils.permissions import HasRequestLimit


class SearchUserView(APIView):

    permission_classes = [IsAuthenticated]

    def get(self, request):

        keyword = request.data.get('keyword')
        try:
            validate_email(keyword)
            users = User.objects.filter(email=keyword).values_list('email', flat=True)
        except Exception:
            query = Q()
            for char in keyword:
                query &= Q(name__icontains=char)
            users = User.objects.filter(query).values_list('email', flat=True)
        return Response(data={'results' : users}, status=status.HTTP_200_OK) 



class FriendRequestView(APIView):

    permission_classes = [IsAuthenticated, HasRequestLimit]

    def post(self, request):

        to = request.data.get('to_email')
        try:
            validate_email(to)
            user = User.objects.get(email=to)
            FriendRequest.objects.get_or_create(
                sender = request.user,
                receiver = user
            )
            user_constraints = UserActivityConstraints.objects.filter(user=request.user)
            if user_constraints.exists():
                user_constraints = user_constraints.first()
                user_constraints.request_limit = user_constraints.request_limit - 1
                user_constraints.save()
            else:
                UserActivityConstraints.objects.create(
                    user=request.user,
                    request_limit=2
                )

            return Response(data={'request sent successfully' : to}, status=status.HTTP_200_OK) 
        except Exception :
            return Response(status=status.HTTP_400_BAD_REQUEST)



class RegisterUser(APIView):
    '''
        This API View is used to reguster new user
    '''
    permission_classes = [AllowAny]

    def post(self, request):

        name = request.data.get('name')
        email = request.data.get('email')
        password = request.data.get('password')
        

        # Validate email format
        try:
            validate_email(email)
        except ValidationError:
            return Response(data={'message': 'Invalid email address'}, status=status.HTTP_400_BAD_REQUEST)

        if not name or not email or not password:
            return Response(data={'message': 'Please enter all required fields'}, status=status.HTTP_400_BAD_REQUEST)


        existing_users = User.objects.filter(email__iexact=email)
        if existing_users.exists():
            return Response(data={'message' : 'user already exists'}, status=status.HTTP_400_BAD_REQUEST) 
        
        
        user = User.objects.create(
            name = name, 
            email = email,
            password = password,
            is_active = True
        )
        user.set_password(password)
        user.save()
        return Response(data={'message' : 'user created'}, status=status.HTTP_201_CREATED)

