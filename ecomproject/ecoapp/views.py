from django.shortcuts import render, redirect,get_object_or_404
from django.views.generic import TemplateView, View, CreateView,FormView, DetailView, ListView,UpdateView, DeleteView
from django.contrib.auth import authenticate, login, logout
from .models import *
from .forms import CheckoutForm,CustomerRegistrationForm , CustomerLoginForm, AdminLoginForm, ProductForm, PasswordForgotForm, PasswordResetForm, ProductUpdateForm
from django.urls import reverse_lazy,reverse
from django.db.models import Q
from django.core.paginator import Paginator
from django.http import JsonResponse
import requests
from .utils import password_reset_token
from django.core.mail import send_mail
from django.conf import settings
from django.http import HttpResponse, HttpResponseRedirect  
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from math import ceil



#for assigning the name of the customer in the admin panel

def index(request):
   
    return render(request, 'index.html')




def home3(request):
    #products = Product.get_all_products().order_by("-id")
    
    #n = len(products)
    #nSlides = n//4 + ceil((n/4)-(n//4))
    #params = {'no_of_slides':nSlides, 'range': range(1,nSlides),'product': products}
    #allProds = [[products, range(1, len(products)), nSlides],[products, range(1, len(products)), nSlides]]
    #params = {'allProds': allProds}
    allProds = []
    catprods = Product.objects.values('category', 'id').order_by("-id")
    cats = {item['category'] for item in catprods}
    for cat in cats:
        prod = Product.objects.filter(category=cat).order_by("-id")
        n = len(prod)
        nSlides = n // 4 + ceil((n / 4) - (n // 4))
        allProds.append([prod, range(1, nSlides), nSlides])

    # params = {'no_of_slides':nSlides, 'range': range(1,nSlides),'product': products}
    # allProds = [[products, range(1, nSlides), nSlides],
    #             [products, range(1, nSlides), nSlides]]
    params = {'allProds':allProds}
    

    return render(request, 'home3.html', params)



    
    
def aboutus(request):
    return render(request, 'aboutus.html')
def contact(request):
    url = request.META.get('HTTP_REFERER')
    
    if request.method == 'POST':  # check post
        form = ContactForm(request.POST)
        if form.is_valid():

               
            data = Contact()  # create relation with model
            data.identity = form.cleaned_data['identity']
            data.email = form.cleaned_data['email']
            data.number = form.cleaned_data['number']
            data.message = form.cleaned_data['message']
           
            data.save()  # save data to table
           
            messages.success(request, "Your message is sent to E-Mart. Thank you for your interest.")
            return HttpResponseRedirect(url)

    return HttpResponseRedirect(url)
    


def addcomment(request,id):
    url = request.META.get('HTTP_REFERER')
    

    if request.method == 'POST':  # check post
        form = CommentForm(request.POST)

        if form.is_valid():
            data = Comment()  # create relation with model
            data.subject = form.cleaned_data['subject']
            data.comment = form.cleaned_data['comment']
            data.rate = form.cleaned_data['rate']
            data.ip = request.META.get('REMOTE_ADDR')
            data.product_id=id
            current_user= request.user
            data.user_id=current_user.id
            data.save()  # save data to table
            messages.success(request, "Your review has ben sent. Thank you for your interest.")
            return HttpResponseRedirect(url)
    return HttpResponseRedirect(url)
    

class EcoMixin(object):
    def dispatch(self, request, *args, **kwargs):
        cart_id = request.session.get("cart_id")
        if cart_id:
            cart_obj = Cart.objects.get(id=cart_id)
            
            if request.user.is_authenticated and request.user.customer:
                cart_obj.customer = request.user.customer
                cart_obj.save()
        return super().dispatch(request, *args, **kwargs)



# Create your views here.
class HomeView(EcoMixin,TemplateView):
    

    template_name = "home.html"


    def get_context_data(self, **kwargs):
            
        product_list = None
        
        categoryID = self.request.GET.get('category')
        if categoryID:
            product_list = Product.get_all_products_by_categoryid(categoryID)
            
        else:
            product_list = Product.get_all_products()



        context = super().get_context_data(**kwargs)
        all_products = Product.get_all_products_by_categoryid(categoryID).order_by("-id")
        paginator = Paginator(all_products,20)
        page_number = self.request.GET.get('page')
        product_list = paginator.get_page(page_number)



        
        context['product_list'] = product_list
        context['categories'] = Category.objects.all()
            
        return context

