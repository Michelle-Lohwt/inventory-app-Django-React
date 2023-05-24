from rest_framework.viewsets import ModelViewSet
from .serializers import Inventory, InventorySerializer, InventoryGroup, InventoryGroupSerializer, Shop, ShopSerializer
from rest_framework.response import Response
from inventory_api.custom_methods import IsAuthenticatedCustom
from inventory_api.utils import CustomPagination, get_query
from django.db.models import Count

# Create your views here.
class InventoryView(ModelViewSet):
  '''
  With select_related, when you retrieve a user, you also have access to their corresponding activities directly. 
  It returns each user along with their activities in a combined result set. 
  You can access the activities of each user directly through the relationship between the user and activity models.
  
  UserActivities.objects.select_related("user") returns a queryset of user activities, where each user activity object has the related user object included. 
  So you get a list of user activities, and for each user activity, you also have the associated user object attached to it. 
  This is useful when you primarily want to work with user activities and also need access to the associated user information.
  '''
  queryset = Inventory.objects.select_related("group", "created_by")
  serializer_class = InventorySerializer
  permission_classes = (IsAuthenticatedCustom, )
  pagination_class = CustomPagination
  
  def get_queryset(self):
    if self.request.method.lower() != 'get':
      return self.queryset
    
    data = self.request.query_params.dict()
    data.pop("page")
    keyword = data.pop("keyword", None)
    
    results = self.queryset(**data)
    
    if keyword:
      search_fields = ("code", "created_by__fullname", "created_by__email", "group__name", "name")
      query = get_query(keyword, search_fields)
      return results.filter(query)
    
    return results
  
  def create(self, request, *args, **kwargs):
    request.data.update({"created_by_id": request.user.id})
    return super().create(request, *args, **kwargs)
  
class InventoryGroupView(ModelViewSet):
  '''
  On the other hand, with prefetch_related, it retrieves a list of users and a list of activities separately, and then links them together based on the defined relationship. 
  It returns the users and activities as separate result sets but ensures that the activities are efficiently fetched and ready to be accessed when needed. 
  This can be useful when you have multiple users and want to access their activities without making additional queries for each user.
  
  CustomUser.objects.prefetch_related("user_activities") returns a queryset of users, where each user object has its related user activities prefetched. 
  So you get a list of users, and for each user, you also have a separate list of their associated user activities. 
  The user activities are fetched efficiently in advance to minimize database queries. 
  This is useful when you primarily want to work with users and also need access to their related user activities.
  
  The query InventoryGroup.objects.select_related("belongs_to", "created_by").prefetch_related("inventories") will return a queryset of 
  InventoryGroup objects that have their related fields "belongs_to" and "created_by" pre-selected. This means that when you access the 
  related fields belongs_to and created_by on an InventoryGroup instance, the data will already be available without requiring additional 
  database queries.
  Additionally, the prefetch_related("inventories") part of the query prefetches the related "inventories" for each InventoryGroup. 
  This means that when you access the "inventories" field on an InventoryGroup instance, the associated inventories will already be available 
  in memory without needing to query the database again.
  '''
  queryset = InventoryGroup.objects.select_related("belongs_to", "created_by").prefetch_related("inventories")
  serializer_class = InventoryGroupSerializer
  permission_classes = (IsAuthenticatedCustom, )
  pagination_class = CustomPagination
  
  def get_queryset(self):
    if self.request.method.lower() != 'get':
      return self.queryset
    
    data = self.request.query_params.dict()
    data.pop("page")
    keyword = data.pop("keyword", None)
    
    results = self.queryset(**data)
    
    if keyword:
      search_fields = ("created_by__fullname", "created_by__email", "name")
      query = get_query(keyword, search_fields)
      results = results.filter(query)
    
    return results.annotate(
      total_items = Count('inventories')
    )
  
  def create(self, request, *args, **kwargs):
    request.data.update({"created_by_id": request.user.id})
    return super().create(request, *args, **kwargs)
  
class ShopView(ModelViewSet):
  queryset = Shop.objects.select_related("created_by")
  serializer_class = ShopSerializer
  permission_classes = (IsAuthenticatedCustom, )
  pagination_class = CustomPagination
  
  def get_queryset(self):
    if self.request.method.lower() != 'get':
      return self.queryset
    
    data = self.request.query_params.dict()
    data.pop("page")
    keyword = data.pop("keyword", None)
    
    results = self.queryset(**data)
    
    if keyword:
      search_fields = ("created_by__fullname", "created_by__email", "name")
      query = get_query(keyword, search_fields)
      results = results.filter(query)
    
    return results
  
  def create(self, request, *args, **kwargs):
    request.data.update({"created_by_id": request.user.id})
    return super().create(request, *args, **kwargs)