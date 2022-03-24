from unicodedata import name
from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('meals', views.meals, name='meals'),
    path('meal/<str:id>/<slug:slug>', views.meal, name='meal'),
    path('variety/<str:id>/<slug:slug>', views.variety, name='variety'),
    path('vary', views.vary, name='vary'),
    path('contact', views.contact, name='contact'),
    path('signin', views.signin, name='signin'),
    path('register', views.register, name='register'),
    path('logoutt', views.logoutt, name='logoutt'),
    path('user_profile', views.user_profile, name='user_profile'),
    path('profile_update', views.profile_update, name='profile_update'),
    path('password-update', views.password_update, name='password-update'),
    path('cart', views.cart, name='cart'),
    path('remove_item', views.remove_item, name='remove_item'),
    path('addtocart', views.addtocart, name='addtocart'),
    path('checkout', views.checkout, name='checkout'),
    path('paidorder', views.paidorder, name='paidorder'),
    path('placeorder', views.placeorder, name='placeorder'),    
    path('searchbar', views.searchbar, name='searchbar'),    
]
