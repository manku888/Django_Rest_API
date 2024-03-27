
from django.urls import path, include
from Users.views import SendPasswordRestEmailView, UserChangePassworView, UserLoginView, UserRegistrationView
urlpatterns = [
     path('register/', UserRegistrationView.as_view(), name='register'),
      path('login/', UserLoginView.as_view(), name='login'),
      path('chanagepassword/', UserChangePassworView.as_view(), name='chanagepassword'),
      path('send-rest-password-email/', SendPasswordRestEmailView.as_view(), name='send-rest-password-email'),
    
]
