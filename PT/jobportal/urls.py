from django.urls import path
from . import views
urlpatterns = [
    path('',views.base,name='base'),
    path('signup/',views.signup,name='signup'),
    path('signin/',views.signin,name='signin'),
    path('logout/',views.logout,name='logout'),
]
