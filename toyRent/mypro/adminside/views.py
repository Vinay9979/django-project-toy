from django.shortcuts import render,redirect,HttpResponse
from django.conf import settings 
from django.contrib.auth.decorators import login_required
from django.contrib import messages,auth
from client.models import *
from django.contrib.auth.models import User
from django.core.files.storage import FileSystemStorage
import os
from django.db.models import F,Q,Case,Value,CharField,When
from .customfunction import SubstringBefore
from django.core.paginator import Paginator
from datetime import datetime
from adminside.models import Categoryphotos 

# Create your views here.

def login(request):
    return render(request,'admin/auth-signin.html')

def checklogin(request):
    username = request.POST.get('username')
    password = request.POST.get('password')
    authuser = auth.authenticate(username=username, password=password)
    print("authuser",authuser)
    if authuser is not None:
        if authuser.is_superuser:
            auth.login(request, authuser)
            return redirect('index')
        else:
            messages.error(request, '*Please check username or password.')
            return redirect('login')
    else:
         messages.error(request, '*Please check username or password.')
         return redirect('login')

@login_required(login_url='/admin/login/')
def logout(request):
    auth.logout(request)
    return redirect('login')

@login_required(login_url='/admin/login/')
def index(request):
    return render(request,'admin/index.html')

@login_required(login_url='/admin/login/')
def addtoy(request):
    category = Category.objects.all()
    subcategory = Subcategory.objects.all()
    store = Store.objects.all()
    manufacturer =  Manufacturer.objects.all()
    context = {
        'categories':category,
        'subcategories':subcategory,
        'stores' :store,
        'manufacturers' : manufacturer
    }
    return render(request,'admin/addtoy.html',context)

