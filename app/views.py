from django.shortcuts import render,redirect
from django.http import JsonResponse
import json
from .models import Product,Customer,Cart,Orderplaced
from django.views import View
from .forms import CustomerRegistrationForm, CustomerProfileForm
from django.contrib import messages
from django.db.models import Q

def home(request):
 slider=Product.objects.raw("SELECT * FROM app_product ORDER BY id DESC LIMIT 0,3") 
 for i in slider:
  print (i.title)
 bottomwears=Product.objects.filter(category='BW')
 topwear=Product.objects.filter(category='M')
 laptop=Product.objects.filter(category='L')
  
 if request.user.is_authenticated:
   
  product=Product.objects.all()
  cart=Cart.objects.filter(user=request.user)
  total=70
  cartItems=0
  for i in cart:
     total+=i.cartTotal
     cartItems+=i.quantity
  return render(request, 'app/home.html', {'bottomwears':bottomwears,'topwear':topwear,'laptop':laptop,'slider':slider,'cartItems':cartItems})

 else: 
    

 
  
#  context={'bottomwears':bottomwears}
  
   return render(request, 'app/home.html', {'bottomwears':bottomwears,'topwear':topwear,'laptop':laptop,'slider':slider, })

def product_detail(request,pk):

    productdetail=Product.objects.get(id=pk)
    # beforediscount=Product.beforediscount
    # print(beforediscount)
    if request.user.is_authenticated:
   
      product=Product.objects.all()
      cart=Cart.objects.filter(user=request.user)
      total=70
      cartItems=0
      for i in cart:
        total+=i.cartTotal
        cartItems+=i.quantity
       
      return render(request, 'app/productdetail.html',{'productdetail':productdetail,'cartItems':cartItems})
    else: 
       cartItems={}

    

       return render(request, 'app/productdetail.html',{'productdetail':productdetail,'cartItems':cartItems})

def add_to_cart(request):
    data= json.loads(request.body)
    productId=data['productId']
    action=data['action']
    print('this is action',action)
    usr=request.user
    product=Product.objects.get(id=productId)
    cart, created= Cart.objects.get_or_create(product=product, user=usr)
     
     
    if action== 'add':
        print('yasma aayo')
        cart.quantity=(cart.quantity +1)
        print(cart.quantity)
        
       
    elif action=='remove':
        cart.quantity=(cart.quantity - 1)
    cart.save()
    if action=='delete' or cart.quantity<=0:
      cart.delete()
       
     
    return JsonResponse('Item was added',safe=False)
    
    # return render(request, 'app/addtocart.html',{'product':product})

def cart(request):
  product=Product.objects.all()
  cart=Cart.objects.filter(user=request.user)
  total=70
  cartItems=0
  for i in cart:
     total+=i.cartTotal
     cartItems+=i.quantity
  print(cartItems)
    
     
   
  # for i in cart:
  #   print(cart.cartTotal)

  
   
  return render(request, 'app/addtocart.html',{'cart':cart,'total':total,'cartItems':cartItems})

def minus_cart(request):
  if request.method == 'GET':
   prod_id =request.GET['prod_id']
   product=Product.objects.get(id=prod_id)
   c, created= Cart.objects.get_or_create(product=product, user=request.user)
   c.quantity-=1
   c.save()
   product=Product.objects.all()
   cart=Cart.objects.filter(user=request.user)
   total=70
   cartItems=0
   for i in cart:
     total+=i.cartTotal
     cartItems+=i.quantity
  data ={
  'quantity': c.quantity,
  'amount':total,
  'carttotal': c.cartTotal
  }
  return JsonResponse(data)

def remove_cart(request):
  if request.method=="GET":
    prod_id=request.GET['prod_id']
    product=Product.objects.get(id=prod_id)
    c=Cart.objects.get(product=product, user=request.user)
    print('aakoxa')
     
    c.delete()
    total=0
    carttotal=0
    

    data={
       
       'amount': total,
       'carttotal':carttotal
    }
    return JsonResponse(data)

def buy_now(request):
 return render(request, 'app/buynow.html')