class HomeAgeView(EcoMixin,TemplateView):
    

    template_name = "home2.html"


    def get_context_data(self, **kwargs):
            
        product_list = None
        
        categoryID = self.request.GET.get('category')
        if categoryID:
            product_list = Product.get_all_products_by_categoryid(categoryID)
            
        else:
            product_list = Product.get_all_products()



        context = super().get_context_data(**kwargs)
        all_products = Product.get_all_products_by_categoryid(categoryID).order_by("-id")
        paginator = Paginator(all_products,12)
        page_number = self.request.GET.get('page')
        product_list = paginator.get_page(page_number)
        



        
        context['product_list'] = product_list
        context['categories'] = Category.objects.all()
            
        return context





def add_to_wishlist(request, id):
    product = get_object_or_404(Product, id = id)
    if product.users_wishlist.filter(id=request.user.id).exists():
        product.users_wishlist.remove(request.user)
        messages.success(request,  product.title + " has been removed from your wishlist")
    else:
        product.users_wishlist.add(request.user)
        messages.success(request, " Added " + product.title + " to your wishlist!! Visit your profile to know your wishlist")

    return HttpResponseRedirect(request.META["HTTP_REFERER"])





def wishlist(request):
    products = Product.objects.filter(users_wishlist=request.user)

    return render(request,"user_wishlist.html" , {"wishlist":products})










class AboutView(EcoMixin,TemplateView):
    template_name = "about.html"


class ContactView(EcoMixin,TemplateView):
    template_name = "contact.html"

class AllProductView(EcoMixin,TemplateView):
    template_name = "allproducts.html"
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["allcategories"] = Category.objects.all()
        return context
    
class ProductDetailView(EcoMixin,TemplateView):
    template_name = "productdetail.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        url_slug = self.kwargs['slug']
        product = Product.objects.get(slug=url_slug)
        product.view_count += 1
        product.save()

        context["product"] = product
        return context
class ProductDetailPageView(EcoMixin,DetailView):
    queryset = Product.objects.all()
    context_object_name = "object_list"
    template_name = "productdetailpage2.html"


    def get_context_data(self,*args, **kwargs):
        context = super(ProductDetailPageView,self).get_context_data(*args,**kwargs)

        

        ProductID = self.request.GET.get('product')
        
    
       
       
       
        url_slug = self.kwargs['slug']
        product = Product.objects.get(slug=url_slug)
        
        
        
        
      
        
        product.view_count += 1
        product.save()
        context["comments"] = Comment.objects.filter(product=self.object)

        context["product"] = product
        return context

    


class AddToCartView(EcoMixin,TemplateView):
    template_name = "addtocart.html"
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        #get product id from requested url
        product_id = self.kwargs['pro_id']
        #get product according to the url
        product_object= Product.objects.get(id = product_id)
        #checking if the cart exits or not
        #Django provides full support for anonymous sessions. The session framework lets you store and retrieve arbitrary data on a per-site-visitor basis. It stores data on the server side and abstracts the sending and receiving of cookies.
        cart_id = self.request.session.get("cart_id",None) 
        if cart_id:
            cart_obj = Cart.objects.get(id = cart_id)
            this_product_in_cart = cart_obj.cartproduct_set.filter(product=product_object)
            #if items already exists in cart
            if this_product_in_cart.exists():
                cartproduct = this_product_in_cart.last()
                cartproduct.quantity += 1
                cartproduct.subtotal += product_object.selling_price
                cartproduct.save()
                cart_obj.total += product_object.selling_price
                cart_obj.save()
            #new items added to cart
            else:
                cartproduct = CartProduct.objects.create(cart=cart_obj, product=product_object, quantity=1, subtotal=product_object.selling_price,rate=product_object.selling_price)
                cart_obj.total += product_object.selling_price
                cart_obj.save()




        else: 
            cart_obj = Cart.objects.create(total=0)
            self.request.session['cart_id'] = cart_obj.id
            cartproduct = CartProduct.objects.create(cart=cart_obj, product=product_object, quantity=1, subtotal=product_object.selling_price, rate=product_object.selling_price)
            cart_obj.total += product_object.selling_price
            cart_obj.save()

            

        
        return context