@login_required(login_url='/admin/login/')
def storetoy(request):
    toyname  = request.POST.get('toyname')
    toydescription  = request.POST.get('toydiscription')
    afp  = request.POST.get('availableforpurchase')
    purchaseprice  = request.POST.get('purchaseprice')

    afr  = request.POST.get('availableforrent')
    rentprice  = request.POST.get('rentprice')
  
    quantity  = request.POST.get('quantity')
    category  = request.POST.get('category')
    subcategory  = request.POST.get('subcategory')
    store  = request.POST.get('store')
    manufacturer  = request.POST.get('manufacturer')
    if 'toyimage' in request.FILES:
        image = request.FILES['toyimage']
        ext = ['png','jpg','jpeg']
        imgext = image.name.split('.')
        imgext = imgext[-1]
        if imgext in ext:
            location= os.path.join(settings.MEDIA_ROOT,'toys')
            obj = FileSystemStorage(location=location)
            obj.save(image.name,image)
            imgUrl = f'../../media/toys/{image.name}'
            if afp=='True' and afr == 'True':
                if (not purchaseprice or purchaseprice==''):
                    purchaseprice =0
                if (not rentprice or rentprice==''):
                    rentprice =0
                Toy.objects.create(name = toyname,description = toydescription,purchasePrice= purchaseprice,rentPrice=rentprice,storeId_id=store,categoryId_id=category,subcategoryId_id=subcategory,stockQuantity=quantity,manufacturerId_id=manufacturer,img_url=imgUrl,isPurchasable=afp,isRentable = afr)
            elif afp == 'True':
                if (not purchaseprice or purchaseprice==''):
                    purchaseprice =0
                Toy.objects.create(name = toyname,description = toydescription,purchasePrice= purchaseprice,rentPrice=0.00,storeId_id=store,categoryId_id=category,subcategoryId_id=subcategory,stockQuantity=quantity,manufacturerId_id=manufacturer,img_url=imgUrl,isPurchasable=afp,isRentable = afr)
            else:
                if (not rentprice or rentprice==''):
                    rentprice =0
                Toy.objects.create(name = toyname,description = toydescription,purchasePrice= 0.00,rentPrice=rentprice,storeId_id=store,categoryId_id=category,subcategoryId_id=subcategory,stockQuantity=quantity,manufacturerId_id=manufacturer,img_url=imgUrl,isPurchasable=afp,isRentable = afr)
            messages.success(request,'Toy added Successfully')
            return redirect('addtoy')
        else:
            toyname  = request.POST.get('toyname')
            toydescription  = request.POST.get('toydiscription')
            afp  = request.POST.get('availableforpurchase')
            purchaseprice  = request.POST.get('purchaseprice')
            afr  = request.POST.get('availableforrent')
            rentprice  = request.POST.get('rentprice')
            quantity  = request.POST.get('quantity')
            category  = request.POST.get('category')
            subcategory  = request.POST.get('subcategory')
            store  = request.POST.get('store')
            manufacturer  = request.POST.get('manufacturer')
            categories = Category.objects.all()
            subcategories = Subcategory.objects.all()
            stores = Store.objects.all()
            manufacturers =  Manufacturer.objects.all()
            print(afr,afp)
            if afp and afr:
                context = {
                    'toyname':toyname,
                    'toydescription':toydescription,
                    'afp':afp,
                    'pprice':purchaseprice,
                    'afr':afr,
                    'rprice':rentprice,
                    'quantity':quantity,
                    'category':category,
                    'subcategory':subcategory,
                    'store':store,
                    'manufacturer':manufacturer,
                    'categories':categories,
                    'subcategories':subcategories,
                    'stores':stores,
                    'manufacturers':manufacturers
                }
                messages.error(request,f'image extension should be {ext}')
                return render(request,'admin/addtoy.html',context)
            elif afr:
                context = {
                    'toyname':toyname,
                    'toydescription':toydescription,
                    'notafp':True,
                    'pprice':purchaseprice,
                    'afr':afr,
                    'rprice':rentprice,
                    'quantity':quantity,
                    'category':category,
                    'subcategory':subcategory,
                    'store':store,
                    'manufacturer':manufacturer,
                    'categories':categories,
                    'subcategories':subcategories,
                    'stores':stores,
                    'manufacturers':manufacturers
                }
                
                messages.error(request,f'image extension should be {ext}')
                return render(request,'admin/addtoy.html',context)
            elif afp:
                context = {
                    'toyname':toyname,
                    'toydescription':toydescription,
                    'afp':afp,
                    'pprice':purchaseprice,
                    'notafr':True,
                    'rprice':rentprice,
                    'quantity':quantity,
                    'category':category,
                    'subcategory':subcategory,
                    'store':store,
                    'manufacturer':manufacturer,
                    'categories':categories,
                    'subcategories':subcategories,
                    'stores':stores,
                    'manufacturers':manufacturers
                }
                messages.error(request,f'image extension should be {ext}')
                return render(request,'admin/addtoy.html',context)
    else:
        toyname  = request.POST.get('toyname')
        toydescription  = request.POST.get('toydiscription')
        afp  = request.POST.get('availableforpurchase')
        purchaseprice  = request.POST.get('purchaseprice')
        afr  = request.POST.get('availableforrent')
        rentprice  = request.POST.get('rentprice')
        quantity  = request.POST.get('quantity')
        category  = request.POST.get('category')
        subcategory  = request.POST.get('subcategory')
        store  = request.POST.get('store')
        manufacturer  = request.POST.get('manufacturer')
        if afp and afr:
            context = {
                'toyname':toyname,
                'toydescription':toydescription,
                'afp':afp,
                'pprice':purchaseprice,
                'afr':afr,
                'rprice':rentprice,
                'quantity':quantity,
                'category':category,
                'subcategory':subcategory,
                'store':store,
                'manufacturer':manufacturer,
                'categories':categories,
                'subcategories':subcategories,
                'stores':stores,
                'manufacturers':manufacturers
            }
            return render(request,'admin/addtoy.html',context)
        elif afr:
            context = {
                'toyname':toyname,
                'toydescription':toydescription,
                'notafp':True,
                'pprice':purchaseprice,
                'afr':afr,
                'rprice':rentprice,
                'quantity':quantity,
                'category':category,
                'subcategory':subcategory,
                'store':store,
                'manufacturer':manufacturer,
                'categories':categories,
                'subcategories':subcategories,
                'stores':stores,
                'manufacturers':manufacturers
            }
            return render(request,'admin/addtoy.html',context)
        else:
            context = {
                'toyname':toyname,
                'toydescription':toydescription,
                'afp':afp,
                'pprice':purchaseprice,
                'notafr':True,
                'rprice':rentprice,
                'quantity':quantity,
                'category':category,
                'subcategory':subcategory,
                'store':store,
                'manufacturer':manufacturer,
                'categories':categories,
                'subcategories':subcategories,
                'stores':stores,
                'manufacturers':manufacturers
            }
            return render(request,'admin/addtoy.html',context)


