from django.shortcuts import render, HttpResponse,redirect
from .models import Toy,Billingaddress,Deliveryaddress,Cart,Order,OrderDetails,Contact
from django.db.models import F,DecimalField,Sum,Q
from django.db.models.functions import Round
from django.contrib import auth,messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib.auth.password_validation import validate_password
from django.core.validators import validate_email
# import razorpay
# from django.conf import settings
from django.core.exceptions import ValidationError
# from django.views.decorators.csrf import csrf_exempt
from django.core.paginator import Paginator
from adminside.models import Categoryphotos

# client = razorpay.Client(auth=(settings.RAZORPAY_KEY_ID, settings.RAZORPAY_KEY_SECRET))
# Create your views here.

def signin(request):
    return render(request,'client/auth-signin.html')

def checksignin(request):
    username = request.POST.get('username')
    password = request.POST.get('password')
    user = auth.authenticate(username=username,password=password)
    if user is not None:
       if user.is_superuser:
           messages.error(request, '*Please check username or password.')
           return redirect('signin')
       else:
           auth.login(request, user)
           return redirect('home')
    else:
        messages.error(request, '*Please check username or password.')
        return redirect('signin')
    
def signout(request):
     auth.logout(request)
     return redirect('signin')
def signup(request):
    context={}
    return render(request,'client/auth-signup.html',context)

def checksignup(request):
    if request.method=='POST':
        firstName = request.POST.get('firstName')
        lastName = request.POST.get('lastName')
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')
        confirmPassword = request.POST.get('confirmPassword')
        userExists = User.objects.filter(username=username).exists()
        if userExists:

            context={
                    'firstName':firstName,
                    'lastName':lastName,
                    'username':username,
                    'password':password,
                    'confirmPassword': confirmPassword,
                    'email':email,
                    'userExists':"userExists"
              }
            return render(request,'client/auth-signup.html',context)
        
        try:
            validate_email(email)
        except ValidationError as e:
            context={
                    'firstName':firstName,
                    'lastName':lastName,
                    'username':username,
                    'password':password,
                    'confirmPassword': confirmPassword,
                    'email':email,
                    'validateEmail':e
                }
            return render(request,'client/auth-signup.html',context)
            
        if password == confirmPassword:
            try:
                    # Validate the password
                    validate_password(password)
                    
                    # Create the user if password is valid
                    user = User.objects.create_user(
                        first_name=firstName,
                        last_name=lastName,
                        username=username,
                        email=email,
                        password=password
                    )
                    return redirect('signin')
            except ValidationError as e:
                    # If password validation fails, add the error messages to the context
                    context={
                    'firstName':firstName,
                    'lastName':lastName,
                    'username':username,
                    'password':password,
                    'confirmPassword': confirmPassword,
                    'email':email,
                    'validate':e
                }
                    return render(request,'client/auth-signup.html',context)
        else:
                # If passwords do not match, add an error message
                messages.error(request, "Passwords do not match",extra_tags='dontmatch')
                context={
                    'firstName':firstName,
                    'lastName':lastName,
                    'username':username,
                    'password':password,
                    'email':email,
                    'confirmPassword': confirmPassword
                }
                return render(request,'client/auth-signup.html',context)
    else:
         return redirect('signup')

