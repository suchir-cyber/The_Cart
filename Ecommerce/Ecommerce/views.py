from django.shortcuts import render,redirect
from store_app.models import Product,Categories,Filter_Price,Color,Brand,Contact_Us,Order,OrderItem
from django.contrib import messages
from django.conf import settings
from django.core.mail import send_mail
from django.contrib.auth.models import User
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.decorators import login_required
from cart.cart import Cart
from django.views.decorators.csrf import csrf_exempt
import razorpay
import logging

client = razorpay.Client(auth=(settings.RAZORPAY_KEY_ID,settings.RAZORPAY_KEY_SECRET))

logger = logging.getLogger(__name__)

def BASE(request):
    return render(request,'Main/base.html')

def HOME(request):
    product = Product.objects.filter(status = 'PUBLISH')

    context = {
        'product' : product
    }
    return render(request,'Main/index.html',context)

def PRODUCT(request):
    # Fetch all published products
    all_products = Product.objects.filter(status='PUBLISH')
    # Start with all products for filtering
    product = all_products

    # Get filter parameters from the request
    CATID = request.GET.get('categories')
    PRICE_FILTER_ID = request.GET.get('filter_price')
    COLOR_ID = request.GET.get('color')
    BRAND_ID = request.GET.get('brand')
    ATOZ_ID = request.GET.get('ATOZ')
    ZTOA_ID = request.GET.get('ZTOA')
    PRICE_LOWTOHIGH_ID = request.GET.get('PRICE_LOWTOHIGH')
    PRICE_HIGHTOLOW_ID = request.GET.get('PRICE_HIGHTOLOW')
    NEW_PRODUCT_ID = request.GET.get('NEW_PRODUCT')
    OLD_PRODUCT_ID = request.GET.get('OLD_PRODUCT')

    # Apply filters based on query parameters
    if CATID:
        product = product.filter(Categories_id=int(CATID))
    elif PRICE_FILTER_ID:
        product = product.filter(filter_price=PRICE_FILTER_ID)
    elif COLOR_ID:
        product = product.filter(color=COLOR_ID)
    elif BRAND_ID:
        product = product.filter(brand=BRAND_ID)
    elif ATOZ_ID:
        product = product.order_by('name')
    elif ZTOA_ID:
        product = product.order_by('-name')
    elif PRICE_LOWTOHIGH_ID:
        product = product.order_by('price')
    elif PRICE_HIGHTOLOW_ID:
        product = product.order_by('-price')
    elif NEW_PRODUCT_ID:
        product = product.filter(condition='New').order_by('-id')
    elif OLD_PRODUCT_ID:
        product = product.filter(condition='Old').order_by('-id')
    else:
        product = product.order_by('-id')

    # Prepare context for the template
    context = {
        'product': product,
        'categories': Categories.objects.all(),
        'Filter_price': Filter_Price.objects.all(),
        'color': Color.objects.all(),
        'brand': Brand.objects.all(),
        'product_count': product.count(),  # Number of products on the current page
        'total_products': all_products.count(),  # Total number of published products
    }
    return render(request, 'Main/product.html', context)



def SEARCH(request):
    query = request.GET.get('query')
    
    product = Product.objects.filter(name__icontains = query)

    context = {
        'product' : product
    }
    return render(request,'Main/search.html',context)

def PRODUCT_DETAIL_PAGE(request,id):
    prod = Product.objects.filter(id = id).first()
    context = {
        'prod' : prod
    }
    return render(request,'Main/product_single.html',context)