@login_required(login_url='/admin/login/')
def showtoys(request):
    toys = Toy.objects.annotate(first_line=SubstringBefore(F('description'))).values('id','name','first_line','img_url')
    paginator = Paginator(toys, 5)
    page_number = request.GET.get('page')
    toys = paginator.get_page(page_number)
    for toy in toys:
        print(toy)
    context={
        'toys':toys
    }
    return render(request,'admin/showtoys.html',context)
@login_required(login_url='/admin/login/')
def searchtoy(request):
    name = request.GET.get('searched_product')
    print("name:",name)
    if name is None:
        return redirect('showtoys')
    if name.lower() =='rentable':
        print("name:",name)
        rentable=True
        toysQuery = Toy.objects.annotate(first_line=SubstringBefore(F('description'))).filter(isRentable=rentable).values('id','name','first_line','img_url')
        paginator = Paginator(toysQuery, 5)
        page_number = request.GET.get('page')
        toys = paginator.get_page(page_number)
        context={
        'toys':toys,
        'searched_product':name
    }
        return render(request,'admin/showtoys.html',context)
    elif  name.lower()=='purchasable':
        purchasable=True
        toysQuery = Toy.objects.annotate(first_line=SubstringBefore(F('description'))).filter(isPurchasable=purchasable).values('id','name','first_line','img_url')
        paginator = Paginator(toysQuery, 5)
        page_number = request.GET.get('page')
        toys = paginator.get_page(page_number)
        context={
        'toys':toys,
        'searched_product':name
    }
        return render(request,'admin/showtoys.html',context)

    elif name.isdigit():
        price = float(name)
        toysQuery = Toy.objects.annotate(first_line=SubstringBefore(F('description'))).filter(Q(purchasePrice=price)| Q(rentPrice=price) ).values('id','name','first_line','img_url')
        paginator = Paginator(toysQuery, 5)
        page_number = request.GET.get('page')
        toys = paginator.get_page(page_number)
        context={
        'toys':toys,
        'searched_product':name
    }
        return render(request,'admin/showtoys.html',context)  
    else:
        toysQuery = Toy.objects.annotate(first_line=SubstringBefore(F('description'))).filter( Q(name__icontains=name)| Q(categoryId__categoryName__icontains=name)).values('id','name','first_line','img_url')
        paginator = Paginator(toysQuery, 5)
        page_number = request.GET.get('page')
        toys = paginator.get_page(page_number)
        print('toys:',toys)
        if toys:
            context={
                'toys':toys,
                'searched_product':name
            }
            return render(request,'admin/showtoys.html',context)
        else:
            context={
                'searched_product':name,
                'msg':'No toy found'
            }
            return render(request,'admin/showtoys.html',context)

@login_required(login_url='/admin/login/')
def deletetoy(request,id):
    toy = Toy.objects.get(pk=id)
    toy.delete()
    return redirect('showtoys')

@login_required(login_url='/admin/login/')
def deleteorder(request,id):
    order = Order.objects.get(pk=id)
    order.delete()
    return redirect('manageorders')

