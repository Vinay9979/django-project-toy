from rest_framework.serializers import ModelSerializer
from django.contrib.auth.models import User
from client.models import Subcategory

class UserSerializer(ModelSerializer):
    class Meta:
        model = User
        exclude = ['password']
        # fields = '__all__'

class SubcategorySerializer(ModelSerializer):
    class Meta:
        model = Subcategory
        fields = '__all__'
        depth = 1