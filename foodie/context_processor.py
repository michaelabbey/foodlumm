from shopcart.models import Shopcart
from foodie.models import Variety


def dropdown(request):
    varieties = Variety.objects.all()
    
    context = {
    'varieties':varieties
    }
    return context

#this is the numbers that shows the item added to your cart
def cartread(request):
    cart = Shopcart.objects.filter(user__username=request.user.username, item_paid=False)
    cartcount = 0
    for item in cart:
        cartcount += item.quantity  
    
    context = {
        'cartcount':cartcount,
    }
    return context