@login_required(login_url='/client/signin')
def addtocart(request,id):
    stock  = Toy.objects.filter(pk=id).values('stockQuantity','name')
    if stock[0]['stockQuantity']>=1:
        product=id
        uId = request.user.id
        quantity = request.POST.get('quantity')
        cart_item, created = Cart.objects.get_or_create(product_id=product, user_id=uId)
        if not created:
            cartFilter = Cart.objects.get(user=uId,product=product)
            cartQuantity =cartFilter.quantity
            if quantity:
                if stock[0]['stockQuantity']<(int(quantity)+cartQuantity):
                    context={
                    'stockerror':f'We  have {stock[0]['stockQuantity']}left in our stock for {stock[0]['name']}',
                    'name': stock[0]['name']
                    }
                    messages.error(request,f'{stock[0]['name']} is only {stock[0]['stockQuantity']} available',extra_tags=f'{stock[0]['name']}')
                    return redirect('detail',id)
                    
                else:
                    cart_item.quantity += int(quantity)
                    cart_item.save()
                    messages.success(request,'Product added to the cart')
                    return redirect('detail',id)
                
            else:
                if stock[0]['stockQuantity']>=1 and cartQuantity<stock[0]['stockQuantity']:
                    cart_item.quantity += 1
                    cart_item.save()
                    messages.success(request,'Product added to the cart')
                    return redirect('detail',id)
                else:
                    
                    messages.error(request,f'{stock[0]['name']} is only {stock[0]['stockQuantity']} available',extra_tags='stockerror')
                    return redirect('cart')

        else:
            if quantity:
                if (int(quantity)-1)> stock[0]['stockQuantity'] :
                    context={
                    'stockerror':f'We  have {stock[0]['stockQuantity']}that much in our stock for {stock[0]['name']}',
                    'name': stock[0]['name']

                    }
                    messages.error(request,f'{stock[0]['name']} is only {stock[0]['stockQuantity']} available',extra_tags=f'{stock[0]['name']}')
                    return redirect('detail',id)
                    
                else:
                    cart_item.quantity += int(quantity)-1
                    cart_item.save()
                    messages.success(request,'Product added to the cart')
                    return redirect('detail',id)
            else:
                messages.success(request,'Product added to the cart')
                return redirect('detail',id)
    else:
         messages.error(request,f'This product is currently out of stock please check again latter')
         return redirect('detail',id)


@login_required(login_url='/client/signin')
def cartadd(request,id):
    uId = request.user.id   
    stock  = Toy.objects.filter(pk=id).values('stockQuantity','name')
    cartFilter = Cart.objects.get(user=uId,product=id)
    cartQuantity =cartFilter.quantity
    if stock[0]['stockQuantity']>=1 and cartQuantity<stock[0]['stockQuantity']:
        cart = Cart.objects.get(product=id,user=uId)
        cart.quantity+=1
        cart.save()
        return redirect('cart')
    else:
        messages.error(request,f'{stock[0]['name']} is only {stock[0]['stockQuantity']} available',extra_tags=f'stockerror')
        return redirect('cart')


@login_required(login_url='/client/signin')
def home(request):
    toys  = Toy.objects.only('id','name','img_url','purchasePrice').annotate(
    increasedPrice=Round(F('purchasePrice') * 1.2, 2,output_field=DecimalField(max_digits=10, decimal_places=2))
)
    posterList = []
    posters = Categoryphotos.objects.all()
    for category in posters:
        count = Toy.objects.filter(categoryId=category.category)
        count  = count.count()
        posterList.append([category.imgUrl,category.category.categoryName,count])

   
    context={
        'toys':toys,
        'home':True,
        'posters':posterList
    }
    return render(request,'client/index.html',context)

@login_required(login_url='/client/signin')
def contact(request):
    if request.method=='POST':
        user = request.user.id
        subject = request.POST.get('subject')
        message = request.POST.get('message')
        Contact.objects.create(subject=subject,message=message,user_id=user)
        messages.success(request,'message sent successfully')
        return redirect('contact')
    context={
        'contact':True
    }
    return render(request,'client/contact.html',context)

@login_required(login_url='/client/signin')
def detail(request,id):
    toyid = id
    toyDetails  = Toy.objects.annotate(increasedPrice=Round(F('purchasePrice') * 1.2, 2,output_field=DecimalField(max_digits=10, decimal_places=2))).get(pk=toyid)
    similarProducts = Toy.objects.filter(categoryId=toyDetails.categoryId).only('id','name','img_url','purchasePrice').annotate(
    increasedPrice=Round(F('purchasePrice') * 1.2, 2,output_field=DecimalField(max_digits=10, decimal_places=2)))
    context={
         'toyDetails':toyDetails,
         'similarProducts':similarProducts,
         'detail':True
    }
    return render(request,'client/detail.html',context)

@login_required(login_url='/client/signin')
def shop(request):
    products = Toy.objects.annotate(increasedPrice=Round(F('purchasePrice') * 1.2, 2,output_field=DecimalField(max_digits=10, decimal_places=2))).values('img_url','name','purchasePrice','id','increasedPrice')
    paginator = Paginator(products, 3)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    context={
        'page_obj':page_obj,
        'shop':True,
        'all':True
    }
    return render(request,'client/shop.html',context)