@login_required(login_url='/admin/login/')
def editorder(request,id):
    order = Order.objects.get(pk=id)
    print('orderid=',order.id)
    orderDetails = OrderDetails.objects.filter(orderid = order.id)
    context={
        'order':order,
        'orderdetails':orderDetails
    }
    return render(request,'admin/orderdetails.html',context)

@login_required(login_url='/admin/login/')
def edittoy(request,id):
    toy = Toy.objects.get(pk=id)
    categories = Category.objects.all()
    subcategories = Subcategory.objects.all()
    stores = Store.objects.all()
    manufacturers = Manufacturer.objects.all()
    context={
        'toy':toy,
        'categories':categories,
        'subcategories':subcategories,
        'stores':stores,
        'manufacturers':manufacturers
    }
    return render(request,'admin/edittoy.html',context)

def updatetoy(request,id):
    toyname  = request.POST.get('toyname')
    toydescription  = request.POST.get('toydiscription')
    afp  = request.POST.get('availableforpurchase')
    purchaseprice  = request.POST.get('purchaseprice')

    afr  = request.POST.get('availableforrent')
    rentprice  = request.POST.get('rentprice')
  
    quantity  = request.POST.get('quantity')
    category  = request.POST.get('category')
    subcategory  = request.POST.get('subcategory')
    store  = request.POST.get('store')
    manufacturer  = request.POST.get('manufacturer')
    if 'toyimage' in request.FILES:
        image = request.FILES['toyimage']
        location= os.path.join(settings.MEDIA_ROOT,'toys')
        obj = FileSystemStorage(location=location)
        obj.save(image.name,image)
        imgUrl = f'../../media/toys/{image.name}'
        if afp and afr:
            data={
                'name' : toyname,
                'description' : toydescription,
                'purchasePrice':purchaseprice,
                'rentPrice': rentprice,
                'stockQuantity':quantity,
                'img_url': imgUrl,
                'modified_date':datetime.now(),
                'isPurchasable':afp,
                'isRentable':afr,
                'categoryId_id':category,
                'subcategoryId_id':subcategory,
                'storeId_id':store,
                'manufacturerId_id':manufacturer,
                'modified_date':datetime.now()
            }
            Toy.objects.update_or_create(pk=id,defaults=data)
            messages.success(request,'Toy updated successfully',extra_tags='toyupdated')
            return redirect('showtoys')
        elif afp:
            data={
                    'name' : toyname,
                    'description' : toydescription,
                    'purchasePrice':purchaseprice,
                    'rentPrice': 0.00,
                    'stockQuantity':quantity,
                    'img_rl': imgUrl,
                    'modified_date':datetime.now(),
                    'isPurchasable':afp,
                    'isRentable':afr,
                    'categoryId_id':category,
                    'subcategoryId_id':subcategory,
                    'storeId_id':store,
                    'manufacturerId_id':manufacturer,
                    'modified_date':datetime.now()
                }
            Toy.objects.update_or_create(pk=id,defaults=data)
            messages.success(request,'Toy updated successfully',extra_tags='toyupdated')

            return redirect('showtoys')
        
        else:
              data={
                    'name' : toyname,
                    'description' : toydescription,
                    'purchasePrice':0.00,
                    'rentPrice': rentprice,
                    'stockQuantity':quantity,
                    'img_url': imgUrl,
                    'modified_date':datetime.now(),
                    'isPurchasable':afp,
                    'isRentable':afr,
                    'categoryId_id':category,
                    'subcategoryId_id':subcategory,
                    'storeId_id':store,
                    'manufacturerId_id':manufacturer,
                    'modified_date':datetime.now()
                }
              Toy.objects.update_or_create(pk=id,defaults=data)
              messages.success(request,'Toy updated successfully',extra_tags='toyupdated')

              return redirect('showtoys')
    else:
         if afp and afr:
            data={
                'name' : toyname,
                'description' : toydescription,
                'purchasePrice':purchaseprice,
                'rentPrice': rentprice,
                'stockQuantity':quantity,
                'modified_date':datetime.now(),
                'isPurchasable':afp,
                'isRentable':afr,
                'categoryId_id':category,
                'subcategoryId_id':subcategory,
                'storeId_id':store,
                'manufacturerId_id':manufacturer,
                'modified_date':datetime.now()
            }
            Toy.objects.update_or_create(pk=id,defaults=data)
            messages.success(request,'Toy updated successfully',extra_tags='toyupdated')
            return redirect('showtoys')

         elif afp:
              data={
                'name' : toyname,
                'description' : toydescription,
                'purchasePrice':purchaseprice,
                'rentPrice': 0.00,
                'stockQuantity':quantity,
                'modified_date':datetime.now(),
                'isPurchasable':afp,
                'isRentable':afr,
                'categoryId_id':category,
                'subcategoryId_id':subcategory,
                'storeId_id':store,
                'manufacturerId_id':manufacturer,
                'modified_date':datetime.now()
            }
              Toy.objects.update_or_create(pk=id,defaults=data)
              messages.success(request,'Toy updated successfully',extra_tags='toyupdated')

              return redirect('showtoys')

         else:
              data={
                'name' : toyname,
                'description' : toydescription,
                'purchasePrice':purchaseprice,
                'rentPrice': 0.00,
                'stockQuantity':quantity,
                'modified_date':datetime.now(),
                'isPurchasable':afp,
                'isRentable':afr,
                'categoryId_id':category,
                'subcategoryId_id':subcategory,
                'storeId_id':store,
                'manufacturerId_id':manufacturer,
                'modified_date':datetime.now()
            }
              Toy.objects.update_or_create(pk=id,defaults=data)
              messages.success(request,'toy updated successfully',extra_tags='toyupdated')
              return redirect('showtoys')