def Contact_Page(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        email = request.POST.get('email')
        subject = request.POST.get('subject')
        message = request.POST.get('message')
        
        contact = Contact_Us(
                name = name,
                email = email,
                subject = subject,
                message = message
        )
        
        subject = subject
        message = message
        email_from = settings.EMAIL_HOST_USER
        try:
            send_mail(subject,message,email_from,['suchir.pandula18@gmail.com'])
            contact.save()
            messages.success(request, f'Your request has been sent successfully!')
            return redirect('home')
        except Exception as e:
            messages.error(request, f'Error sending email: {str(e)}')
            return redirect('contact')

        

    return render(request,'Main/contact.html')


def HandleRegister(request):
    if request.method == "POST":
        username = request.POST.get('username')
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        email = request.POST.get('email')
        pass1 = request.POST.get('pass1')
        pass2 = request.POST.get('pass2')
        
        # Check if username already exists
        if User.objects.filter(username=username).exists():
            messages.warning(request, 'Registration Unsuccessful!, This username is already taken. Please choose another one.')
            return redirect('register')  # Redirect back to the registration page

        # Check if email already exists
        if User.objects.filter(email=email).exists():
            messages.warning(request, 'Registration Unsuccessful!, This email is already registered. Please use another one.')
            return redirect('register')  # Redirect back to the registration page

        # Check if passwords match
        if pass1 != pass2:
            messages.warning(request, 'Passwords do not match. Please try again.')
            return redirect('register')  # Redirect back to the registration page

        customer = User.objects.create_user(username,email,pass1)
        customer.first_name = first_name
        customer.last_name = last_name

        customer.save()
        messages.success(request, f'You have successfully registered!')
        return redirect('login')
    
    return render(request,'Registration/auth.html')


def HandleLogin(request):
    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')
        
        user = authenticate(username=username,password=password)

        if user is not None:
            login(request,user)
            return redirect('home')
        else:
            messages.warning(request, f'Your Credentials did not match!,Try again.')
            return redirect('login')
    return render(request,'Registration/auth.html')


def HandleLogout(request):
    logout(request)
    return redirect('home')




@login_required(login_url="/login/")
def cart_add(request, id):
    cart = Cart(request)
    product = Product.objects.get(id=id)
    cart.add(product=product)
    return redirect("home")


@login_required(login_url="/login/")
def item_clear(request, id):
    cart = Cart(request)
    product = Product.objects.get(id=id)
    cart.remove(product)
    return redirect("cart_detail")


@login_required(login_url="/login/")
def item_increment(request, id):
    cart = Cart(request)
    product = Product.objects.get(id=id)
    cart.add(product=product)
    return redirect("cart_detail")


@login_required(login_url="/login/")
def item_decrement(request, id):
    cart = Cart(request)
    product = Product.objects.get(id=id)
    cart.decrement(product=product)
    return redirect("cart_detail")


@login_required(login_url="/login/")
def cart_clear(request):
    cart = Cart(request)
    cart.clear()
    return redirect("cart_detail")


@login_required(login_url="/login/")
def cart_detail(request):
    return render(request, 'Cart/cart_details.html')


def Check_out(request):
    amount_str = request.POST.get('amount')
    # print(amount_str)
    # amount_float = float(amount_str)
    # amount = int(amount_float)
    # print(amount)
    payment = client.order.create({
        "amount": 500, 
        "currency": "INR",
        "payment_capture" : "1"
    })


    order_id = payment['id']
    
    context = {
        'payment': payment,
        'order_id' : order_id 
    }
    return render(request,'Cart/checkout.html',context)

def PLACE_ORDER(request):

    context = {}

    if request.method == "POST":
        uid = request.session.get('_auth_user_id')
        user = User.objects.get(id = uid)
        cart = request.session.get('cart')
        firstname = request.POST.get('firstname')
        lastname = request.POST.get('lastname')
        country = request.POST.get('country')
        address = request.POST.get('address')
        city = request.POST.get('city')
        state = request.POST.get('state')
        postcode = request.POST.get('postcode')
        phone = request.POST.get('phone')
        email = request.POST.get('email')
        order_id = request.POST.get('order_id')
        payment = request.POST.get('payment')
        amount = request.POST.get('amount')
         
        context['order_id'] = order_id
        # print(user,firstname,lastname,country,address,city,state,postcode,phone,email,order_id,payment)

        order = Order(
            user = user,
            firstname = firstname,
            lastname = lastname,
            country = country,
            city = city,
            address = address,
            state = state,
            postcode = postcode,
            phone = phone,
            email = email,
            payment_id = order_id,
            amount = amount,
        )
        order.save()

        for i in cart:
            a = (int(cart[i]['price']))
            b = cart[i]['quantity']
            total = a*b
            item = OrderItem(
                order = order,
                product = cart[i]['name'],
                image = cart[i]['image'],
                quantity = cart[i]['quantity'], 
                price =  cart[i]['price'],
                total = total,
            )

            item.save()
        
    return render(request,'Cart/placeorder.html',context)

@csrf_exempt
def SUCCESS(request):
    if request.method == "POST":
        logger.info(f"User  authenticated before payment: {request.user.is_authenticated}")
        a = request.POST
        order_id = ""
        for key,val in a.items():
            if key == 'razorpay_order_id':
                order_id = val
                break
        user = Order.objects.filter(payment_id = order_id).first()
        # user.paid = True
        # user.save()
        logger.info(f"User  authenticated after payment: {request.user.is_authenticated}")
    return render(request,'Cart/thank_you.html')