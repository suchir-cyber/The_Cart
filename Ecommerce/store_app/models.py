from django.db import models
from django.utils import timezone
from ckeditor.fields import RichTextField
from django.contrib.auth.models import User

# Create your models here.
class Categories(models.Model):
    name = models.CharField(max_length=200)

    def __str__(self):
        return self.name

class Brand(models.Model):
    name = models.CharField(max_length=200)

    def __str__(self):
        return self.name


class Color(models.Model):
    name = models.CharField(max_length=200)
    code = models.CharField(max_length=50)
    
    def __str__(self):
        return self.name

class Filter_Price(models.Model):
    FILTER_PRICE = (
        ('1000 TO 10000','1000 TO 10000'),
        ('10000 TO 20000','10000 TO 20000'),
        ('20000 TO 30000','20000 TO 30000'),
        ('30000 TO 40000','30000 TO 40000'),
        ('40000 TO 50000','40000 TO 50000')
    )    
    price = models.CharField(choices=FILTER_PRICE,max_length=60)    

    def __str__(self):
        return self.price


class Product(models.Model):
    CONDITION = (
        ('New' , 'New'),
        ('Old' , 'Old  ')
    )
    STOCK = (
        ('IN STOCK' , 'IN STOCK'),
        ('OUT OF STOCK' , 'OUT OF STOCK')
    )
    STATUS = (
        ('PUBLISH','PUBLISH'),
        ('DRAFT','DRAFT')
    )
    unique_id = models.CharField(unique=True,max_length=200,null=True,blank=True)
    image = models.ImageField(upload_to='Product_images/img')
    name = models.CharField(max_length=200)
    price = models.IntegerField()
    condition = models.CharField(choices=CONDITION,max_length=100)
    information = RichTextField(null=True)
    description = RichTextField(null=True)
    stock = models.CharField(choices=STOCK,max_length=100)
    status = models.CharField(choices=STATUS,max_length=100)
    created_date = models.DateTimeField(default=timezone.now)


    Categories = models.ForeignKey(Categories,on_delete=models.CASCADE)
    brand = models.ForeignKey(Brand,on_delete=models.CASCADE)
    color = models.ForeignKey(Color,on_delete=models.CASCADE)
    filter_price = models.ForeignKey(Filter_Price,on_delete=models.CASCADE, null=True, blank=True)


    def save(self, *args, **kwargs):
        # Check if the instance is being created for the first time
        if not self.pk:
            super().save(*args, **kwargs)  # Save to generate the ID
            # Generate unique_id using created_date and the generated ID
            self.unique_id = self.created_date.strftime('75%Y%m%d23') + str(self.id)
            # Update the instance with the unique_id
            kwargs['force_insert'] = False  # Avoid inserting again, just update
        super().save(*args, **kwargs)  # Save again with the updated unique_id
 
    
    def __str__(self):
        return self.name
    


class Images(models.Model):
    image = models.ImageField(upload_to='Product_images/img')
    product = models.ForeignKey(Product,on_delete=models.CASCADE)


class Tag(models.Model):
    name = models.CharField(max_length=200)
    product = models.ForeignKey(Product,on_delete=models.CASCADE)     


class Contact_Us(models.Model):
    name = models.CharField(max_length=200)
    email = models.EmailField(max_length=200)
    subject = models.CharField(max_length=200)
    message = models.TextField()       
    date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.email
    

class Order(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    firstname = models.CharField(max_length=100)
    lastname = models.CharField(max_length=100)
    country = models.CharField(max_length=100)
    address = models.TextField()
    city = models.CharField(max_length=100)
    state = models.CharField(max_length=100)
    postcode = models.IntegerField()
    phone = models.IntegerField()
    email = models.EmailField(max_length=100)
    amount = models.CharField(max_length=100)
    payment_id = models.CharField(max_length=300,null=True,blank=True)
    paid = models.BooleanField(default=False,null=True)
    date = models.DateField(auto_now_add=True)


    def __str__(self):
        return self.user.username
    

class OrderItem(models.Model):
    order = models.ForeignKey(Order,on_delete=models.CASCADE)
    product = models.CharField(max_length=200)
    image = models.ImageField(upload_to='Product_images/Order_Img')
    quantity = models.CharField(max_length=20)
    price = models.CharField(max_length=100)
    total = models.CharField(max_length=100)


    def __str__(self):
        return self.order.user.username