@login_required(login_url='admin/login/')
def addcategory(request):
    categories =  Category.objects.values('id','categoryName').order_by('id')
    context={
        'categories' : categories
    }
    return render(request,'admin/addcategory.html',context)
    
@login_required(login_url='/admin/login/')
def storecategory(request):
        name = request.POST['categoryname']
        try:
            category = Category.objects.get(categoryName = name)
            messages.error(request, 'Category already exists!',extra_tags='categoryError')
            return redirect('addcategory')
        except Category.DoesNotExist:
            Category.objects.create(categoryName = name)
            messages.success(request, 'Category added successfully!',extra_tags='categorySuccess')
            return redirect('addcategory')
        
@login_required(login_url='/admin/login/')
def updatecategory(request,id):
    if request.method=='POST':
        categoryName= request.POST.get('categoryname')
        # print(category)
        category = Category.objects.filter(categoryName=categoryName)
        if category:
            messages.error(request,'Category already exists',extra_tags='categoryupdated')
            return redirect('updatecategory',id)
        else:
            category  =Category.objects.get(pk=id)
            # print(type(category),type())
            category.categoryName = categoryName
            category.save()
            # print()
            messages.success(request,'Category updated successfully',extra_tags='categoryupdated')
            return redirect('updatecategory',id)
    else:
        category = Category.objects.get(pk=id)
        context={
            'category':category
        }
        return render(request,'admin/updatecategory.html',context)

@login_required(login_url='/admin/login/')
def updatesubcategory(request,id):
    if request.method=='POST':
        print(request.POST)
        categoryName= request.POST.get('categoryName')
        print("---------->",categoryName)
        subcategory= request.POST.get('subcategory')
        # print(category)
        sCategory = Subcategory.objects.filter(category=categoryName,subcategoryName=subcategory)
        if sCategory:
            messages.error(request,'Subcategory already exists',extra_tags='categoryupdated')
            return redirect('updatesubcategory',id)
        else:
            sCategory  =Subcategory.objects.get(pk=id)
            sCategory.category_id = categoryName
            sCategory.subcategoryName= subcategory
            sCategory.lastModifiedDate = datetime.now()
            sCategory.save()
            # print()
            messages.success(request,'Subcategory updated successfully',extra_tags='categoryupdated')
            return redirect('updatesubcategory',id)
    else:
        subcategory = Subcategory.objects.get(pk=id)
        category = Category.objects.all()
        context={
            'subcategory':subcategory,
            'categories':category
        }
        return render(request,'admin/updatesubcategory.html',context)
    