@login_required(login_url='/client/signin')
def cart(request):
    id=request.user.id
    print(id)
    product = Cart.objects.filter(user=id)
    if product.exists():
        products = Cart.objects.filter(user=id).select_related('product_id').annotate(productTotal=F('product__purchasePrice') * F('quantity')).values('product__id','product__img_url','product__name','quantity','product__purchasePrice','productTotal')
        subtotal = products.aggregate(subtotal=Sum('productTotal'))
        subtotal=subtotal['subtotal']
        shipping= 300
        total = subtotal+shipping
        context={
            'products':products,
            'subtotal':subtotal,
            'shipping':shipping,
            'total':total
        }
        return render(request,'client/cart.html',context)
    else:
       context={
           'msg':'Add products to cart',
           'subtotal':0,
            'shipping':0,
            'total':0
       }
       return render(request,'client/cart.html',context)
@login_required(login_url='/client/signin')
def deletecartitem(request,id):
    uId = request.user.id
    cart = Cart.objects.get(product=id,user=uId)
    cart.delete()
    return redirect('cart')

@login_required(login_url='/client/signin')
def cartremove(request,id):
    uId = request.user.id
    cart = Cart.objects.get(product=id,user=uId)
    if cart.quantity==1:
        cart.delete()
    else:
        cart.quantity-=1
        cart.save()
    return redirect('cart')



@login_required(login_url='/client/signin')
def address(request):
    id = request.user.id
    billAddress = Billingaddress.objects.filter(uId=id).exists()
    shipAddress = Deliveryaddress.objects.filter(uId=id).exists()
    if billAddress:
        billAddress = Billingaddress.objects.get(uId=id)
        sba = billAddress.address.split('->')
    else:
        billAddress=''
        sba = ''
    if shipAddress:
        shipAddress = Deliveryaddress.objects.get(uId=id)
        ssa = shipAddress.address.split('->') 
    else:
        billAddress =''
        ssa=''
    context={
        'billingAddress':billAddress,
        'shippingAddress': shipAddress,
        'sba':sba,
        'ssa':ssa
    }
    return render(request,'client/address.html',context)

