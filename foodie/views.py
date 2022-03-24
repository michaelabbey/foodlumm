import json
import uuid
import requests
import json


from ast import If
from multiprocessing import context
from urllib import request
from django.shortcuts import redirect, render
from django.http import HttpResponse
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.decorators import login_required
from django.db.models import Q



# Create your views here.
from foodie.models import *
from shopcart.models import *
from foodie.forms import *



def index(request):
    breakfast = Meal.objects.filter(breakfast=True,display=True).order_by('-id')[:4]
    lunch = Meal.objects.filter(lunch=True,display=True).order_by('-id')[:4]
    dinner = Meal.objects.filter(dinner=True,display=True).order_by('-id')[:4]
    varieties = Variety.objects.all()
          
    
    context = {
        'breakfast':breakfast,
        'lunch':lunch,
        'dinner':dinner,
        'varieties':varieties,  
    }
    return render(request, 'index.html', context)

#searchbar
def searchbar(request):
    if request.method == 'GET':
        query = request.GET.get('query')
        if query:
            meal = Meal.objects.filter(Q(Q(meal__icontains=query)|Q(time__icontains=query)))
            return render(request, 'searchbar.html',{'meal':meal})
        else:
            meal = Meal.objects.all()
            return render(request, 'searchbar.html',{'meal':meal})
#searchbar done
    

def meals(request):
    meals = Meal.objects.all() #This is show casing all the meals we have in our DB.
        
    context = {
        'meals':meals,
    }
    return render(request, 'meals.html', context)




def meal(request, id,slug):
    meal = Meal.objects.get(pk=id) #This is getting each meals by their specify ID. in this place, we use objects.get
    
    context = {
        'meal':meal,    }
    return render(request, 'meal.html', context)




def variety(request, id, slug):
    variety = Meal.objects.filter(variety_id=id) 
    single = Variety.objects.get(pk=id)
    
    context = {
        'variety': variety,
        'single':single,    }
    return render(request, 'variety.html', context)

def vary(request):
    varieties = Variety.objects.all() 
    
    context = {
        'varieties': varieties,}
    return render(request, 'vary.html', context)


#shopcart
@login_required(login_url='signin')
def cart(request):
    cart =Shopcart.objects.filter(user__username=request.user.username, item_paid=False)
    
    total = 0
    var = 0
    subtotal = 0
    
    for item in cart:
        if item.meal.discount:
            subtotal += item.meal.discount * item.quantity
        else:
            subtotal += item.meal.price * item.quantity
                        
    var = 0.075 * subtotal # please note that, vat is at 7.5% of the subtotal, that is 75/100 * subtotal
    total = var + subtotal   # Please note, Addition of vat and subtotal gives the total value to be charged
    context = {
        'cart':cart,
        'subtotal':subtotal,
        'var':var,
        'total':total,    }
    return render(request, 'cart.html',context)

@login_required(login_url='signin')
def remove_item(request): #This is the function to remove an item from the cart page.
    deleteitem = request.POST['deleteitem']
    Shopcart.objects.filter(pk=deleteitem).delete()
    messages.success(request, 'Item successfully deleted from your shopcart')
    return redirect('meals')

@login_required(login_url='signin')
def checkout(request):
    cart = Shopcart.objects.filter(user__username=request.user.username,item_paid=False)
    user_profile = Profile.objects.get(user__username=request.user.username)
    total = 0
    var = 0
    subtotal = 0
    
    for item in cart:
        if item.meal.discount:
            subtotal += item.meal.discount * item.quantity
        else:
            subtotal += item.meal.price * item.quantity
            
    var = 0.075 * subtotal # please note that, vat is at 7.5% of the subtotal, that is 75/100 * subtotal
    total = var + subtotal   # Please note, Addition of vat and subtotal gives the total value to be charged
    context = {
        'cart':cart,
        'total':total,
        'user_profile':user_profile,
        # 'orderno': cart[0].order_no
    }
    return render(request, 'checkout.html', context)


