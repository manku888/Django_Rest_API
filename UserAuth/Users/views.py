
from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView

from Users.serializers import SendPasswordRestSerializer, UserChangePasswordSerializer, UserLoginSerializer, UserRegistrationSerializer
from django.contrib.auth import authenticate
from rest_framework_simplejwt.tokens import RefreshToken
from Users.renders import UserRenderer
from rest_framework.permissions import IsAuthenticated
#Generate token manullay
def get_tokens_for_user(user):
    refresh = RefreshToken.for_user(user)

    return {
        'refresh': str(refresh),
        'access': str(refresh.access_token),
    }
# Create your views here.

#register User
class UserRegistrationView(APIView):
   renderer_classes = [UserRenderer]
   def post(self, request, format=None):
     serializer = UserRegistrationSerializer(data=request.data)
     if serializer.is_valid(raise_exception=True):
        user = serializer.save()
        token = get_tokens_for_user(user)
        return Response({'token':token,'msg':'Registration Successfull'},status=status.HTTP_201_CREATED)
     return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
   
#Login User
class UserLoginView(APIView):
   renderer_classes = [UserRenderer]
   def post(self, request, format=None):
     serializer = UserLoginSerializer(data=request.data)
     if serializer.is_valid(raise_exception=True):
        email = serializer.data.get('email')
        password =  serializer.data.get('password')
        user = authenticate(email=email, password=password)
        if user is not None:
           token = get_tokens_for_user(user)
           return Response({'token':token,'msg':'Login Successfull'},status=status.HTTP_200_OK)
        else:
           return Response({'errors':{'non_field_errors':['Email or password is not vaild']}},status=status.HTTP_404_NOT_FOUND)

class UserChangePassworView(APIView):
   renderer_classes =[ UserRenderer]
   permission_classes = [IsAuthenticated]
   def post(self, request, format=None):
      serializer = UserChangePasswordSerializer(data=request.data,context={'user':request.user})
      if serializer.is_valid(raise_exception=True):
         return Response({'msg':'password change Successfully'},status=status.HTTP_200_OK)
      return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    

class SendPasswordRestEmailView(APIView):
   renderer_classes =[ UserRenderer]
   def post(self, request, format=None):
      serializer = SendPasswordRestSerializer(data=request.data)
      if serializer.is_valid(raise_exception=True):
         return Response({'msg':'password Rest link send. please chacek your Email'},status=status.HTTP_200_OK)
      return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

   


