from django.shortcuts import render,HttpResponse,redirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout

from productapp.models import Product, Cart, Order
from django.db.models import Q
import random
import razorpay

# Create your views here.
def demo(request):
    return HttpResponse("welcome")

def homePage(request):
    # userid=request.user.id
    # print('The login user id is:',userid)
    context={}
    p=Product.objects.filter(is_active=True)
    context['products']=p
    print('status: ',request.user.is_authenticated)
    return render(request,'home.html',context)

def catfilter(request,catval):
    context={}
    # p=Product.objects.filter(cat=catval)
    # context['products']=p
    # print('status: ',request.user.is_authenticated)
    q1=Q(is_active=True)
    q2=Q(cat=catval)
    p=Product.objects.filter(q1 & q2)
    context['products']=p
    return render(request,'home.html',context)

def register(request):
    if request.method == "POST":
        context={}
        uname=request.POST['uname']
        upass = request.POST['upass']
        cpass = request.POST['cpass']
        # print(uname,upass,cpass)
        # user = User.objects.create(password=upass,username=uname,email=uname)
        if uname=="" or upass=="" or cpass=="":
            context['errorMsg']='Field can not be empty'
            return render(request,'register.html',context)
        elif upass != cpass:
            context['errorMsg']='Password must match with confirm Password'
            return render(request,'register.html',context)
        else:
            user = User.objects.create(username=uname,email=uname)
            # print(user.id)
            user.set_password(upass)#for encrypted password
            user.save()
            context['success']='User registered successfully!!! Please Login'
            return render(request,'login.html',context)
    else: #to display empty form, in case of GET request
        return render(request,'register.html')

def user_login(request):
    if request.method=="GET":
        return render(request,'login.html')
    else: #POST
        context={}
        uname=request.POST['uname']
        upass=request.POST['upass']
        print(uname,upass)
        if uname=="" or upass=="":
            context['errorMsg']="Fields can not be blank"
            return render(request,'login.html',context)
        else:
            u=authenticate(username=uname,password=upass)
            # print(u) # print('passw: ',u.password)  # print('super? ',u.is_superuser)
            #here, u represents the entire row, and we can access individual fields like
            # u.email (model property)
            # u.password (model property) 
            if u is not None:
                login(request,u)#starts session, and stores id of user in session
                return redirect('/home')
            else:
                context['errorMsg']='Invalid username or password'
                return render(request,'login.html',context)

def user_logout(request):
    logout(request)
    # return render(request,'home.html') dont use this, 
    return redirect('/home')
   
def about(request):
    return render(request,'about.html')

def sort(request,sv):
    if sv=='0':
        col='price'
    else:
        col='-price'
    context={}
    p=Product.objects.filter(is_active=True).order_by(col)
    context['products']=p
    return render(request,'home.html',context)

def range(request):
    min = request.GET['min']
    max = request.GET['max']
    q1=Q(price__gte=min)
    q2=Q(price__lte=max)
    q3=Q(is_active=True)
    p = Product.objects.filter(q1 & q2 & q3).all()
    context={}
    context['products']=p
    return render(request,'home.html',context)

def contact(request):
    return render(request,'contact_us.html')

def showDetails(request,pid):
    p = Product.objects.filter(id=pid)
    context = {}
    context['product'] = p[0]
    return render(request,'details.html',context)

def addToCart(request,pid):
    userid = request.user.id
    if userid:
        print('userid:',userid)
        u = User.objects.filter(id = userid)
        p = Product.objects.filter(id = pid)
        print(u,'\n',u[0])
        print(p,'\n',p[0])
        c = Cart.objects.create(uid=u[0],pid=p[0])
        c.save()
        return HttpResponse('added to cart')
    else:
        context={}
        context['errorMsg']='Please login to add to cart'
        return render(request,'login.html')

def showMyCart(request):
    context = {}
    userid = request.user.id    
    u = User.objects.filter(id = userid)
    c = Cart.objects.filter(uid = u[0])
    context['mycart'] = c
    count = len(c)
    billAmount =0
    for cart in c:
        billAmount += cart.pid.price * cart.quantity    
    context['count'] = count
    context['billAmount'] = billAmount
    return render(request,'mycart.html',context)

def updateQuantity(request,incr,cid):       
    c = Cart.objects.filter(id=cid)
    if incr == '0':
        c.update(quantity = c[0].quantity-1)
    else:
        c.update(quantity = c[0].quantity+1)
    return redirect('/mycart')

def deleteCart(request, cid):
    c = Cart.objects.filter(id=cid)
    c.delete()
    return redirect('/mycart')
    
def placeOrder(request):
    context={}
    userid = request.user.id
    order_id = random.randrange(1000,9999)
    #fetch current cart
    mycart = Cart.objects.filter(uid = userid)    
    #add the cart items to Order
    for cart in mycart:
        ord = Order.objects.create(order_id=order_id, sid = cart.pid,uid = cart.uid, quantity=cart.quantity)
        ord.save()
    mycart.delete() #clear cart table for current user 
    mycart = Order.objects.filter(order_id = order_id) #fetch order deatils
    #calculate count and total
    count = len(mycart)
    billAmount =0
    for cart in mycart:
        billAmount += cart.sid.price * cart.quantity  
    context['count'] = count
    context['billAmount'] = billAmount
    context['mycart']=mycart        
    return render(request,'placeorder.html',context)

def makepayment(request):
    #get the orderdetails for current loggedin user
    userid = request.user.id
    ordDetails = Order.objects.filter(uid = userid)
    #calculate the billamount
    bill=0
    for ord in ordDetails:
        bill += ord.sid.price * ord.quantity
        ordId = ord.order_id
    client = razorpay.Client(auth=("rzp_test_fZSr0rRCCCK3f6", "WlRA9peyeaFVTtYJRb3Rirx7"))
    data = { "amount": bill*100, "currency": "INR", "receipt": str(ordId) }
    payment = client.order.create(data=data)
    print(payment)
    # return HttpResponse("success")
    context={}
    context['data']=payment
    return render(request,'pay.html',context)











