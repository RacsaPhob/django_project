from .models import category, Menu, ShoppingCart
from rest_framework import  serializers


class MenuSerializer(serializers.ModelSerializer):
    related = serializers.StringRelatedField()

    class Meta:
        model = Menu
        fields = ['name','price','description','related']


