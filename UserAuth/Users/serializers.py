from xml.dom import ValidationErr
from django.forms import ValidationError
from rest_framework import serializers
from Users.models import User
from django.utils.encoding import smart_str,force_bytes,DjangoUnicodeDecodeError
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode
from django.contrib.auth.tokens import PasswordResetTokenGenerator

class UserRegistrationSerializer(serializers.ModelSerializer):
    confirm_password = serializers.CharField(style={'input_type':'password'}, write_only=True)
    class Meta:
        model = User
        fields = ['email','first_name','last_name','password', 'confirm_password','tc']
        extra_kwargs={
            'password':{'write_only':True}
        }

#validate psw and c-psw while registration
    def validate(self, attrs):
        password = attrs.get('password')
        confirm_password = attrs.get('confirm_password')
        if password != confirm_password:
            raise serializers.ValidationError("Password and Confirm Password doesNot Match")
        return attrs
    
    def create(self, validated_data):
        return User.objects.create_user(**validated_data)
    
class UserLoginSerializer(serializers.ModelSerializer):
     email= serializers.EmailField(max_length=255)
     class Meta:
        model = User
        fields = ['email','password']
        
class UserChangePasswordSerializer(serializers.Serializer):
    password = serializers.CharField(max_length=255,style={'input_type' : 'password'}, write_only=True)
    class Meta:
        fields =['password', 'confirm_password']
       
    
    def validate(self, attrs):
       password = attrs.get('password')
       confirm_password = attrs.get('confirm_password')
       user = self.context.get('user')
       if password != confirm_password:
        raise serializers.ValidationError("Password and Confirm Password doesNot Match")
       user.set_password(password)
       user.save()
       return attrs

class SendPasswordRestSerializer(serializers.Serializer):
    email = serializers.EmailField(max_length=255)
    class Meta:
        fields = ['email']
    
    def vaildate(self,attrs):
        email = attrs.get('email')
        if User.objects.filter(email=email).exists():
            user = User.objects.get(email=email)
            uid =urlsafe_base64_encode(force_bytes(user.id))
            token = PasswordResetTokenGenerator().make_token(user)
            link ='http://localhost:3000/api/user/reset/'+uid+'/'+token
            print('password Rest Link', link)
            return attrs
        else:
            raise ValidationErr('you are not a Registered User')
       
     