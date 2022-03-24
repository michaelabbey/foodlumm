from email.policy import default
from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Variety(models.Model):
    name = models.CharField(max_length=100)
    slug = models.SlugField(unique=True, null=False)
    image = models.ImageField(upload_to='variety', default='variety.jpg', blank=True, null=True)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return self.name
    
    class Meta:
        db_table = 'variety'
        managed = True
        verbose_name = 'Variety'
        verbose_name_plural = 'Varieties'  

  
    
SPICEY = [
    ('Not','Not'),
    ('Mild','Mild'),
    ('Medium','Medium'),
    ('Hot','Hot'),
    ('Extra Hot','Extra Hot'),
]  

class Meal(models.Model):
    variety = models.ForeignKey(Variety, on_delete=models.CASCADE)
    meal = models.CharField(max_length=100)
    slug = models.SlugField(unique=True, null=False)
    # menu = models.TextField()
    image = models.ImageField(upload_to='meal', default= 'meal.jpg')
    spicy = models.CharField(max_length=100)
    time = models.CharField(max_length=50)
    price = models.IntegerField()
    discount = models.FloatField()
    min_order = models.IntegerField(default=1)
    max_order = models.IntegerField(default=20)
    breakfast = models.BooleanField()
    lunch = models.BooleanField()
    dinner = models.BooleanField()
    display = models.BooleanField(default=False)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return self.meal
    
    class Meta:
        db_table = 'meal'
        managed = True
        verbose_name = 'Meal'
        verbose_name_plural = 'Meals'
        

STATUS = [
    ('New', 'New'),
    ('Pending', 'Pending'),
    ('Processing', 'Processing'),
    ('Closed', 'Closed'),
]
      
class Contact(models.Model):
    first_name = models.CharField(max_length=150, blank=True, null=True)
    last_name = models.CharField(max_length=150,blank=True, null=True)
    phone = models.CharField(max_length=20, blank=True, null=True)
    email = models.EmailField(blank=True, null=True)
    message = models.TextField(blank=True, null=True)
    created = models.DateTimeField(auto_now_add=True)
    closed = models.DateTimeField(blank=True, null=True)
    status = models.CharField(max_length=50, choices=STATUS, default='New')
    
    def __str__(self):
        return self.first_name
    
    class Meta:
        db_table = 'contact'
        managed = True
        verbose_name = 'Contact'
        verbose_name_plural = 'Contacts'

 
class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    phone = models.CharField(max_length=20, blank=True, null=True )
    address = models.CharField(max_length=100, blank=True, null=True)
    state = models.CharField(max_length=50, blank=True, null=True)
    country = models.CharField(max_length=50, blank=True, null=True)
    image = models.ImageField(upload_to='profile', default='favw.jpeg', blank=True, null=True)
    cart_code = models.AutoField(primary_key=True, serialize=True)
    
    
    def __str__(self):
        return self.user.username    
    
    class Meta:
        db_table = 'profile'
        managed = True
        verbose_name = 'Profile'
        verbose_name_plural = 'Profiles'
  