class ManageCartView(EcoMixin,View):
    def get(self, request, *args , **kwargs):
        cp_id = self.kwargs["cp_id"]
        action = request.GET.get("action")
        cp_obj = CartProduct.objects.get(id=cp_id)
        cart_obj = cp_obj.cart
        if action == "inc":
            cp_obj.quantity +=1
            cp_obj.subtotal += cp_obj.rate
            cp_obj.save()
            cart_obj.total += cp_obj.rate 
            cart_obj.save()

        elif action == "dcr":
            cp_obj.quantity -=1
            cp_obj.subtotal -= cp_obj.rate
            cp_obj.save()
            cart_obj.total -= cp_obj.rate 
            cart_obj.save()
            if cp_obj.quantity == 0:
                cp_obj.delete()
            
        elif action == "rmv":
            cart_obj.total -= cp_obj.subtotal
            cart_obj.save()
            cp_obj.delete()
        else:
            pass


        return redirect("ecoapp:mycart")


def  index(request):
    return render(request,"index.html")



    
class MyCartView(EcoMixin,TemplateView):
    template_name = "mycart.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        cart_id = self.request.session.get("cart_id",None)
        if cart_id :
            cart = Cart.objects.get(id=cart_id)
        else:
            cart = None
        context['cart'] = cart

        return context

class EmptyCartView(EcoMixin,View):
    def get(self, request, *args , **kwargs):
        cart_id = request.session.get("cart_id",None)
        if cart_id:
            cart = Cart.objects.get(id=cart_id)
            cart.cartproduct_set.all().delete()
            cart.total = 0
            cart.save()
        return redirect("ecoapp:mycart")


    




class CheckoutView(EcoMixin,CreateView):
    template_name = "checkout.html"
    form_class = CheckoutForm
    success_url = reverse_lazy("ecoapp:mycart")
    #dispatch function is used for activating the current code before the next code.
    def dispatch(self,request,*args, **kwargs):
        if request.user.is_authenticated and request.user.customer:
            pass
        else:
            return redirect("/login/?next=/checkout/")



        return super().dispatch(request,*args,**kwargs)
    




    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        cart_id = self.request.session.get("cart_id",None)
        if cart_id:
            cart_obj = Cart.objects.get(id=cart_id)
        
        else:
            cart_obj = None
        context["cart"] = cart_obj
        return context

    def form_valid(self, form):
        cart_id = self.request.session.get('cart_id')
        if cart_id:
            cart_obj = Cart.objects.get(id = cart_id)
            form.instance.cart = cart_obj
            form.instance.subtotal = cart_obj.total
            form.instance.discount = 0
            form.instance.total = cart_obj.total 
            form.instance.order_status = "Order Received"
            del self.request.session["cart_id"]
            pem = form.cleaned_data.get("payment_method")
            order = form.save()
            if pem == "Khalti Payment":
                return redirect(reverse("ecoapp:khaltirequest") + "?o_id=" + str(order.id))

           

        else:
            return redirect("ecoapp:home")
        return super().form_valid(form)
class KhaltiRequestView(View):
    def get(self,request,*args, **kwargs):
        o_id = request.GET.get("o_id")
        order = Order.objects.get(id=o_id)
        context = {
            "order": order

        }
        return render(request, "khaltirequest.html",context)


class KhaltiVerifyView(View):
    def get(self,request,*args, **kwargs):
        token = request.GET.get("token")
        amount = request.GET.get("amount")
        o_id = request.GET.get("order_id")
        print(token,amount,o_id)
        url = "https://khalti.com/api/v2/payment/verify/"
        payload = {
            "token": token,
            "amount": amount

        }
        headers = {

            "Authorization" : "Key test_secret_key_7d342bc1ddc946769ec2f760882e5efc"
        }

        
        order_obj = Order.objects.get(id=o_id)

        response = requests.post(url, payload, headers = headers)
        resp_dict = response.json()
        if resp_dict.get("idx"):
            success = True
            order_obj.payment_completed = True
            order_obj.save()
        else:
            success = False
                

        data = {
            "success" : success
         

        }
        return JsonResponse(data)


