from django.urls import path, include
from .views import CreateUserView, LoginView, UpdatePasswordView, MeView, UsersView, UserActivitiesView
from rest_framework.routers import DefaultRouter

'''
The API root is the entry point or the starting point of an API. 
It represents the root URL of the API and provides a list of available endpoints or resources that can be accessed through the API.
In Django REST Framework, the API root is typically represented as a JSON response containing URLs for different resources or views in the API. 
This response helps clients understand the available endpoints and how to interact with them.
The API root is useful for navigation and discovering the available resources in an API. 
It serves as a central point to access various parts of the API and provides a high-level overview of the API's structure and functionality.
'''

router = DefaultRouter(trailing_slash = False)
router.register("create-user", CreateUserView, "create user")
router.register("login", LoginView, "login")
router.register("update-password", UpdatePasswordView, "update password")
router.register("me", MeView, "me")
router.register("activities-log", UserActivitiesView, "activities log")
router.register("users", UsersView, "users")

urlpatterns = [
    path("", include(router.urls))
]