@login_required(login_url='/admin/login/')
def storesubcategory(request):
    name = request.POST['subcategory']
    category= request.POST['categoryName']
    try:
        subCategory = Subcategory.objects.get(subcategoryName = name,category_id = category)
        messages.error(request, 'Sub-category already exists!',extra_tags='subcategoryerror')
        return redirect('addcategory')
    except Subcategory.DoesNotExist:
        Subcategory.objects.create(subcategoryName = name, category_id = category)
        messages.success(request, 'Sub-category added successfully!',extra_tags='subcategorysuccess')
        return redirect('addcategory')

@login_required(login_url='/admin/login/')
def showcategory(request):
    if 'filter' in request.GET:
        filter = request.GET.get('filter')
        if filter=='Category':
            categories = Category.objects.values('categoryName','id')
            paginator = Paginator(categories,10)
            pageNumber = request.GET.get('page')
            categories = paginator.get_page(pageNumber)
            context={
                'categories':categories,
                'filter':'Category'
            }
            return render(request,'admin/showcategory.html',context)
        else:
            return redirect('showsubcategory')
    else:
        
        categories = Category.objects.values('categoryName','id')
        paginator = Paginator(categories,10)
        pageNumber = request.GET.get('page')
        categories = paginator.get_page(pageNumber)
        context={
                'categories':categories,
                'filter':'Category'
            }
        return render(request,'admin/showcategory.html',context)
    
@login_required(login_url='/admin/login/')
def searchcategory(request):
    if 'filter' and 'category' in request.GET:
        filter = request.GET.get('filter')
        category = request.GET.get('category')
        if filter == 'Category':
            categories = Category.objects.filter(Q(categoryName__icontains=category))
            paginator = Paginator(categories,3)
            pageNumber = request.GET.get('page')
            categories = paginator.get_page(pageNumber)
            if not categories:
                 context={
                'msg':'No results',
                'filter': filter,
                'searched_category':category
            }
                 return render(request,'admin/showcategory.html',context)
            # print(categories)
            context={
                'categories':categories,
                'filter': filter,
                'searched_category':category
            }
            return render(request,'admin/showcategory.html',context)
        else:
            categories = Subcategory.objects.filter(Q(subcategoryName__icontains=category)| Q(category_id__categoryName__icontains=category)).values('subcategoryName','id','category_id__categoryName').order_by('category_id')
            paginator = Paginator(categories,3)
            pageNumber = request.GET.get('page')
            categories = paginator.get_page(pageNumber)
            if not categories:
                 context={
                'msg':'No results',
                'filter': filter,
                'searched_category':category
            }
                 return render(request,'admin/showcategory.html',context)
            context={
                'categories':categories,
                'filter': filter,
                'searched_category':category
            }
            return render(request,'admin/showcategory.html',context)
    else:
        filter = request.GET.get('filter')
        if filter == 'Subcategory':
            return redirect('showsubcategory')
        else:
            return redirect('showcategory')
        
@login_required(login_url='/admin/login/')
def showsubcategory(request):
    if 'filter' in request.GET:
        filter=request.GET.get('filter')
        if filter=="Category":
            return redirect('showcategory')
    subcategories = Subcategory.objects.values('subcategoryName','id','category_id__categoryName').order_by('category_id')
    paginator = Paginator(subcategories,5)
    pageNumber = request.GET.get('page')
    subcategories = paginator.get_page(pageNumber)
    context={
                'categories':subcategories,
                'filter':'Subcategory'
            }
    return render(request,'admin/showcategory.html',context)