def profile(request):
 return render(request, 'app/profile.html')

def address(request):
  usr=request.user
  add=Customer.objects.filter(user=usr)
  for i in add:
    print(i.name)
    print(i.locality)
   
  return render(request, 'app/address.html',{'add':add})

def laptop(request, data=None):
  laptop=Product.objects.filter(category='L')
  if data==None:
    laptop=Product.objects.filter(category='L')
  elif data=='DELL' or data=='APPLE' or data=='ACER' or data=='HP':
    laptop=Product.objects.filter(Q(category='L') & Q(brand=data))

  return render(request,'app/laptop.html',{'mobile':laptop})

def mobile(request,data=None):
  mobile=Product.objects.filter(category='M')
  if data==None:
     mobile = Product.objects.filter(category='M')
  elif data=='MI' or data=='Vivo' or data=='apple' or  data=='Nokia' or data=='Android':
    
     mobile = Product.objects.filter(category='M').filter(brand=data)
  
  elif data=='below':
     mobile= Product.objects.filter(category='M').filter(selling_price__lt=50000)
  elif data=='above':
     mobile=Product.objects.filter(category='M').filter(selling_price__gte=50000)
  return render(request, 'app/mobile.html',{'mobile':mobile})

def login(request):
 return render(request, 'app/login.html')

# def customerregistration(request):
#  return render(request, 'app/customerregistration.html')
class CustomerRegistrationView(View):
  def get(self, request):
    form=CustomerRegistrationForm()
    return render(request,'app/customerregistration.html',{'form':form})
  def post(self, request):
    form=CustomerRegistrationForm(request.POST)
    if form.is_valid():
      form.save()
      messages.success(request, 'COngratulations User Registered successfully')
    return render(request,'app/customerregistration.html',{'form':form})
    

class ProfileView(View):
  def get(self, request):
    form=CustomerProfileForm()
    return render(request,'app/profile.html',{'form':form})

  def post(self, request):
    
    form=CustomerProfileForm(request.POST)
    if form.is_valid():
      usr=request.user
      customers=Customer.objects.filter(user=usr).count()
      if customers<=2:
        print (customers)
      
        name=form.cleaned_data['name']
        locality=form.cleaned_data['locality']
        city=form.cleaned_data['city']
        state=form.cleaned_data['state']
        zipcode=form.cleaned_data['zipcode']
        print(usr,name,locality,city)
        reg=Customer(user=usr,name=name,locality=locality,city=city,
        state=state,zipcode=zipcode)

        reg.save()
        messages.success(request, 'COngratulations User Profile successfully added')
        return render(request,'app/profile.html',{'form':form})
      messages.warning(request, 'Cannot add Already consists 2 profile ')
      return render(request,'app/profile.html',{'form':form})

def checkout(request):
  usr=request.user
  customer=Customer.objects.filter(user=usr)
  customer=Customer.objects.filter(user=usr)
  cart=Cart.objects.filter(user=usr)

  
  
   
  total=70
  cartItems=0
  for i in cart:
     total+=i.cartTotal
     cartItems+=i.quantity
  return render(request, 'app/checkout.html',{'cart':cart,'total':total,'customer':customer,'cartItems':cartItems })

def payment_done(request):
  usr=request.user
  cust_id=request.GET.get('custid')
  customer=Customer.objects.get(user=usr, id=cust_id)
  cart=Cart.objects.filter(user=usr)
  for i in cart:
     
  
   orderplaced=Orderplaced.objects.create(user=usr, customer=customer,product=i.product,
   quantity=i.quantity
   )
   orderplaced.save()
   cart.delete()
   
   
  return redirect('orders')
   
def orders(request):
  user=request.user
  cart=Cart.objects.filter(user=user)
  cartItems=0
  for i in cart:
   total+=i.cartTotal
   cartItems+=i.quantity
  
  orderplaced=Orderplaced.objects.filter(user=user)
  
  messages.success(request, 'Cannot add Already consists 2 profile ')
  return render(request,'app/orders.html',{'op':orderplaced,'cartItems':cartItems})



 
  

   
