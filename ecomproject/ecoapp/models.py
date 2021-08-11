from django.db import models
from django.contrib.auth.models import User
from django.forms import ModelForm
from django.conf import settings


# Create your models here.
class Admin(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    full_name = models.CharField(max_length=50)
    image = models.ImageField(upload_to="admins")
    mobile  = models.CharField(max_length=20)

    def __str__(self):
        return self.user.username




class Customer(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)#onetoone give the object name directly
    
    full_name = models.CharField(max_length=200)
    address = models.CharField(max_length=200, null=True, blank=True)
    joined_on = models.DateTimeField(auto_now_add=True)


    def __str__(self):
        return self.full_name








class Category(models.Model):
    title = models.CharField(max_length=200)
    slug = models.SlugField(unique=True)




    @staticmethod
    def get_all_categories():
        return Category.objects.all()
   




    def __str__(self):
        return self.title


class Product(models.Model):
    title = models.CharField(max_length=200)
    slug = models.SlugField(unique=True)
    image = models.ImageField(upload_to="products")
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    marked_price = models.PositiveIntegerField()
    selling_price = models.PositiveIntegerField()
    description = models.TextField()
    
    
    warranty = models.CharField(max_length=300,null=True , blank=True)
    warranty_policy = models.CharField(max_length=300,null=True , blank=True)
    view_count = models.PositiveIntegerField(default=0)
    users_wishlist = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name="user_wishlist", blank=True)

    @staticmethod
    def get_all_products():
        return Product.objects.all()

    @staticmethod
    def get_all_products_by_categoryid(category_id):
        if category_id:
            return Product.objects.filter(category = category_id)
        
        else:
            return Product.get_all_products()
    


    def __str__(self):
        return self.title

class ProductImage(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    image = models.ImageField(upload_to = "products/images/")
    
    def __str__(self):
        return self.product.title




class Cart(models.Model):
    customer = models.ForeignKey(Customer,on_delete=models.SET_NULL, null=True, blank=True)
    total = models.PositiveIntegerField(default=0)
    created_at = models.DateTimeField(auto_now=True)


    def __str__(self):
        return "Cart:" + str(self.id)






class CartProduct(models.Model):
    cart = models.ForeignKey(Cart,on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField()
    subtotal = models.PositiveIntegerField()
    rate = models.PositiveIntegerField()

    def __str__(self):
        return "Cart:" + str(self.cart.id) + "CartProduct:" +str(self.id)

ORDER_STATUS = (
    ("Order Received", "Order Received"),# this is one of the property given by the django and first is stored in database and another is shon in the form
    ("Order Processing", "Order Processing"),
    ("On the Way", "on the way"),
    ("Order Completed", "Order Completed"),
    ("Order Canceled", "Order Canceled"),
)
METHOD = (
    ("Cash On Delivery","Cash On Delivery"),
    ("Khalti Payment","Khalti Payment"),

)

class Order(models.Model):
    
    cart= models.OneToOneField(Cart, on_delete=models.CASCADE)
    order_by = models.CharField(max_length=200)
    shipping_address = models.CharField(max_length=200)
    mobile = models.CharField(max_length=10)
    email = models.EmailField(null = True, blank=True)
    subtotal = models.PositiveIntegerField()
    discount = models.PositiveIntegerField()
    total = models.PositiveIntegerField()
    order_status = models.CharField(max_length=50, choices = ORDER_STATUS, default="Order Received")
    created_at = models.DateTimeField(auto_now=True)
    payment_method = models.CharField(max_length=20, choices = METHOD, default="Cash On Delivery")
    payment_completed = models.BooleanField(default = False, null= True, blank=True)
    def __str__(self):
        return "Order:" + str(self.id)


class Wish(models.Model):
    customer = models.ForeignKey(Customer,on_delete=models.SET_NULL, null=True, blank=True)
    email = models.ForeignKey(Order, on_delete=models.CASCADE, null=True, blank=True)
    total = models.PositiveIntegerField(default=0)
    created_at = models.DateTimeField(auto_now=True)


    def __str__(self):
        return "Wish:" + str(self.id)

class WishProduct(models.Model):
    wish = models.ForeignKey(Wish,on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField()
    subtotal = models.PositiveIntegerField()
    rate = models.PositiveIntegerField() 

    def __str__(self):
        return "Wish:" + str(self.wish.id) + "WishProduct:" +str(self.id)
    
   













class Comment(models.Model):
    STATUS = (
        ('New','New'),
        ('True','True'),
        ('False','False'),
    )
    product=models.ForeignKey(Product, related_name="comments",on_delete=models.CASCADE)
 
    user=models.ForeignKey(User, on_delete=models.CASCADE)
    
    subject = models.CharField(max_length=50, blank=True)
    comment = models.CharField(max_length=250, blank=True)
    rate = models.IntegerField(default=1)
    ip = models.CharField(max_length=20, blank=True)
    status = models.CharField(max_length=10, choices=STATUS,default='New')
    create_at = models.DateTimeField(auto_now=True)
    update_at = models.DateTimeField(auto_now=True) 

    def __str__(self):
        return 'Comment {} by {}'.format(self.comment, self.user)



  


class CommentForm(ModelForm):
    class Meta:
        model = Comment
        fields = ['subject', 'comment', 'rate']
        
class Contact(models.Model):
    identity = models.CharField(max_length=50, blank=True)
    email = models.EmailField()
    number = models.PositiveIntegerField()
    message = models.TextField()


    def __str__(self):
        return self.identity

class ContactForm(ModelForm):
    class Meta:
        model = Contact
        fields = ['identity', 'email', 'number','message']