@login_required(login_url='/client/signin')
def getAddresses(request):
    id = request.user.id
    billAddress = Billingaddress.objects.filter(uId=id).exists()
    shipAddress = Deliveryaddress.objects.filter(uId=id).exists()
    #form data
    bfirstname = request.POST.get('bfirstName')
    blastName = request.POST.get('blastName')
    bemail = request.POST.get('bemail')
    bmobile = request.POST.get('bmobile')
    bad1 = request.POST.get('bad1')
    bad2 = request.POST.get('bad2')
    bcountry = request.POST.get('bcountry')
    bcity = request.POST.get('bcity')
    bstate = request.POST.get('bstate')
    bzipcode = request.POST.get('bzipcode')
    fulladdress = [bad1,bad2,bcountry,bcity,bstate,bzipcode]
    joinaddress = '->'.join(fulladdress)
    diffenentaddress = request.POST.get('differentaddress')
    sameaddress = request.POST.get('sameaddress')
 
    if not sameaddress and not diffenentaddress :
        firstname = request.POST.get('firstName')
        lastName = request.POST.get('lastName')
        email = request.POST.get('email')
        mobile = request.POST.get('mobile')
        ad1 = request.POST.get('ad1')
        ad2 = request.POST.get('ad2')
        country = request.POST.get('country')
        city = request.POST.get('city')
        state = request.POST.get('state')
        zipcode = request.POST.get('zipcode')
        context ={ 'billingAddress':{'firstName' : firstname,
        'lastName' : lastName,
        'email' : email,      
        'mobile' : mobile,
        'ad1' : ad1,
        'ad2' : ad2,
        'country' : country,
        'city' : city,
        'state' : state,
        'zipcode' : zipcode}
        }
        messages.error(request,'please select any of this one')
        return render(request,'client/address.html',context)
    uId= request.user.id
    if billAddress:
        defaults={
            'uId_id':uId,
            'firstName':bfirstname,
            'lastName':blastName,
            'email':bemail,
            'mobile':bmobile,
            'address':joinaddress
        }
        Billingaddress.objects.update_or_create(uId=id,defaults=defaults)
    else:
         Billingaddress.objects.create(uId_id = uId,firstName=bfirstname,lastName=blastName,email=bemail,mobile=bmobile,address=joinaddress)
    if shipAddress:
        if sameaddress:
            defaults={
            'uId_id':uId,
            'firstName':bfirstname,
            'lastName':blastName,
            'email':bemail,
            'mobile':bmobile,
            'address':joinaddress
        }
            Deliveryaddress.objects.update_or_create(uId=id,defaults=defaults)
            return redirect('checkout')
        else:
            firstname = request.POST.get('firstName')
            lastName = request.POST.get('lastName')
            email = request.POST.get('email')
            mobile = request.POST.get('mobile')
            ad1 = request.POST.get('ad1')
            ad2 = request.POST.get('ad2')
            country = request.POST.get('country')
            city = request.POST.get('city')
            state = request.POST.get('state')
            zipcode = request.POST.get('zipcode')
            sFulladdress = [ad1,ad2,country,city,state,zipcode]
            sFulladdress = '->'.join(sFulladdress)
            defaults={
                'uId_id':uId,
                'firstName':firstname,
                'lastName':lastName,
                'email':email,
                'mobile':mobile,
                'address':sFulladdress
          }
            Deliveryaddress.objects.update_or_create(uId=id,defaults=defaults)
            return redirect('checkout')
    else:
        if sameaddress:
            Deliveryaddress.objects.create(uId_id = uId,firstName=bfirstname,lastName=blastName,email=bemail,mobile=bmobile,address=joinaddress)
            return redirect('checkout')
        else:
            firstname = request.POST.get('firstName')
            lastName = request.POST.get('lastName')
            email = request.POST.get('email')
            mobile = request.POST.get('mobile')
            ad1 = request.POST.get('ad1')
            ad2 = request.POST.get('ad2')
            country = request.POST.get('country')
            city = request.POST.get('city')
            state = request.POST.get('state')
            zipcode = request.POST.get('zipcode')
            sFulladdress = [ad1,ad2,country,city,state,zipcode]
            sFulladdress = '->'.join(sFulladdress)
            Deliveryaddress.objects.create(uID_id=uId,irstName=firstname,lastName=lastName,email=email,mobile=mobile,address=sFulladdress)
            return redirect('checkout')

@login_required(login_url='/client/signin')
def checkout(request):
    id = request.user.id
    products = Cart.objects.filter(user=id).select_related('product_id').annotate(productTotal=F('product__purchasePrice') * F('quantity')).values('product__name','productTotal')
    subtotal = products.aggregate(subtotal=Sum('productTotal'))
    shipping= 300
    total = subtotal['subtotal']+shipping
    uId= request.user.id
    billingAddress= Billingaddress.objects.get(uId=uId)
    shippingAddress= Deliveryaddress.objects.get(uId=uId)
    bSplitAddress= billingAddress.address.split('->')
    sSplitAddress= shippingAddress.address.split('->')
    context={
        'billingAddress': billingAddress,
        'shippingAddress': shippingAddress,
        'bSplitAddress' : bSplitAddress,
        'sSplitAddress' : sSplitAddress,
        'products':products,
        'subtotal':subtotal,
        'shipping':shipping,
        'total':total,
    }
    return render(request,'client/checkout.html',context)

def checkpaymentmethod(request):
    paymentmethod = request.POST.get('payment')
    user = request.user.id
    if paymentmethod=='cod':
        products = Cart.objects.filter(user=user).select_related('product_id').annotate(productTotal=F('product__purchasePrice') * F('quantity')).values('productTotal')
        subtotal = products.aggregate(subtotal=Sum('productTotal'))
        shipping = 300
        total = shipping+subtotal['subtotal']
        new_order =  Order.objects.create(customer_id=user,total_amount=total)
        orderId = new_order.id
        cart = Cart.objects.filter(user=user)

        for  item in cart:
            toy = Toy.objects.get(pk=item.product.id)
            toy.stockQuantity -=item.quantity
            toy.save()
            OrderDetails.objects.create(toyid_id=item.product.id,quantity=item.quantity,itemprice = item.product.purchasePrice,orderid_id=orderId)
            context={
               'orderId':new_order.id,
               'totalAmount':new_order.total_amount
           }
        Cart.objects.filter(user=user).delete()
        return render(request,'client/successful.html',context)
    elif paymentmethod=='razor pay':
        return HttpResponse('https://rzp.io/l/kZDfA1L8l')
           

