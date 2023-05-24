from .models import Inventory, InventoryGroup, Shop
from user_control.serializers import CustomUserSerializer
from rest_framework import serializers

'''
serializers.ModelSerializer can provide extra customization as well. It offers a convenient way to generate serializer fields based on 
the model fields, but it also allows you to override and customize the generated fields or define additional fields.

You can customize the behavior of serializer fields by specifying additional options such as read_only, write_only, required, and more. 
You can also define custom serializer methods to handle complex field serialization or validation logic. Furthermore, you can override the 
default create() and update() methods of the serializer to control how the data is saved or updated in the database.
'''

class InventoryGroupSerializer(serializers.ModelSerializer):
  '''
  The read_only option is useful when you want to include a field in the serialized output but prevent it from being updated when the data is 
  submitted for deserialization. This can be useful, for example, when you have computed fields or fields that should be automatically 
  generated and should not be modified by the client.
  
  The write_only option is used in serializers to mark certain fields as write-only, meaning they will be included during deserialization (write) 
  but will not be included in the serialized representation when the data is retrieved (read).
  
  The purpose of write-only fields is typically to handle sensitive or confidential information that should not be exposed in the API response. 
  For example, when creating a new user, you might include a password field as write-only, so it's only used for creating the user object but 
  not included in the serialized representation when the user data is retrieved.
  '''
  # When you request the InventoryGroup data, the serialized representation of each InventoryGroup object will include the serialized 
  # representation of the related CustomUser object (created_by field). This allows you to access information about the related CustomUser 
  # when retrieving InventoryGroup data.
  # However, since created_by is set to read_only=True, you won't be able to provide the created_by field when creating or updating 
  # InventoryGroup objects through the serializer. The deserialization process will ignore the created_by field, and it will not be included 
  # in the list of writable fields. This ensures that you can't modify the created_by field directly through the serializer.
  
  # created_by field displays information about the creator. 
  # When creating or updating an InventoryGroup, you can use the created_by_id  field to associate it with a specific CustomUser 
  # without the need to provide all the details of the CustomUser object.
  created_by = CustomUserSerializer(read_only=True)
  created_by_id = serializers.CharField(write_only=True, required=False)
  belongs_to = serializers.SerializerMethodField(read_only=True)
  belongs_to_id = serializers.CharField(write_only=True)
  total_items = serializers.CharField(read_only=True, required=False)
  
  class Meta:
    model = InventoryGroup
    fields = "__all__"
    
  def get_belongs_to(self, obj):
    if obj.belongs_to is not None:
      return InventoryGroupSerializer(obj.belongs_to).data
    return None

class InventorySerializer(serializers.ModelSerializer):
  created_by = CustomUserSerializer(read_only=True)
  created_by_id = serializers.CharField(write_only=True, required=False)
  group = InventoryGroupSerializer(read_only=True)
  group_id = serializers.CharField(write_only=True)
  
  class Meta:
    model = Inventory
    fiels = "__all__"
    
class ShopSerializer(serializers.ModelSerializer):
  created_by = CustomUserSerializer(read_only=True)
  created_by_id = serializers.CharField(write_only=True, required=False)
  amount_total = serializers.CharField(read_only=True, required=False)
  count_total = serializers.CharField(read_only=True, required=False)
  
  class Meta:
    model = Shop
    fields = "__all__"