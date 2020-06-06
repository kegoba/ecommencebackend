from django.db import models
#'max_digits'
#decimal_places
# Create your models here.
class UserProfile (models.Model):
    user_id = models.AutoField(primary_key=True)
    name = models.CharField("name", max_length=50)
    password = models.CharField("password", max_length=30)
    email = models.EmailField("email", max_length=30, unique = True)
    wallet = models.DecimalField("wallet", max_digits=10, null=True, decimal_places=2)
    phone = models.CharField("phone number", null=True,  max_length=15)
    date_joined = models.DateTimeField("date join", auto_now_add=True)


class Transaction(models.Model):
    id  = models.AutoField(primary_key=True)
    orders = models.CharField("orders",null=True, max_length=100)
    pending = models.CharField("pending orders", max_length=100)
    user_id = models.ForeignKey(UserProfile, null=True, related_name="transaction_id", on_delete=models.CASCADE)

class Order(models.Model):
    id = models.AutoField(primary_key=True)
    item_order = models.CharField("Cart Item", null=True,  max_length=1000)
    date_order = models.DateTimeField("date join", auto_now_add=True)
    total_price = models.DecimalField("price of product", max_digits=10, null=True, decimal_places=2)
    user_id = models.ForeignKey(UserProfile, null=True, related_name="order_id", on_delete=models.CASCADE)

class Cart(models.Model):
    id = models.AutoField(primary_key=True)
    item = models.CharField("Cart Item", null=True,  max_length=1000)
    user_id = models.ForeignKey(UserProfile, null=True, related_name="cart_id", on_delete=models.CASCADE)



class Product (models.Model):
    product_id = models.AutoField(primary_key=True)
    product_price = models.DecimalField("price of product", max_digits=10, null=True, decimal_places=2)
    product_category = models.CharField("list of Catergories", null=True, max_length=100) #product_category
    image = models.ImageField("image", upload_to='post_images' , null=True)
    product_desc = models.CharField("product description", null=True, max_length=100)




class Vtu_transaction(models.Model):
    id  = models.AutoField(primary_key=True)
    transaction_type = models.CharField("transaction type",null=True, max_length=100)
    amount = models.DecimalField("amout", max_digits=10, null=True, decimal_places=2)
    ref_id = models.CharField("reference number s", max_length=100)
    phone = models.CharField("phone number credited", max_length=100)
    user_id = models.ForeignKey(UserProfile, null=True, related_name="vtu_id", on_delete=models.CASCADE)