class CustomerRegistrationView(CreateView):
    template_name = "customerregistration.html"
    form_class = CustomerRegistrationForm
    success_url = reverse_lazy("ecoapp:home3")

    def form_valid(self, form):
        username = form.cleaned_data.get("username")
        password = form.cleaned_data.get("password")
        email = form.cleaned_data.get("email")
        user = User.objects.create_user(username,email,password)
        form.instance.user = user
        login(self.request, user)

        return super().form_valid(form)


    def get_success_url(self):
        if "next" in self.request.GET:

            next_url = self.request.GET.get("next")
            return next_url

        else:
            return self.success_url

class CustomerLogoutView(View):
    def get(self, request):
        logout(request)
        return redirect("ecoapp:home")

class CustomerLoginView(FormView):
    template_name = "customerlogin.html"
    form_class = CustomerLoginForm
    success_url = reverse_lazy("ecoapp:home3")
    #form valid method is a type ofpost method and is available in createview, formview and updateview

    def form_valid(self,form):
        uname = form.cleaned_data.get("username")
        pword = form.cleaned_data.get("password")
        usr = authenticate(username=uname, password= pword)
        if usr is not None and Customer.objects.filter(user=usr).exists():
            login(self.request,usr)
        else:
            return render(self.request, self.template_name, {"form":self.form_class,"error":"Invalid Credentials"})
        return super().form_valid(form)


    def get_success_url(self):
        if "next" in self.request.GET:
            next_url = self.request.GET.get("next")
            return next_url

        else:
            return self.success_url



class CustomerProfileView(TemplateView):
    template_name = "customerprofile.html"
    def dispatch(self,request,*args, **kwargs):
        if request.user.is_authenticated and Customer.objects.filter(user=request.user).exists():
            pass
        else:
            return redirect("/login/?next=/profile/")



        return super().dispatch(request,*args,**kwargs)


    def get_context_data(self, **kwargs):
         context = super().get_context_data(**kwargs)
         customer = self.request.user.customer
         context["customer"] = customer
         orders = Order.objects.filter(cart__customer=customer).order_by("-id")
         context["orders"] = orders
         return context
     
class CustomerOrderDetailView(DetailView):

    template_name = "customerorderdetail.html"
    model = Order
    context_object_name = "ord_obj"

    def dispatch(self,request,*args, **kwargs):
        if request.user.is_authenticated and Customer.objects.filter(user=request.user).exists():
            order_id = self.kwargs["pk"]
            order = Order.objects.get(id=order_id)
            if request.user.customer != order.cart.customer:
                return redirect("ecoapp:customerprofile")

        else:
            return redirect("/login/?next=/profile/")



        return super().dispatch(request,*args,**kwargs)
class SearchView(TemplateView):
    template_name = "search.html"
     
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        kw = self.request.GET.get('keyword')
        results = Product.objects.filter(Q(title__icontains=kw) | Q(description__icontains=kw))
        context["results"] = results
        return context
class SearchBaseView(TemplateView):
    template_name = "searchbase.html"
     
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        kw = self.request.GET.get('keyword')
        results = Product.objects.filter(Q(title__icontains=kw) | Q(description__icontains=kw))
        context["results"] = results
        return context

class PasswordForgotView(FormView):
    template_name = "forgotpassword.html"
    form_class = PasswordForgotForm
    success_url = "/forgot-password/?m=s"

    def form_valid(self, form):
        email = form.cleaned_data.get("email")
        url = self.request.META['HTTP_HOST']
        # get customer and then user
        customer = Customer.objects.get(user__email=email)
        user = customer.user
        # send mail to the user with email
        text_content = 'Please Click the link below to reset your password. '
        html_content = url + "/password-reset/" + email + \
            "/" + password_reset_token.make_token(user) + "/"
        send_mail(
            'Password Reset Link | E-Mart',
            text_content + html_content,
            settings.EMAIL_HOST_USER,
            [email],
            fail_silently=False,
        )
        return super().form_valid(form)

