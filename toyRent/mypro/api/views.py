from django.shortcuts import render
from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.contrib.auth.models import User
from client.models import Subcategory
from .serializer import UserSerializer,SubcategorySerializer
from rest_framework import viewsets,mixins

# Create your views here.
@api_view(['GET'])
def view(request):
    Users = User.objects.all()
    serializer = UserSerializer(Users, many = True)
    return Response(serializer.data)

class YourModelViewSet(mixins.ListModelMixin,
                       mixins.CreateModelMixin,
                       mixins.UpdateModelMixin,
                       viewsets.GenericViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    
@api_view(['POST','GET'])
def update(request):
    if request.method=='POST':
        data = request.data
        username = data['username']
        password = data['password']
        user = User.objects.create(username=username,password=password)
        print("user printed:",user.id)
        serializer = UserSerializer(user,many=False)
        return Response(serializer.data)

    elif request.method=='GET':
        Users = User.objects.all()
        serializer = UserSerializer(Users, many = True)
        return Response(serializer.data)
    
        
@api_view(['GET'])
def subcategories(request):
    subcategories = Subcategory.objects.all()
    serializer = SubcategorySerializer(subcategories,many = True)
    return Response(serializer.data)