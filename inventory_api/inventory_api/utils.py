import jwt
from datetime import datetime, timedelta
from django.conf import settings
from user_control.models import CustomUser
from rest_framework.pagination import PageNumberPagination
import re
from django.db.models import Q

# After user login, how long can he/she access the website without logging in again
def get_access_token(payload, days):
  '''
  This function is used to generate an access token for a user after successful authentication. 
  It takes a payload, which typically includes information about the user (e.g., user ID), 
  and the number of days for which the token should remain valid. The function generates a JWT token using the payload and 
  specified expiration time. This token can then be used by the client to authenticate subsequent requests to the server. 
  The purpose of this function is to provide a secure and time-limited token for user authentication and authorization.
  '''
  token = jwt.encode({'exp': datetime.now() + timedelta(days=days), **payload}, settings.SECRET_KEY, algorithm="HS256")
  return token

def decodeJWT(bearer):
  '''
  This function is used to decode and validate a JWT token provided by the client. 
  It takes a bearer token as input, which is typically included in the Authorization header of an HTTP request. 
  The function extracts the token from the "Bearer " prefix and attempts to decode it using the secret key specified in the Django settings. 
  If the decoding is successful and the token is valid, it retrieves the user_id from the token and attempts to fetch the corresponding 
  CustomUser instance from the database. 
  The purpose of this function is to authenticate and authorize the user based on the provided JWT token, 
  ensuring that the token is valid and associated with a valid user in the system.
  '''
  if not bearer:
    return None
  # It assumes that the token is prefixed with "Bearer " and takes the substring starting from the 7th character.
  token = bearer[7:]
  
  try:
    decoded = jwt.decode(token, key=settings.SECRET_KEY, algorithms="HS256")
  except Exception:
    return None
  
  if decoded:
    try:
      return CustomUser.objects.get(id=decoded["user_id"])
    except Exception:
      return None
    
class CustomPagination(PageNumberPagination):
  page_size = 20
  
def normalize_query(query_string, findterms=re.compile(r'"([^"]+)"|(\S+)').findall, normspace=re.compile(r'\s{2,}').sub):
    return [normspace(' ', (t[0] or t[1]).strip()) for t in findterms(query_string)]

def get_query(query_string, search_fields):
    query = None  # Query to search for every search term
    terms = normalize_query(query_string)
    for term in terms:
        or_query = None  # Query to search for a given term in each field
        for field_name in search_fields:
            q = Q(**{"%s__icontains" % field_name: term})
            if or_query is None:
                or_query = q
            else:
                or_query = or_query | q
        if query is None:
            query = or_query
        else:
            query = query & or_query
        return query