@login_required(login_url='/admin/login/')
def deletecategory(request):
    category = request.POST.get('delete')
    category = Category.objects.get(pk=category)
    category.delete()
    return redirect('showcategory')


@login_required(login_url='/admin/login/')
def deletesubcategory(request):
    subcategory = request.POST.get('delete')
    subcategory = Subcategory.objects.get(pk=subcategory)
    subcategory.delete()
    return redirect('showsubcategory')

@login_required(login_url='/admin/login/')
def manageorders(request):
    orders = Order.objects.annotate( pStatus=Case(
        When(payment_status='P', then=Value('Pending')),
        When(payment_status='C', then=Value('Completed')),
        When(payment_status='F', then=Value('Failed')),
        output_field=CharField()),dStatus=Case(
        When(delivery_status='P', then=Value('Pending')),
        When(delivery_status='D', then=Value('Delivered')),
        When(delivery_status='R', then=Value('Returned')),
        When(delivery_status='OD',then=Value('Out for delivery')),
        output_field=CharField())).all()
    context={
        'orders':orders
    }
    return render(request,'admin/manageorders.html',context)

@login_required(login_url='/admin/login/')
def showusers(request):
    if 'username' in request.GET:
        name = request.GET.get('username')
        print(name)
        users_data = User.objects.filter(username__icontains=name).values('username', 'first_name', 'last_name','is_superuser').all()
        if users_data.exists():
            context={
                'searched_user':name,
                'userdetails':users_data
            }
        else:
            context={
                'searched_user':name,
                'msg':"No user found",
            }
        return render(request,'admin/showusers.html',context)
    else:
        userdetails = User.objects.values('id','username','first_name','last_name').all()
        if not userdetails:
            context={
                'msg':'No users to show'
            }
        else:
            context=  {
                'userdetails': userdetails
            }
        return render(request,'admin/showusers.html',context)

@login_required(login_url='/admin/login/')
def edituser(request):
    editUser = request.POST.get('edit')
    deleteUser = request.POST.get('delete')
    print('edit:',editUser)
    if editUser:
        return redirect('addtoy')
    else:
        return redirect('addcategory')
    
@login_required(login_url='/admin/login/')
def addstore(request):
    return render(request,'admin/addstore.html')

@login_required(login_url='/admin/login/')
def addcatphoto(request):
    categories = Category.objects.all()
    context = {
        'categories':categories
    }
    return render(request,'admin/addcatphotos.html',context)

def storecatphoto(request):
    category   = request.POST.get('category')
    check = Categoryphotos.objects.filter(category = category)
    if check:
        messages.error(request,'Category photo already exists!')
        return redirect('addcatphoto')
    photo   = request.FILES['catimage']
    location= os.path.join(settings.MEDIA_ROOT,'category')
    obj = FileSystemStorage(location=location)
    obj.save(photo.name,photo)
    imgUrl = f'../../media/category/{photo.name}'
    category = Categoryphotos.objects.create(category_id=category,imgUrl=imgUrl)
    messages.success(request,f'Photo added successfully for {category.category.categoryName}')
    return redirect('addcatphoto')


@login_required(login_url='/admin/login/')
def storestore(request):
    sName = request.POST.get('name')
    address = request.POST.get('address')
    oName = request.POST.get('oname')
    email = request.POST.get('email')
    website = request.POST.get('website')
    Store.objects.create(storeName = sName,ownerName=oName,email = email,address=address,website=website)
    messages.success(request,'Store Added successfully')
    return redirect('addstore')

@login_required(login_url='/admin/login/')
def showstores(request):
    stores = Store.objects.values('id','storeName','email','ownerName')
    context={
        'stores':stores
    }
    return render(request,'admin/showstores.html',context)