# def create_order(request):
#     products = Cart.objects.select_related('product_id').annotate(productTotal=F('product__purchasePrice') * F('quantity')).values('productTotal')
#     subtotal = products.aggregate(subtotal=Sum('productTotal'))
#     shipping= 300
#     total = subtotal['subtotal']+shipping
#     order_amount = float(total)*100  # Amount in paise
#     order_receipt = 'order_rcptid_11'
#     order_currency = 'INR'
        
#     response = client.order.create({
#         "amount": order_amount,
#         "currency": order_currency,
#         "receipt": order_receipt,
#         "payment_capture": '1'
#     })
    
#     # order = Order.objects.create(
#     #     razorpay_order_id=response['id'],
#     #     amount=order_amount,
#     #     currency=order_currency,
#     #     receipt=order_receipt
#     # )

#     context = {
#         'razorpay_key': settings.RAZORPAY_KEY_ID,
#         'order_id': response['id'],
#         'amount': order_amount,
#         'name': 'Your Company Name',
#         'description': 'Purchase Description',
#         'prefill': {
#             'name': 'Your Customer Name',
#             'email': 'customer@example.com',
#             'contact': '1234567890'
#         },
#         'theme': {
#             'color': '#3399cc'
#         },
#         'method': {
#             'netbanking': '0',
#             'card': '0',
#             'upi': '1',
#             'wallet': '0',
#             'emi': '0'
#         }
#     }
#     return render(request,'client/payment.html',context)

# @csrf_exempt
# def paymenthandler(request):
#     if request.method == "POST":
#         try:
#             payment_id = request.POST.get('razorpay_payment_id', '')
#             order_id = request.POST.get('razorpay_order_id', '')
#             signature = request.POST.get('razorpay_signature', '')

#             params_dict = {
#                 'razorpay_order_id': order_id,
#                 'razorpay_payment_id': payment_id,
#                 'razorpay_signature': signature
#             }

#             result = client.utility.verify_payment_signature(params_dict)

#             if result is None:
#                 amount = 50000  # Amount in paise
#                 client.payment.capture(payment_id, amount)

#                 return JsonResponse({'status': 'Payment successful'})
#             else:
#                 return JsonResponse({'status': 'Payment verification failed'})

#         except Exception as e:
#             return JsonResponse({'status': 'Payment failed', 'error': str(e)})
#     else:
#         return JsonResponse({'status': 'Invalid request method'})

