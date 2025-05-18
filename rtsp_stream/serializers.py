from django.contrib.auth import authenticate
from django.contrib.auth.models import User
from django.contrib.auth.password_validation import validate_password
# from django.contrib.auth import get_user_model 

from rest_framework import serializers
from rest_framework.validators import UniqueValidator
from rest_framework.exceptions import AuthenticationFailed


class UserRegistrationSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(
        required=True,
        validators=[UniqueValidator(queryset=User.objects.all())]
    )

    password1 = serializers.CharField(write_only=True, required=True, validators=[validate_password])
    password2 = serializers.CharField(write_only=True, required=True)

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']

    def validate(self, attrs):
        # Ensure passwords match here
        if attrs['password1'] != attrs['password2']:
            raise (serializers.ValidationError({"password": "The two password fields didn't match."}))
        return attrs

    def create(self, validated_data):
        # Remove password1 and password2 from validated data; handle password encryption
        user = User(username=validated_data['username'],email=validated_data['email'],)
        # Set and hash user passwords securely
        user.set_password(validated_data['password1'])
        user.save()
        return user
    

class SignInSerializer(serializers.Serializer):
    username = serializers.CharField()
    password1 = serializers.CharField(write_only= True)

    def validate(self, data):
        username=data.get('username')
        password=data.get('password1')
        
        # print("DEBUG: username =", username)
        # print("DEBUG: password =", password)
        request= self.context.get('request')

        if not username or not password:
            raise serializers.ValidationError("Both username and password are required.")

        user = authenticate(request=request,username=username, password=password)

        if not user:
            raise AuthenticationFailed("Invalid username or password")
        
        return user
    
