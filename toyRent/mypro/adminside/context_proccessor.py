# myapp/context_processors.py
from django.templatetags.static import static
from client.models import Cart,Category,Subcategory,Toy
from django.db.models import Count

def add_username(request):
    if request.user.is_authenticated:
        return {'username': request.user.username}
    return {'username': ''}

def img(request):
        return {'imgUrl': static('admin/profile/admin.jpg')}


def countCartitems(request):
    id = request.user.id
    try:
        total = Cart.objects.filter(user=id)
        total  = total.aggregate(total=Count('user'))
        total = total['total']
        return{'cartNumber':total}
    except KeyError :
         total =0
         return{'cartNumber':total}
    
def categories(request):
    categories= Category.objects.values('categoryName','id')
    verified = []
    subcategories = Subcategory.objects.select_related('category').values('subcategoryName','category__categoryName','id')
    for  subcategory in subcategories:
        for category in categories:
            if subcategory['category__categoryName']== category['categoryName']:
                if category['categoryName']in verified:
                    break
                else:
                    verified.append(category['categoryName'])
    onlycategories=[]
    for category in categories:
        if category['categoryName'] in verified:
            continue
        else:
            if category not in onlycategories:
              onlycategories.append(category['categoryName'])
    return{
        'categories':categories,
        'verified': verified,
        'subcategories':subcategories,
        'onlycategories':onlycategories
    }
def recentcategories(request):
    recentcategories = Toy.objects.all().order_by('-created_date')
    return {
        'recentadded':recentcategories
    }

def pricerange(request):
    totaltoys = Toy.objects.count()
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
            counts[f"{lower}+"] = Toy.objects.filter(purchasePrice__gte=lower).count()
        else:
            counts[f"{lower}-{upper}"] = Toy.objects.filter(purchasePrice__gte=lower, purchasePrice__lt=upper).count()

    countList = []
    for pricerange,count in counts.items():
        countList.append([pricerange,count])

    return{
        'totaltoys':totaltoys,
        'counts':countList
    }

    
    
