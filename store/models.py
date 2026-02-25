from django.db import models
from django.contrib.auth.models import User


class Store(models.Model):
    """Represent a vendor's store."""
    owner = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
    )
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        """Return a string representation of the Store."""
        return self.name


class Product(models.Model):
    """Represent a product listed in a store."""
    store = models.ForeignKey(
        Store,
        on_delete=models.CASCADE,
    )
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    stock = models.PositiveIntegerField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        """Return a string representation of the Product."""
        return self.name

    def is_in_stock(self):
        """Return True if the product has stock available."""
        return self.stock > 0


class Order(models.Model):
    """Represent a completed purchase by a buyer."""
    buyer = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
    )
    created_at = models.DateTimeField(auto_now_add=True)
    total_price = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        default=0,
    )

    def __str__(self):
        """Return a string representation of the Order."""
        return f"Order #{self.id} by {self.buyer.username}"

    def calculate_total(self):
        """Calculate and save the total price from all order items."""
        total = sum(item.get_subtotal() for item in self.orderitem_set.all())
        self.total_price = total
        self.save()


class OrderItem(models.Model):
    """Represent a single product line within an order."""
    order = models.ForeignKey(
        Order,
        on_delete=models.CASCADE,
    )
    product = models.ForeignKey(
        Product,
        on_delete=models.CASCADE,
    )
    quantity = models.PositiveIntegerField()
    price_at_purchase = models.DecimalField(
        max_digits=10,
        decimal_places=2,
    )

    def __str__(self):
        """Return a string representation of the OrderItem."""
        return f"{self.quantity} x {self.product.name}"

    def get_subtotal(self):
        """Return the subtotal for this line item."""
        return self.quantity * self.price_at_purchase


class Review(models.Model):
    """Represent a buyer's review of a product."""
    product = models.ForeignKey(
        Product,
        on_delete=models.CASCADE,
    )
    reviewer = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
    )
    rating = models.PositiveSmallIntegerField()
    comment = models.TextField()
    is_verified = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        """Return a string representation of the Review."""
        return f"Review by {self.reviewer.username} on {self.product.name}"

    def set_verified_status(self, status):
        """Set whether the review is verified and save the change."""
        self.is_verified = status
        self.save()
