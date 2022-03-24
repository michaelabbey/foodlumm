from django.contrib import admin

# Register your models here.
from . models import *


class VarietyAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'slug', 'image', 'created', 'updated')
    list_display_links = ('id','name', 'slug')
    prepopulated_fields = {'slug':('name',)}
    


class MealAdmin(admin.ModelAdmin):
    list_display = ('id', 'variety', 'meal','slug', 'image', 'spicy', 'time', 'price','discount','max_order', 'max_order', 'breakfast', 'lunch', 'dinner','display', 'created', 'updated')
    list_display_links = ('id','variety', 'meal','slug')
    list_editable = ['display','discount']
    prepopulated_fields = {'slug':('meal',)}
    


class ContactAdmin(admin.ModelAdmin):
    list_display = ['id', 'first_name', 'last_name', 'phone', 'email', 'message', 'created','status', 'closed']
    list_display_links = ['id', 'first_name', 'last_name', 'phone']
    


class ProfileAdmin(admin.ModelAdmin):
    list_display = ['user', 'first_name', 'last_name', 'phone', 'address', 'state', 'country', 'image', 'cart_code']
    list_display_links = ['user', 'first_name', 'last_name', 'cart_code']




admin.site.register(Variety,VarietyAdmin)   
admin.site.register(Meal,MealAdmin)    
admin.site.register(Contact,ContactAdmin)   
admin.site.register(Profile,ProfileAdmin)