#shopcartdone


#Thank you page
def paidorder(request):
    profile = Profile.objects.get(user__username = request.user.username)
    #we are trying to empty our cart page after payment as been done.
    cart = Shopcart.objects.filter(user__username = request.user.username, item_paid=False)
    for item in cart:
        item.item_paid = True
        item.save()
        
    context = {
        'profile':profile
    }
    return render(request, 'paidorder.html', context)
#Thank you page done

#placeorder
@login_required(login_url='signin')
def placeorder(request):
    if request.method == 'POST':
        #collect data to send to paystack.
        # the api_key(registration programming interface key) and curl will be sourced from paystack site, 
        # paystack will give text secret key for testing, when you want to go liv, paystack will give live key.
        # cburl (callback url),total,ref_num,order_num,email provided by me in my application, 
        api_key = 'sk_test_1690919ca38995c567f6aa2748e35877709b5ff4' #This is from paystack
        curl = 'https://api.paystack.co/transaction/initialize' #This is from paystack Api documentation
        cburl = 'http://3.80.138.169/paidorder' #This ip '54.86.10.239' address is from the one i got from AWS.
        # cburl = 'http://localhost:8000/paidorder'
        ref_num = str(uuid.uuid4())
        total = float(request.POST['get_total']) * 100
        phone = request.POST['phone']
        address = request.POST['address']
        state = request.POST['state']
        cartno = Profile.objects.get(user__username=request.user.username)
        order_num = cartno.cart_code
        # order_num = request.POST['get_orderno']
        user = User.objects.get(username = request.user.username)
        
        
        headers = {'Authorization': f'Bearer {api_key}'}
        data = {'reference':ref_num, 'order_number':order_num, 'amount':int(total), 'callback_url':cburl, 'email':user.email, 'currency':'NGN'}
        #collect data to send to paystack done.
        
        #call to paystack
        try:
            r = requests.post(curl,headers=headers, json=data)
        except Exception:
            messages.error(request, 'Network busy, please refresh and try again. Thank You.')   
        else:
            transback = json.loads(r.text)
            rd_url = transback['data']['authorization_url']  
            
            
            # take record of transactions made
            paidorder = PaidOrder()
            paidorder.user = user
            paidorder.total = total/100
            paidorder.cart_no = order_num
            paidorder.payment_code = ref_num
            paidorder.paid_item = True
            paidorder.first_name = user.first_name
            paidorder.last_name = user.last_name
            paidorder.email = user.email
            paidorder.save()
            
            
            shipping = Shipping()
            shipping.user = user
            shipping.shipping_no = order_num
            shipping.paid_cart = True
            shipping.first_name = user.first_name
            shipping.last_name = user.last_name
            shipping.phone = phone
            shipping.address = address
            shipping.state = state
            # shipping.meal = Meal.objects.get('Meal')
            shipping.save()
            # take record of transactions made done
            return redirect(rd_url)
        #call to paystack done, when transaction is successful is redirected to the callback page.
    
    
#add to cart
@login_required(login_url='signin')
def addtocart(request):
    # cart_code = str(uuid.uuid4())
    cartno = Profile.objects.get(user__username=request.user.username)
    cart_code = cartno.cart_code
    if request.method == 'POST':
        addquantity = int(request.POST['quantity'])
        addspice = request.POST['how_spicey']
        addid = request.POST['mealid']
        mealid = Meal.objects.get(pk=addid)
        addspicy = request.POST.get('spicy', None)
        
        
        # instantiate the cart for prospective user
        cart = Shopcart.objects.filter(user__username=request.user.username,item_paid=False)
        
        if cart:  # instantiate the cart for a selected item
            more = Shopcart.objects.filter(meal_id=mealid.id,user__username=request.user.username).first()
            if more:
                more.quantity += addquantity
                more.how_spicey += addspice
                more.save()
                messages.success(request, 'Product added to shopcart!')
                return redirect('meals')
            else: #add new items to cart
                newitem = Shopcart()
                newitem.user = request.user
                newitem.meal = mealid
                newitem.quantity = addquantity
                newitem.how_spicey = addspice
                newitem.order_no = cart_code
                newitem.item_paid = False
                newitem.save()
                messages.success(request, 'added!')
                return redirect('meals')
                
        else: # create a cart
            newcart = Shopcart()
            newcart.user = request.user
            newcart.meal = mealid
            newcart.quantity = addquantity
            newcart.how_spicey = addspice
            newcart.order_no = cart_code
            newcart.item_paid = False
            newcart.save()
            messages.success(request, f'Item has been added to your shopcart 🛒')
            
    return redirect('meals')




