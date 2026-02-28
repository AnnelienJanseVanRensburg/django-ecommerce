from rest_framework import serializers
from .models import Store, Product, Review


class StoreSerializer(serializers.ModelSerializer):
    """Translate Store objects into JSON and back."""

    class Meta:
        model = Store
        fields = ['id', 'owner', 'name', 'description']
        # 'id' is included so the API user knows which store is which
        # 'owner' is the vendor's user ID


class ProductSerializer(serializers.ModelSerializer):
    """Translate Product objects into JSON and back."""

    class Meta:
        model = Product
        fields = [
            'id', 'store', 'name',
            'description', 'price', 'stock'
        ]


class ReviewSerializer(serializers.ModelSerializer):
    """Translate Review objects into JSON and back."""

    class Meta:
        model = Review
        fields = [
            'id', 'product', 'reviewer',
            'rating', 'comment', 'is_verified', 'created_at'
        ]
        # read_only_fields means the API user can't manually set these
        read_only_fields = ['reviewer', 'is_verified', 'created_at']
