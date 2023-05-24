from django.db import models
from django.contrib.auth.models import (
  AbstractBaseUser, PermissionsMixin, BaseUserManager
)

# Create your models here.
Roles = (("admin", "admin"), ("creator", "creator"), ("sale", "sale"))

# Inherit BaseUserManager
class CustomUserManager(BaseUserManager):
  def create_superuser(self, email, password, **extra_fields):
    '''
    The **extra_fields parameter allows for passing any additional fields as key-value pairs that are not part of the method signature. 
    By using the setdefault method on the extra_fields dictionary, the code ensures that certain fields have a default value if they are not passed as part of the **extra_fields. 
    For example, if is_staff is not provided in extra_fields, it will default to True. 
    Similarly, is_superuser and is_active will default to True as well. 
    This is useful because when creating a superuser, we want to ensure that certain properties are set to their default values, and we don't want to rely on the caller to always pass in the correct values. 
    By setting the defaults in the code, we can ensure that the created superuser has the expected properties.
    '''
    extra_fields.setdefault("is_staff", True)
    extra_fields.setdefault("is_superuser", True)
    extra_fields.setdefault("is_active", True)
    
    if extra_fields.get("is_staff") is not True:
      raise ValueError("Superuser must be a staff, set is_staff=True.")
    
    if extra_fields.get("is_superuser") is not True:
      raise ValueError("Superuser must be a superuser, set is_superuser=True.")
    
    if not email:
      raise ValueError("Email field is required")
    
    # Saving admin into the database
    user = self.model(email = email, **extra_fields)
    user.set_password(password)
    user.save()
    
    return user
  
class CustomUser(AbstractBaseUser, PermissionsMixin):
  fullname = models.CharField(max_length=255)
  email = models.EmailField(unique=True)
  role = models.CharField(max_length=8, choices=Roles)
  created_at = models.DateTimeField(auto_now_add=True)
  updated_at = models.DateTimeField(auto_now=True)
  is_staff = models.BooleanField(default=False)
  is_superuser = models.BooleanField(default=False)
  is_active = models.BooleanField(default=True)
  last_login = models.DateTimeField(null=True)
  
  # email is set as the identity to identify users when logging in
  USERNAME_FIELD = "email"
  
  # Specify the admin of this user
  # CustomUserManager is a custom manager that inherits from BaseUserManager, and it provides some additional functionality for creating and managing user accounts. By setting objects = CustomUserManager() inside the CustomUser model, we are specifying that all instances of CustomUser should use CustomUserManager as their default manager. This means that all queries made on the CustomUser model will use CustomUserManager by default, unless another manager is specified explicitly.
  objects = CustomUserManager()
  
  def __str__(self):
    '''
    Returns a string representation of the user object. 
    In this case, it returns the user's email address.
    '''
    return self.email
  
  class Meta:
    '''
    This inner class contains metadata about the model. 
    In this case, it specifies the default ordering for query sets of CustomUser objects. 
    Query sets will be ordered by the created_at field in ascending order.
    '''
    ordering = ("created_at", )
    
class UserActivities(models.Model):
  '''
  CustomUser will access the UserActivities model using "user_activities",
  when a CustomUser object is deleted, the user field in the UserActivity model that references the deleted CustomUser object will be set to NULL.
  '''
  user = models.ForeignKey(CustomUser, on_delete=models.SET_NULL, related_name="user_activities", null=True)
  email = models.EmailField()
  fullname = models.CharField(max_length=255)
  action = models.TextField()
  created_at = models.DateTimeField(auto_now_add=True)
  
  class Meta:
    ordering = ("-created_at", )
    
  def __str__(self):
    return f"{self.fullname} {self.action} on {self.created_at.strftime('%Y-%m-%d %H-%M')}"