@login_required(login_url='/client/signin')
def searchproduct(request):
        if 'pricerange' in request.GET:
                pricerange= request.GET.getlist('pricerange')
                if 'pricerange' not in request.session:
                    request.session['pricerange'] = pricerange[-1]
                    print('session price:',request.session.get('pricerange'))
                    pricerange = request.session.get('pricerange')
                    if pricerange == '10000+':
                                pricerange = '10000-1000000'
                else:
                    for price in pricerange:
                        if price != request.session.get('pricerange'):
                            request.session['pricerange'] = price
                            request.session.modified = True
                            pricerange = request.session.get('pricerange')
                            if pricerange == '10000+':
                                pricerange = '10000-1000000'
                                print('session price:',request.session.get('pricerange'))

                            break
                        else:
                            request.session['pricerange'] = price
                            request.session.modified = True
                            pricerange = request.session.get('pricerange')

                            if pricerange == '10000+':
                                pricerange = '10000-1000000'
                    
        if 'name' in request.GET and 'filter' in request.GET and 'pricerange' in request.GET:
            name = request.GET.get('name')
            filter = request.GET.get('filter')
            pricerange = pricerange
            if pricerange == 'all':
                products = Toy.objects.filter(Q(name__icontains=name) | Q(categoryId__categoryName__icontains=name)|Q(subcategoryId__subcategoryName__icontains=name)).annotate(increasedPrice=Round(F('purchasePrice') * 1.2, 2,output_field=DecimalField(max_digits=10, decimal_places=2))).values('img_url','name','purchasePrice','id','increasedPrice').order_by(filter)
            else:
                pricerange = pricerange.split('-')
                products = Toy.objects.filter((Q(name__icontains=name) | Q(categoryId__categoryName__icontains=name)) & (Q(purchasePrice__gte = int(pricerange[0])) & Q(purchasePrice__lte = int(pricerange[1])))).annotate(increasedPrice=Round(F('purchasePrice') * 1.2, 2,output_field=DecimalField(max_digits=10, decimal_places=2))).values('img_url','name','purchasePrice','id','increasedPrice').order_by(filter)
            counts,totaltoys = countprice(request,name)
            totaltoys= products.count()
            paginator = Paginator(products, 3)
            page_number = request.GET.get('page')
            page_obj = paginator.get_page(page_number)
            pricerange = '-'.join(pricerange) 
            if products.exists():
                if pricerange == 'a-l-l':
                    context={
                        'searched_product':name,
                        'page_obj':page_obj,
                        'filter':filter,
                        'pricerange':'all',
                        'totaltoys':totaltoys,
                        'counts':counts,
                        'all':True
                    }
                else:
                    context={
                        'searched_product':name,
                        'page_obj':page_obj,
                        'filter':filter,
                        'pricerange':pricerange,
                        'totaltoys':totaltoys,
                        'counts':counts
                    }

            else:
                counts,totaltoys = list(zerocount())
                context={
                    'searched_product':name,
                    'filter':filter,
                    'counts':counts,
                    'pricerange':pricerange,
                    'msg':"No Product found",
                    'totaltoys':totaltoys
                }

            return render(request,'client/shop.html',context)
        elif 'name' in request.GET  and 'pricerange' in request.GET:
            name = request.GET.get('name')
            filter = request.GET.get('filter')
            pricerange = pricerange
            if pricerange =='all':
                products = Toy.objects.filter(Q(name__icontains = name) |  Q(categoryId__categoryName__icontains=name)).annotate(increasedPrice=Round(F('purchasePrice') * 1.2, 2,output_field=DecimalField(max_digits=10, decimal_places=2))).values('img_url','name','purchasePrice','id','increasedPrice')
                totaltoys= products.count()
                paginator = Paginator(products, 3)
                page_number = request.GET.get('page')
                page_obj = paginator.get_page(page_number)
                pricerange = '-'.join(pricerange) 
                counts,totaltoys= countprice(request,name)

                if products.exists():
                    if pricerange =='a-l-l':

                        context={
                            'all':True,
                            'searched_product':name,
                            'page_obj':page_obj,
                            'all':pricerange,
                            'counts':counts,
                            'totaltoys':totaltoys,
                            'pricerange':'all'
                          }
                    else:
                        context={
                            'searched_product':name,
                            'page_obj':page_obj,
                            'all':pricerange,
                            'counts':counts,
                            'totaltoys':totaltoys
                    }
                else:
                    counts,totaltoys = zerocount()
                    context={
                        'counts':counts,
                        'searched_product':name,
                        'pricerange':pricerange,
                        'msg':"No Product found",
                        'totaltoys':totaltoys
                    }
                return render(request,'client/shop.html',context)
            else:
                pricerange = pricerange.split('-')
                products = Toy.objects.filter( (Q(name__icontains=name) |   Q(categoryId__categoryName__icontains=name)) &( Q(purchasePrice__gte = int(pricerange[0])) & Q(purchasePrice__lte = int(pricerange[1])))).annotate(increasedPrice=Round(F('purchasePrice') * 1.2, 2,output_field=DecimalField(max_digits=10, decimal_places=2))).values('img_url','name','purchasePrice','id','increasedPrice')
                totaltoys= products.count()
                paginator = Paginator(products, 3)
                page_number = request.GET.get('page')
                page_obj = paginator.get_page(page_number)
                counts,totaltoys = countprice(request,name)
                pricerange = '-'.join(pricerange) 
                if products.exists():
                    context={
                        'searched_product':name,
                        'page_obj':page_obj,
                        'pricerange':pricerange,
                        'counts':counts,
                        'totaltoys':totaltoys
                    }
                else:
                    counts,totaltoys = zerocount()
                    context={
                        'counts':counts,
                        'searched_product':name,
                        'pricerange':pricerange,
                        'msg':"No Product found",
                        'counts':counts,
                        'totaltoys':totaltoys
                    }

                return render(request,'client/shop.html',context)

        elif 'name' in request.GET and 'filter' in request.GET:
            name = request.GET.get('name')
            filter = request.GET.get('filter')
            products = Toy.objects.filter(Q(name__icontains=name) | Q(categoryId__categoryName__icontains=name)).annotate(increasedPrice=Round(F('purchasePrice') * 1.2, 2,output_field=DecimalField(max_digits=10, decimal_places=2))).values('img_url','name','purchasePrice','id','increasedPrice').order_by(filter)
            paginator = Paginator(products, 3)
            page_number = request.GET.get('page')
            page_obj = paginator.get_page(page_number)
            counts,totaltoys = countprice(request,name)

            if products.exists():
                context={
                    'searched_product':name,
                    'filter':filter,
                    'page_obj':page_obj,
                    'totaltoys':totaltoys,
                    'counts':counts
                }
            else:
                counts,totaltoys = zerocount()

                context={
                    'counts':counts,
                    'searched_product':name,
                    'filter':filter,
                    'msg':"No Product found",
                    'totaltoys':totaltoys
                }

            return render(request,'client/shop.html',context)
        elif 'filter' in request.GET and 'pricerange' in request.GET:
            filter = request.GET.get('filter')
            pricerange = pricerange
            if pricerange == 'all':
                products = Toy.objects.filter().annotate(increasedPrice=Round(F('purchasePrice') * 1.2, 2,output_field=DecimalField(max_digits=10, decimal_places=2))).values('img_url','name','purchasePrice','id','increasedPrice').order_by(filter)
            else:
                pricerange = pricerange.split('-')
                products = Toy.objects.filter(Q(purchasePrice__gte = int(pricerange[0])) & Q(purchasePrice__lte = int(pricerange[1]))).annotate(increasedPrice=Round(F('purchasePrice') * 1.2, 2,output_field=DecimalField(max_digits=10, decimal_places=2))).values('img_url','name','purchasePrice','id','increasedPrice').order_by(filter)
            paginator = Paginator(products, 3)
            page_number = request.GET.get('page')
  
            page_obj = paginator.get_page(page_number)
            pricerange = '-'.join(pricerange) 
          
            if products.exists():
                if pricerange == 'a-l-l':

                    context={
                        'page_obj':page_obj,
                        'filter':filter,
                        'pricerange':'all',
                        'all':True
                    }
                else:
                    context={
                        'page_obj':page_obj,
                        'filter':filter,
                        'pricerange':pricerange,
                    }

            else:
                context={
                    'filter':filter,
                    'pricerange':pricerange,
                    'msg':"No Product found",
                }

            return render(request,'client/shop.html',context)
        elif 'name' in request.GET:
            name = request.GET.get('name')
            products = Toy.objects.filter(Q(name__icontains=name) | Q(categoryId__categoryName__icontains=name)).annotate(increasedPrice=Round(F('purchasePrice') * 1.2, 2,output_field=DecimalField(max_digits=10, decimal_places=2))).values('img_url','name','purchasePrice','id','increasedPrice')
            totaltoys= products.count()
            paginator = Paginator(products, 3)
            page_number = request.GET.get('page')
            counts,totaltoys = countprice(request,name)
            
            page_obj = paginator.get_page(page_number)
            if products.exists():
                context={
                    'all':True,
                    'searched_product':name,
                    'page_obj':page_obj,
                    'totaltoys':totaltoys,
                    'counts': counts
                }
            else:
                counts,totaltoys = zerocount()
                context={
                    'searched_product':name,
                    'msg':"No Product found",
                    'counts':counts,
                    'totaltoys':totaltoys
                }
            return render(request,'client/shop.html',context)

        elif 'filter' in request.GET:
            filter = request.GET.get('filter')
            products = Toy.objects.annotate(increasedPrice=Round(F('purchasePrice') * 1.2, 2,output_field=DecimalField(max_digits=10, decimal_places=2))).values('img_url','name','purchasePrice','id','increasedPrice').all().order_by(filter)
            paginator = Paginator(products, 3)
            page_number = request.GET.get('page')
            page_obj = paginator.get_page(page_number)
            if products.exists():
                context={
                    'page_obj':page_obj,
                    'filter':filter,
                }
            else:
                context={
                    'filter':filter,
                    'msg':"No Product found",
                }

            return render(request,'client/shop.html',context)
        elif 'pricerange' in request.GET:
            pricerange = pricerange
            if pricerange=='all':
              products = Toy.objects.filter().annotate(increasedPrice=Round(F('purchasePrice') * 1.2, 2,output_field=DecimalField(max_digits=10, decimal_places=2))).values('img_url','name','purchasePrice','id','increasedPrice')
            else:
                pricerange = pricerange.split('-')
                products = Toy.objects.filter(Q(purchasePrice__gte = int(pricerange[0])) & Q(purchasePrice__lte = int(pricerange[1]))).annotate(increasedPrice=Round(F('purchasePrice') * 1.2, 2,output_field=DecimalField(max_digits=10, decimal_places=2))).values('img_url','name','purchasePrice','id','increasedPrice')
            
            paginator = Paginator(products, 3)
            page_number = request.GET.get('page')
            
            page_obj = paginator.get_page(page_number)
            pricerange = '-'.join(pricerange) 
            if products.exists():
                if pricerange=='a-l-l':
                    context={
                        'page_obj':page_obj,
                        'pricerange':'all',
                        'all':True
                    }
                else:
                     context={
                        'page_obj':page_obj,
                        'pricerange':pricerange,
                    }

            else:
                context={
                    'msg':"No Product found",
                    'pricerange':pricerange
                }
            return render(request,'client/shop.html',context)
        else:
            products = Toy.objects.annotate(increasedPrice=Round(F('purchasePrice') * 1.2, 2,output_field=DecimalField(max_digits=10, decimal_places=2))).values('img_url','name','purchasePrice','id','increasedPrice')
            totaltoys= products.count()
            paginator = Paginator(products, 3)
            page_number = request.GET.get('page')
            page_obj = paginator.get_page(page_number)
            if products.exists():
                context={
                    'page_obj':page_obj,
                    'all':True
                }
            else:
                context={
                    'msg':"No Product found",
                }

            return render(request,'client/shop.html',context)
            
