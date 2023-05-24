from rest_framework.permissions import BasePermission
# It provides a framework for defining the logic that determines 
# whether a user has permission to perform a specific action on a particular resource.
# To use BasePermission, you need to create a subclass and override the has_permission() and/or has_object_permission() methods. 
# These methods contain the logic to determine the permission based on the request and the resource being accessed.
from .utils import decodeJWT

class IsAuthenticatedCustom(BasePermission):
  def has_permission(self, request, view):
    '''
    In the has_permission() method, you can define the permission logic based on the request and the view being accessed. 
    The purpose of this method is to provide a global permission check based on the presence and validity of a JWT token in the 
    request's Authorization header. If the token is valid, it sets the authenticated user in the request, allowing subsequent 
    authentication and authorization checks to be performed within the view or other parts of the code. 
    If the token is invalid or not provided, it denies access to the view.
    
    In other words: The has_permission function checks whether the user has logged in and has been authorized to 
                    access the system for the duration specified by the token.
    '''
    try:
      auth_token = request.Meta.get("HTTP_AUTHORIZATION", None)
    except Exception:
      return False
    if not auth_token:
      return False
    
    user = decodeJWT(auth_token)
    if not user:
      return False
    request.user = user
    return True
    