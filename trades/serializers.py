# trades/serializers.py
from rest_framework import serializers
from .models import Stock

class StockSerializer(serializers.ModelSerializer):
    class Meta:
        model = Stock
        fields = ['stock_code', 'stock_name', 'stock_price']  # Adjust field names to match your model

# serializers.py
from rest_framework import serializers
from .models import User

class LoginSerializer(serializers.Serializer):
    username = serializers.CharField(max_length=150)
    password = serializers.CharField(write_only=True)

class BalanceSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['balance']


