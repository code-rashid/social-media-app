from django.shortcuts import render
from api.models import User, FriendRequest, UserActivityConstraints, Friendship
from rest_framework.views import APIView
from rest_framework.response import Response
import rest_framework.status as status
from rest_framework.permissions import AllowAny, IsAuthenticated
from django.core.validators import validate_email
from django.core.exceptions import ValidationError
from django.db.models import Q
from utils.permissions import HasRequestLimit
from rest_framework.pagination import PageNumberPagination


class SearchUserView(APIView):

    """
    API endpoint to search for users by email or name.

    Users must be authenticated to access this endpoint.
    """

    permission_classes = [IsAuthenticated]

    def get(self, request):

        """
        Get method to search for users.

        If the keyword matches an exact email, return the user associated with that email.
        If the keyword contains any part of the name, return a list of all users with matching names.

        Parameters:
            request (HttpRequest): The HTTP request object.

        Returns:
            Response: A JSON response containing the search results.
        """

        keyword = request.data.get('keyword')
        try:
            # Attempt to validate the keyword as an email
            validate_email(keyword)
            users = User.objects.filter(email=keyword).values_list('email', flat=True)
        except Exception:
            # If keyword is not a valid email, search by name
            query = Q()
            for char in keyword:
                query &= Q(name__icontains=char)
            users = User.objects.filter(query).values_list('email', flat=True)
        return Response(data={'results' : users}, status=status.HTTP_200_OK) 


class ListPendingRequestView(APIView):

    """
    API endpoint to list pending friend requests received by the authenticated user.
    
    Users must be authenticated to access this endpoint.
    """

    permission_classes = [IsAuthenticated]

    def get(self, request):

        """
        Get method to retrieve pending friend requests.

        Retrieves a list of pending friend requests received by the authenticated user.

        Parameters:
            request (HttpRequest): The HTTP request object.

        Returns:
            Response: A JSON response containing the list of pending friend requests.
        """

        lists = FriendRequest.objects.filter(receiver=request.user, accepted=False).values_list('sender__email', flat=True)
        return Response(data={'results' : lists}, status=status.HTTP_200_OK) 
    

class ManageFriendRequestView(APIView):

    """
    API endpoint to manage friend requests received by the authenticated user.
    
    Users must be authenticated to access this endpoint.
    """

    permission_classes = [IsAuthenticated]

    def post(self, request):

        """
        POST method to manage friend requests.

        Accepts or rejects a friend request sent by another user.

        Parameters:
            request (HttpRequest): The HTTP request object containing data about the friend request.

        Returns:
            Response: A JSON response indicating the status of the friend request.
        """

        accept = request.data.get('accept')
        sender_email = request.data.get('sender')
        ref = FriendRequest.objects.filter(sender__email=sender_email, receiver=request.user)
        if ref.exists():
            ref = ref.first()
            if not accept:
                ref.delete()
                return Response(data={'accept-status' : accept}, status=status.HTTP_200_OK) 
            ref.accepted = accept
            ref.save()

            Friendship.objects.get_or_create(
                user = request.user,
                friend = ref.sender
            )

            return Response(data={'accept-status' : accept}, status=status.HTTP_200_OK) 
        else:
            return Response(data={'message': 'Invalid email address'}, status=status.HTTP_400_BAD_REQUEST)




class ListAllFriends(APIView):

    """
    API endpoint to list all friends of the authenticated user.

    Users must be authenticated to access this endpoint.
    """

    permission_classes = [IsAuthenticated]

    def get(self, request):

        """
        GET method to retrieve a paginated list of all friends of the authenticated user.

        Parameters:
            request (HttpRequest): The HTTP request object.

        Returns:
            Response: A paginated JSON response containing a list of all friends.
        """

        paginator = PageNumberPagination()
        paginator.page_size = 10 # Number of friends per page

        your_friends = Friendship.objects.filter(user=request.user)
        you_as_friend = Friendship.objects.filter(friend=request.user)

        friend_emails = list(your_friends.values_list('friend__email', flat=True)) + \
                        list(you_as_friend.values_list('user__email', flat=True))

        # Paginate the friend list
        result_page = paginator.paginate_queryset(friend_emails, request)
        
        # Return paginated response
        return paginator.get_paginated_response({'lists': result_page})



class FriendRequestView(APIView):

    """
    API endpoint for sending friend requests.

    Users must be authenticated and have request limits to access this endpoint.
    """

    permission_classes = [IsAuthenticated, HasRequestLimit]

    def post(self, request):

        """
        POST method to send a friend request to a specified user.

        Parameters:
            request (HttpRequest): The HTTP request object containing the 'to_email' field.

        Returns:
            Response: A JSON response indicating the success or failure of the request.
        """

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