@login_required(login_url='/admin/login/')
def updatestore(request,id):
    if request.method == 'POST':
        name = request.POST.get('name')
        address = request.POST.get('address')
        oname = request.POST.get('oname')
        email  = request.POST.get('email')
        website = request.POST.get('website')

        data={
            'storeName':name,
            'address':address,
            'ownerName':oname,
            'email': email,
            'website':website
        }
        Store.objects.update_or_create(pk=id,defaults=data)
        messages.success(request,'store updated successfully',extra_tags='storeupdated')
        return redirect('showstores')
    else:
        store = Store.objects.get(pk=id)
        context = {
            'store':store
        }
        return render(request,'admin/updatestore.html',context)
    

@login_required(login_url='/admin/login/')
def showmanufacturers(request):
    manufacturers = Manufacturer.objects.values('id','manufacturerName','email','owner')
    print(manufacturers)
    if not manufacturers:
        context={
            'msg':'No manufacturers to show'
        }
    else:
        context={
            'manufacturers':manufacturers
        }
    return render(request,'admin/showmanufacturers.html',context)

@login_required(login_url='/admin/login/')
def updatemanufacturer(request,id):
    if request.method == 'POST':
        name = request.POST.get('name')
        address = request.POST.get('address')
        oname = request.POST.get('oname')
        email  = request.POST.get('email')
        website = request.POST.get('website')

        data={
            'manufacturerName':name,
            'address':address,
            'owner':oname,
            'email': email,
            'website':website
        }
        Manufacturer.objects.update_or_create(pk=id,defaults=data)
        messages.success(request,'manufacturer updated successfully',extra_tags='storeupdated')
        return redirect('showmanufacturers')
    else:
        manufacturer = Manufacturer.objects.get(pk=id)
        context = {
            'manufacturer':manufacturer
        }
        return render(request,'admin/updatemanufacturer.html',context)

@login_required(login_url='/admin/login/')
def deletemanufacturer(request,id):
    manufacturer = Manufacturer.objects.get(pk=id)
    manufacturer.delete()
    messages.success(request,'manufacturer deleted successfully',extra_tags='storedeleted')
    return redirect('showmanufacturers')

@login_required(login_url='/admin/login/')
def searchmanufacturer(request):
     if 'manufacturer' in request.GET:
        mName = request.GET.get('manufacturer')
        searchedManufacturer = Manufacturer.objects.filter(Q(manufacturerName__icontains=mName))
        if not searchedManufacturer:
            context={
                'msg':'No manufacturer found',
                'searchedManufacturer':mName
            }
            return render(request,'admin/showmanufacturers.html',context)
        else:
            context= {
                'manufacturers':searchedManufacturer,
                'searchedManufacturer':mName
            }
            return render(request,'admin/showmanufacturers.html',context)



@login_required(login_url='/admin/login')
def searchstore(request):
    if 'store' in request.GET:
        storeName = request.GET.get('store')
        searchedStore = Store.objects.filter(Q(storeName__icontains=storeName))
        if not searchedStore:
            context={
                'msg':'No store found',
                'searchedStore':storeName
            }
            return render(request,'admin/showstores.html',context)
        else:
            context= {
                'stores':searchedStore,
                'searchedStore':storeName
            }
            return render(request,'admin/showstores.html',context)


@login_required(login_url='/admin/login/')
def deletestore(request,id):
    store = Store.objects.get(pk=id)
    store.delete()
    messages.success(request,'store deleted successfully',extra_tags='storedeleted')
    return redirect('showstores')


@login_required(login_url='/admin/login/')
def addmanufacturer(request):
    return render(request,'admin/addmanufacturer.html')

@login_required(login_url='/admin/login/')
def storemanufacturer(request):
    sName = request.POST.get('name')
    address = request.POST.get('address')
    oName = request.POST.get('oname')
    email = request.POST.get('email')
    website = request.POST.get('website')
    Manufacturer.objects.create(manufacturerName = sName,owner=oName,email = email,address=address,website=website)
    messages.success(request,'Manufacturer Added successfully')
    return redirect('addmanufacturer')
