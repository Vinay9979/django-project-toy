from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from datetime import datetime

# Create your models here.
class Category(models.Model):
    categoryName = models.CharField(max_length=200)
    createDate = models.DateTimeField(auto_now_add=True,editable=False)
    lastModifiedDate = models.DateTimeField(auto_now=True)

    

class Subcategory(models.Model):
    subcategoryName = models.CharField(max_length=200)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    createDate = models.DateTimeField(auto_now_add=True,editable=False)
    lastModifiedDate = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.subcategoryName
    
class Store(models.Model):
    storeName = models.CharField(max_length=100)
    ownerName = models.CharField(max_length=100)
    email = models.EmailField(max_length=254)
    address = models.CharField(max_length=1000)
    website = models.CharField(max_length=250)

    def __str__(self):
        return self.storeName


class Manufacturer(models.Model):
    manufacturerName = models.CharField(max_length=100)
    owner = models.CharField(max_length=100)
    email = models.EmailField(max_length=250)
    address = models.CharField(max_length=1000)
    website = models.CharField(max_length=250)

    def __str__(self):
        return self.manufacturerName


class Toy(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    purchasePrice = models.DecimalField(max_digits=10, decimal_places=2)
    rentPrice = models.DecimalField(max_digits=10, decimal_places=2)
    storeId = models.ForeignKey(Store, on_delete=models.CASCADE,null=True)
    categoryId = models.ForeignKey(Category, on_delete=models.CASCADE)
    subcategoryId = models.ForeignKey(Subcategory, on_delete=models.CASCADE)
    stockQuantity = models.PositiveIntegerField()
    manufacturerId = models.ForeignKey(Manufacturer, on_delete=models.CASCADE)
    img_url = models.URLField()
    created_date = models.DateTimeField(auto_now_add=True,editable=False)
    modified_date = models.DateTimeField(auto_now=True)
    isPurchasable = models.BooleanField(default=True)
    isRentable = models.BooleanField(default=True)

    def __str__(self):
        return self.name 
    
# class Userdetails(models.Model):
#     address = models.CharField(max_length=500)
#     phone = models.BigIntegerField()
#     userId = models.ForeignKey(User,on_delete=models.CASCADE)
    
#     def __str__(self):
#         return self.phone
    

    
class Billingaddress(models.Model):
    uId = models.ForeignKey(User,on_delete=models.CASCADE)
    firstName = models.CharField(max_length=100)
    lastName = models.CharField(max_length=100)
    email = models.EmailField(max_length=200)
    mobile = models.PositiveBigIntegerField()
    address = models.CharField(max_length=1000)

class Deliveryaddress(models.Model):
    uId = models.ForeignKey(User,on_delete=models.CASCADE)
    firstName = models.CharField(max_length=100)
    lastName = models.CharField(max_length=100)
    email = models.EmailField(max_length=200)
    mobile = models.PositiveBigIntegerField()
    address = models.CharField(max_length=1000)

class Cart(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    product = models.ForeignKey(Toy,on_delete=models.CASCADE)
    quantity=models.IntegerField(default=1)

    def __str__(self):
        return f"{self.product}"

class Order(models.Model):
    STATUS_CHOICES = [
        ('P', 'Pending'),
        ('C', 'Completed'),
        ('F', 'Failed'),
        ('R','Refunded')
    ]
    delivery_choices=[
        ('P','Pending'),
        ('D','Delivered'),
        ('OD','Out for delivery'),
        ('R','Returned')
    ]

    customer = models.ForeignKey(User, on_delete=models.CASCADE)
    order_date = models.DateTimeField(auto_now_add=True)
    payment_status = models.CharField(max_length=1, choices=STATUS_CHOICES, default='P')
    delivery_status = models.CharField(max_length=2,choices=delivery_choices,default='P')
    total_amount = models.DecimalField(max_digits=10, decimal_places=2)
    orderId  = models.BigIntegerField(default=1)

    def __str__(self):
        return f"Order {self.id} by {self.customer.username}"
    

class OrderDetails(models.Model):
    toyid = models.ForeignKey(Toy, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField()
    itemprice = models.DecimalField(max_digits=10, decimal_places=2)
    subtotal = models.DecimalField(max_digits=10, decimal_places=2)
    orderDate = models.DateTimeField(auto_now_add=True)
    orderid = models.ForeignKey(Order,on_delete=models.CASCADE,blank=True)
    def save(self, *args, **kwargs):
        # Calculate subtotal based on quantity and item price
        self.subtotal = self.quantity * self.itemprice
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.toyid} - {self.quantity}"
    
    

class Review(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    rating = models.IntegerField()
    review = models.CharField(max_length=1000)

    class Meta:
        db_table = 'review'

class Contact(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    subject = models.CharField(max_length=100)
    message = models.CharField(max_length=1000)
    read = models.BooleanField(default=False)

    class Meta:
        db_table='contact'







        
