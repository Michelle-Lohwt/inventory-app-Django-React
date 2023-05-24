from django.shortcuts import render
from rest_framework.viewsets import ModelViewSet
from .serializers import CreateUserSerializer, CustomUser, LoginSerializer, UpdatePasswordSerializer, CustomUserSerializer, UserActivities, UserActivitiesSerializer
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth import authenticate
from datetime import datetime
from inventory_api.utils import get_access_token
from inventory_api.custom_methods import IsAuthenticatedCustom

def add_user_activity(user, action):
  UserActivities.objects.create(
    user_id = user.id,
    email = user.email,
    fullname = user.fullname,
    action = action
  )

# Create your views here.
class CreateUserView(ModelViewSet):
  http_method_names = ["post"]
  queryset = CustomUser.objects.all()
  serializer_class = CreateUserSerializer
  permission_classes = (IsAuthenticatedCustom, )
  
  def create(self, request):
    valid_req = self.serializer_class(data=request.data)
    valid_req.is_valid(raise_exception=True)
    CustomUser.objects.create(**valid_req.validated_data)
    add_user_activity(request.user, "added_new_user")
    return Response({"success": "User data created successfully"}, status=status.HTTP_201_CREATED)
  
class LoginView(ModelViewSet):
  http_method_names = ["post"]
  queryset = CustomUser.objects.all()
  serializer_class = LoginSerializer()
  
  def create(self, request):
    valid_req = self.serializer_class(data=request.data)
    valid_req.is_valid(raise_exception=True)
    
    # new_user = valid_req.validated_data["is_new_user"] retrieves the value of a boolean field called is_new_user from the validated data.
    # If new_user is true, the code checks if a user with the given email already exists in the CustomUser model.
    # If a user with the given email exists, the code checks if the user already has a password.
    # If the user does not have a password, the user ID is returned in the response.
    # If the user has a password, an exception is raised indicating that the user already has a password.
    # If a user with the given email does not exist, an exception is raised indicating that the user was not found.
    new_user = valid_req.validated_data["is_new_user"]
    if new_user:
      user = CustomUser.objects.filter(email=valid_req.validated_data["email"])
      if user:
        user = user[0]
        if not user.password:
          return Response({"user_id": user.id})
        else:
          raise Exception ("User has password already")
      else:
        raise Exception("User with email not found")
    
    # If not new_user, proceed to check user in the database
    user = authenticate(
      username=valid_req.validated_data["email"],
      password=valid_req.validated_data.get("password", None)
    )
    if not user:
      return Response({"error": "Invalid email or password"}, status=status.HTTP_400_BAD_REQUEST)
    
    access = get_access_token({"user_id": user.id}, 1)
    user.last_login = datetime.now()
    user.save()
    add_user_activity(user, "logged in")
    return Response({"access": access})
  
class UpdatePasswordView(ModelViewSet):
  http_method_names = ["post"]
  queryset = CustomUser.objects.all()
  serializer_class = UpdatePasswordSerializer()
  
  def create(self, request):
    valid_req = self.serializer_class(data=request.data)
    valid_req.is_valid(raise_exception=True)
    
    user = CustomUser.objects.filter(id=valid_req.validated_data["user_id"])
    if not user:
      raise Exception("User with id not found")
    user = user[0]
    user.set_password(valid_req.validated_data["password"])
    user.save()
    add_user_activity(user, "updated password")
    return Response({"success": "User password updated"})
  
class MeView(ModelViewSet):
  http_method_names = ["get"]
  queryset = CustomUser.objects.all()
  serializer_class = CustomUserSerializer()
  permission_classes = (IsAuthenticatedCustom, )
  
  def list(self, request):
    data = self.serializer_class(request.user).data
    return Response(data)
  
class UserActivitiesView(ModelViewSet):
  http_method_names = ["get"]
  queryset = UserActivities.objects.all()
  serializer_class = UserActivitiesSerializer()
  permission_classes = (IsAuthenticatedCustom, )
  
class UsersView(ModelViewSet):
  http_method_names = ["get"]
  queryset = CustomUser.objects.all()
  serializer_class = CustomUserSerializer()
  permission_classes = (IsAuthenticatedCustom, )
  
  def list(self, request):
    '''
    Return a list of users that are not admin
    '''
    users = self.queryset().filter(is_superuser = False)
    data = self.serializer_class(users, many = True).data
    return Response(data)