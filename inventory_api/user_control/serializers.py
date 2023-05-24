from rest_framework import serializers
from .models import CustomUser, Roles, UserActivities
'''
Serializers in Django Rest Framework (DRF) provide a way to convert complex data types, such as Django models, 
into Python data types that can be easily rendered into JSON or XML format.

When you want to include all fields from the model in the serializer without any additional customization, 
you can use serializers.ModelSerializer. This serializer class automatically generates serializer fields for all fields in the model.

However, if you need to include additional data or perform custom validation and processing that goes beyond simple field serialization, 
you can use serializers.Serializer. This serializer class allows you to define each field explicitly and provides more flexibility for 
customization. You can include fields that are not part of the model, handle nested relationships, define custom validation rules, and 
perform data transformations.

So, if you have a straightforward case where you want to include all fields from the model without any extra customization, 
serializers.ModelSerializer is convenient and saves you from explicitly defining each field. But if you need more control and customization 
over the serialization process, serializers.Serializer gives you the flexibility to define fields and their behavior according to your specific 
requirements.
'''

class CreateUserSerializer(serializers.Serializer):
  email = serializers.EmailField()
  fullname = serializers.CharField()
  role = serializers.ChoiceField(Roles)
  
class LoginSerializer(serializers.Serializer):
  email = serializers.EmailField()
  password = serializers.CharField(required=False)
  is_new_user = serializers.BooleanField(default=False, required=False)
  # The login flow may have different requirements for different cases. 
  # For example, if the user is not a new user, then the password field may be required, 
  # while if the user is a new user, they may be logging in for the first time and hence do not have a password yet. 
  # In this case, is_new_user may be used to indicate that the user is new and the authentication flow will be different.
  # By setting these fields as not required, it allows for more flexibility in how the serializer is used in different scenarios.
  
class UpdatePasswordSerializer(serializers.Serializer):
  user_id = serializers.CharField()
  password = serializers.CharField()
  
class CustomUserSerializer(serializers.ModelSerializer):
  class Meta:
    model = CustomUser
    exclude = ("password", )

class UserActivitiesSerializer(serializers.ModelSerializer):
  class Meta:
    model = UserActivities
    fields = ("__all__")