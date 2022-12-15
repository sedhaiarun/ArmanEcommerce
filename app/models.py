from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MaxValueValidator, MinValueValidator

# Create your models here.
STATE_CHOICES =(
    ('Province 1','Province 1'),
    ('Bagmati ', 'Bagmati'),
    ('Gandaki','Gandaki'),
    ('Lumbini','Lumbini'),
    ('Madhesh','Madhesh'),
    ('Karnali','Karnali'),
    ('Sudur Pashchim','Sudur Paschim')

)

CATEGORY_CHOICES=(
    ('M','Mobile'),
    ('L','Laptop'),
    ('TW','Top Wear'),
    ('BW','Buttom Wear')
)

STATUS_CHOICES=(
    ('Accepted','Accepted'),
    ('Packed','Packed'),
    ('On The Way','On The Way'),
    ('Delivered','Delivered'),
    ('Cancel','Cancel')
)

class Customer(models.Model):
    user=models.ForeignKey(User, on_delete= models.CASCADE)
    name=models.CharField(max_length=200)
    locality=models.CharField(max_length=100)
    city=models.CharField(max_length=200)
    zipcode=models.IntegerField()
    state=models.CharField(choices=STATE_CHOICES, max_length=100)

    def __str__(self):
        return str(self.id)

    @property
    def completeAddress(self):
        address=(self.locality) +','+ (self.city)
        return address
   
class Product(models.Model):
    title=models.CharField(max_length=100)
    selling_price=models.FloatField()
    discount_price=models.FloatField()
    description=models.TextField()
    brand=models.CharField(max_length=100)
    category=models.CharField(choices=CATEGORY_CHOICES, max_length=2)
    product_image=models.ImageField(upload_to='productimg')
    
    def __str__(self):
        return str(self.id)
    @property
    def beforediscount(self):
        total=self.selling_price + self.discount_price
        return total
    def get_cart_items(self):
        cart=self.cart_set.all()
        total=sum([item.quantity for item in cart])
        return total

class Cart(models.Model):
    user=models.ForeignKey(User, on_delete=models.CASCADE)
    product=models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity=models.IntegerField(default=0, null=True, blank=True)

    def __str__(self):
        return str(self.id)
    
    @property
    def cartTotal(self):
       total= self.product.selling_price* self.quantity
       return total

class Orderplaced(models.Model):
    user=models.ForeignKey(User, on_delete=models.CASCADE,null=True)
    customer=models.ForeignKey(Customer, on_delete=models.CASCADE,null=True)
    product=models.ForeignKey(Product, on_delete=models.CASCADE, null=True)
    quantity=models.PositiveBigIntegerField(default=1)
    
    ordered_date= models.DateTimeField(auto_now_add=True )
    status=models.CharField(choices=STATUS_CHOICES,default='pending' , max_length=50)

    


    
     

     
     
    
    