def countprice(request,name):
    product = name
    price_ranges = [
        (0, 1000),
        (1000, 2000),
        (2000, 4000),
        (4000, 10000),
        (10000, None)  # None means no upper limit
    ]

    # Prepare a dictionary to hold the counts
    counts = {}

    for lower, upper in price_ranges:
        if upper is None:
            counts[f"{lower}+"] = Toy.objects.filter((Q(name__icontains=product) | Q(categoryId__categoryName__icontains=product)) &( Q(purchasePrice__gte=lower))).count()
        else:
            counts[f"{lower}-{upper}"] = Toy.objects.filter((Q(name__icontains=product) | Q(categoryId__categoryName__icontains=product)) & (Q(purchasePrice__gte=lower) & Q(purchasePrice__lte=upper))).count()

    countList = []
    for pricerange,count in counts.items():
        countList.append([pricerange,count])

    totaltoys = 0
    for name,count in countList:
        totaltoys += count


    return countList,totaltoys

def zerocount():
    price_ranges = [
        (0, 1000),
        (1000, 2000),
        (2000, 4000),
        (4000, 10000),
        (10000, None)  # None means no upper limit
    ]

    countList = []
    for upper,lower in price_ranges:
        countList.append([str(upper)+'-'+str(lower),0])
    alltoys = 0
    return countList,alltoys

def checkquantity(request):
    id = request.user.id
    cart = Cart.objects.filter(user=id)
    if not cart:
        messages.error(request,'You don\'t have any item in the cart','emptycart')
        return redirect('cart') 

    for item in cart:
        toy = Toy.objects.get(pk=item.product.id)
        if item.quantity  > toy.stockQuantity:
            messages.error(request,f'{toy.name} is  {toy.stockQuantity} available',extra_tags=f'stockerror')
            return redirect('cart') 
        else:
            continue
   
    return redirect('address')


            

        