#contact 
def contact(request):
    cform = ContactForm() #instantiate an empty form for a GET request
    if request.method == 'POST':
        cform = ContactForm(request.POST)#instantiate the form for a POST request
        if cform.is_valid():
            cform.save()
            messages.success(request, 'Thank you for contacting us, Our Customer Care will reach you soon😊')
            return redirect('index')
        else:
            messages.error(request, cform.errors)
            return redirect('index')
    
    context = {
        'cform':cform
    }
    
    return render(request,'index.html', context)
#contact done

#profile 
@login_required(login_url='signin')
def user_profile(request):
    user_profile = Profile.objects.get(user__username=request.user.username)
    
    context = {
        'user_profile':user_profile,    }
    return render(request, 'user_profile.html',context)

@login_required(login_url='signin')
def profile_update(request):
    load_profile = Profile.objects.get(user__username=request.user.username)
    form = ProfileForm(instance=request.user.profile)
    if request.method == 'POST':
        form = ProfileForm(request.POST, request.FILES, instance=request.user.profile)
        if form.is_valid():
            henry=form.save()
            messages.success(request, f'{henry.first_name} your profile is updated successful🙂')
            return redirect('user_profile')
        
    context = {
        'load_profile':load_profile,
        'form':form
    }
    
    return render(request, 'profile_update.html', context)
#profile done


#authentication methods
def register(request):
    form = RegisterForm() #instantiate the reistration form for a GET request
    if request.method =='POST': # check if a POST method for persisting data to the DB
        phone = request.POST['phone']
        image = request.POST['image']
        form = RegisterForm(request.POST) # instantiate the reisterform for a POST request
        if form.is_valid(): # ensures security checks here
            user = form.save() # save data if data is valid
            profile = Profile(user = user)
            profile.first_name = user.first_name
            profile.last_name = user.last_name
            profile.phone = phone
            profile.image = image
            profile.save()
            login(request, user)
            messages.success(request, f'{user.first_name} Your Registeration Was Successful😊')
            return redirect('signin') # send user any page you desire, in this case Homepage
        else:
            messages.error(request, form.errors)
            return redirect('register')
    
    context = {
        'form':form
    }
        
    return render(request, 'register.html', context)



def signin(request):
    #making a post request
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request,username=username,password=password)
        if user:
            login(request, user)
            messages.success(request, f'welcome {user.first_name}, its good to have you here!')
            return redirect('index')
        else:
            return redirect('signin')
    
    context = {    }
    
    return render(request, 'signin.html', context)


def logoutt(request):
    logout(request)
    messages.success(request, 'you have successfully logout')
    return redirect('signin')

#Authentication done


#changepassword
@login_required(login_url='signin')
def password_update(request):
    load_profile = Profile.objects.get(user__username=request.user.username)
    form = PasswordChangeForm(request.user)
    if request.method == 'POST':
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)
            messages.success(request, 'Your password has been updated successfully✅✅✅')
            return redirect('user_profile')
        else:
            messages.error(request, form.errors)
            return redirect('password-update')
               
    
    context = {
        'load_profile':load_profile,
        'form':form
    }
    return render(request, 'password_update.html', context)
#changepassword done