class PasswordResetView(FormView):
    template_name = "passwordreset.html"
    form_class = PasswordResetForm
    success_url = "/login/"

    def dispatch(self, request, *args, **kwargs):
        email = self.kwargs.get("email")
        user = User.objects.get(email=email)
        token = self.kwargs.get("token")
        if user is not None and password_reset_token.check_token(user, token):
            pass
        else:
            return redirect(reverse("ecomapp:passwordforgot") + "?m=e")

        return super().dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        password = form.cleaned_data['new_password']
        email = self.kwargs.get("email")
        user = User.objects.get(email=email)
        user.set_password(password)
        user.save()
        return super().form_valid(form)



    
###############################################################################################Admin view#############################################################################
class AdminLoginView(FormView):
    template_name = "adminpages/adminlogin.html"
    form_class = AdminLoginForm
    success_url = reverse_lazy("ecoapp:adminhome")


    def form_valid(self,form):
        uname = form.cleaned_data.get("username")
        pword = form.cleaned_data.get("password")
        usr = authenticate(username=uname, password= pword)
        if usr is not None and Admin.objects.filter(user=usr).exists():
            login(self.request,usr)
        else:
            return render(self.request, self.template_name, {"form":self.form_class,"error":"Invalid Credentials"})

        return super().form_valid(form)

     

        

#adminrequiredmixin: is used for only for admin view for that operation
class AdminRequiredMixin(object):
     def dispatch(self,request,*args, **kwargs):
        if request.user.is_authenticated and Admin.objects.filter(user=request.user).exists():
            pass
        else:
            return redirect("/admin-login/")



        return super().dispatch(request,*args,**kwargs)

class AdminMessageView(AdminRequiredMixin,TemplateView):

    template_name = "adminpages/adminmessage.html"
    

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["message"] = Contact.objects.all().order_by("-id")
        messages.success(self.request, "Your response  is sent to the customer.")
        return context
    



  


class AdminHomeView(AdminRequiredMixin,TemplateView):
    template_name = "adminpages/adminhome.html"
    


    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["pendingorders"] = Order.objects.filter(order_status="Order Received").order_by("-id")
        return context


class AdminOrderDetailView(AdminRequiredMixin,DetailView):
    template_name = "adminpages/orderdetailpage.html"
    model = Order
    context_object_name = "ord_obj"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["allstatus"] = ORDER_STATUS
        return context
    



class AdminOrderListView(AdminRequiredMixin,ListView):
    template_name = "adminpages/adminorderlist.html"
    queryset = Order.objects.all().order_by("-id")
    context_object_name = "allorders"

class AdminOrderStatusChangeView(AdminRequiredMixin, View):
    def post(self, request, *args, **kwargs):
        order_id = self.kwargs["pk"]
        order_obj = Order.objects.get(id=order_id)
        new_status = request.POST.get("status")
        order_obj.order_status = new_status
        order_obj.save()
        return redirect(reverse_lazy("ecoapp:orderdetailpage", kwargs={"pk": order_id}))

        
class AdminProductView(AdminRequiredMixin, ListView):
    template_name = "adminpages/adminproductlist.html"
    queryset = Product.objects.all().order_by("-id")
    context_object_name = "allproducts"

class AdminProductCreateView(AdminRequiredMixin, CreateView):
    template_name = "adminpages/adminproductcreate.html"
    form_class = ProductForm
    success_url = reverse_lazy("ecoapp:adminproductlist")


    def form_valid(self, form):
        p = form.save()
        images = self.request.FILES.getlist("more_images")
        for i in images:
            ProductImage.objects.create(product=p, image=i)

        return super().form_valid(form)



class ProductUpdateView(AdminRequiredMixin,UpdateView):
    
    model = Product  # required
    template_name = 'adminpages/adminproductupdate.html'
    form_class = ProductUpdateForm
    success_url = reverse_lazy("ecoapp:adminproductlist")

    def get_queryset(self):
        queryset = Product.objects.all()
        
        return queryset.all()

    def get_success_url(self):
        return reverse_lazy(
            'ecoapp:adminproductlist'
        )

 
def product_delete_view(request, id):
    obj = get_object_or_404(Product, id=id)
    if request.method == "POST":
        obj.delete()
        return redirect('ecoapp:adminproductlist')

    context ={
        "object":obj
    }
    return render(request,"adminpages/product_delete.html", context)


class AdminLogoutView(View):
    def get(self, request):
        logout(request)
        return redirect("ecoapp:home")