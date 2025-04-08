from django.db import models
from authuser.models import User

class Modification(models.Model):
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name="created_%(class)s")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name="updated_%(class)s")
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True  # 👈 Abstract class to prevent table creation



class Snacks(Modification):
    name = models.CharField(max_length=100, unique=True)

    def save(self, *args, **kwargs):
        self.name = self.name.upper()
        super().save(*args, **kwargs)

    class Meta:
        db_table = "snacks_table"

    def __str__(self):
        return self.name

class SnacksItem(Modification):
    category = models.ForeignKey(Snacks, on_delete=models.CASCADE, related_name="SnacksItem")
    name = models.CharField(max_length=200)
    image = models.FileField(upload_to='snacks_img/%Y/%m/%d/',blank=True)

    def save(self, *args, **kwargs):
        self.name = self.name.upper()
        super().save(*args, **kwargs)

    class Meta:
        db_table = "snacks_item_table"

    def __str__(self):
        return f"{self.name} ({self.category.name})"



class Order(Modification):
    status = models.BooleanField(default=False)

    class Meta:
        db_table = "order_table"

    def __str__(self):
        return f"Order {self.id} - {self.created_at.strftime('%Y-%m-%d %H:%M:%S')}"


class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name="order_items")
    order_type = models.CharField(max_length=200,null=True,blank=True)
    order_item = models.CharField(max_length=200)
    qty = models.CharField(max_length=200)

    class Meta:
        db_table = "order_item_table"

    def __str__(self):
        return f"OrderItem {self.id} (Order {self.order.id})"
