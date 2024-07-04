from django.urls import path
from . import views

urlpatterns = [
    path('home/',views.home,name='home'),
    path('contact/',views.contact,name='contact'),
    path('detail/<int:id>',views.detail,name='detail'),
    path('shop/',views.shop,name='shop'),
    path('cart/',views.cart,name='cart'),
    path('address/',views.address,name='address'),
    path('signin/',views.signin,name='signin'),
    path('checksignin/',views.checksignin,name='checksignin'),
    path('addtocart/<int:id>/',views.addtocart,name='addtocart'),
    path('signup/',views.signup,name='signup'),
    path('checksignup/',views.checksignup,name='checksignup'),
    path('signout/',views.signout,name='signout'),
    path('deletecartitem/<int:id>/',views.deletecartitem,name='deletecartitem'),
    path('cartremove/<int:id>/',views.cartremove,name='cartremove'),
    path('cartadd/<int:id>/',views.cartadd,name='cartadd'),
    path('getAddresses',views.getAddresses,name='getAddresses'),
    path('checkout/',views.checkout,name='checkout'),
    # path('create_order/', views.create_order, name='create_order'),
    # path('paymenthandler/', views.paymenthandler, name='paymenthandler'),
    path('checkpaymentmethod',views.checkpaymentmethod,name='checkpaymentmethod'),
    path('searchproduct/',views.searchproduct,name='searchproduct'),
    path('checkquantity/',views.checkquantity,name='checkquantity'),
    
]