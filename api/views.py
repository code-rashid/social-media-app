from django.shortcuts import render
from api.models import User
from rest_framework.views import APIView
from rest_framework.response import Response
import rest_framework.status as status
from rest_framework.permissions import AllowAny
from django.core.validators import validate_email
from django.core.exceptions import ValidationError




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

