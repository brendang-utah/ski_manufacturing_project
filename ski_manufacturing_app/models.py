from django.db import models

# Create your models here.

class User(models.Model):
    username = models.CharField(max_length=150, unique=True)
    password = models.CharField(max_length=255)
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    phone_number = models.CharField(max_length=20, blank=True, null=True)
    address = models.TextField(blank=True, null=True)
    role = models.CharField(max_length=50)

    def __str__(self):
        return self.username

class Employee(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    position = models.CharField(max_length=100)
    training_status = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.user.first_name} {self.user.last_name} - {self.position}"

class Customer(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    order_history = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.user.username

class Product(models.Model):
    name = models.CharField(max_length=200)
    description = models.TextField(blank=True, null=True)
    makeup = models.TextField(blank=True, null=True)
    size = models.CharField(max_length=50)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    stock_status = models.IntegerField()
    imagepath = models.ImageField(upload_to="product_images/", blank=True, null=True)

    def __str__(self):
        return self.name

class RawMaterial(models.Model):
    type = models.CharField(max_length=200)
    quantity_available = models.IntegerField()

    def __str__(self):
        return self.type

class Payment(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    payment_method = models.CharField(max_length=50)
    payment_details = models.TextField()
    exp_date = models.DateField()
    status = models.CharField(max_length=50)

    def __str__(self):
        return f"Payment {self.id} - {self.status}"

class Order(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    payment = models.ForeignKey(Payment, on_delete=models.CASCADE)
    status = models.CharField(max_length=50)
    date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Order {self.id} - {self.status}"

class OrderLine(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.IntegerField()
    unit_price = models.DecimalField(max_digits=10, decimal_places=2)
    total_price = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"OrderLine {self.id} - {self.product.name}"

class Report(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    employee = models.ForeignKey(Employee, on_delete=models.CASCADE)
    date_range = models.CharField(max_length=100)
    total_net_sales = models.DecimalField(max_digits=12, decimal_places=2)

    def __str__(self):
        return f"Report {self.id} - {self.date_range}"

class Return(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    reason = models.TextField()

    def __str__(self):
        return f"Return {self.id} - {self.reason}"

