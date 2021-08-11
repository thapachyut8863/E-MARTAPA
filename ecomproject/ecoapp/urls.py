from django.urls import path 
from .views import *
app_name = "ecoapp"
from .import views
from django.contrib.auth import views as auth_views
from django.conf.urls import url



urlpatterns = [
    #customer url patterns
    path("", views.index, name="index"),
    path("r'^home3/?$'", views.home3, name="home3"),
    path("aboutus/",views.aboutus, name="aboutus"),
   
    path("r'^addcomment/<int:id>/?$'", views.addcomment, name="addcomment"),
    path("contact/", views.contact, name="contact"),
    
    path("home",HomeView.as_view(),name="home"),
    
   
   
    path("about",AboutView.as_view(),name="about"),
    
    path("allproducts/", AllProductView.as_view(),name="allproducts"),
    path("product/<slug:slug>/", ProductDetailView.as_view(),name="productdetail"),
    path("product2/<slug:slug>/", ProductDetailPageView.as_view(),name="productdetailpage2"),
    
    
    

    path("add-to-cart-<int:pro_id>", AddToCartView.as_view(),name="addtocart"),
    
    path("my-cart",MyCartView.as_view(),name="mycart"),
   
    
    path("manage-cart/<int:cp_id>/",ManageCartView.as_view(),name="managecart"),
    
    path("empty-cart", EmptyCartView.as_view(),name="emptycart"),
    path("checkout/", CheckoutView.as_view(), name="checkout"),
    path("khalti-request/", KhaltiRequestView.as_view(), name="khaltirequest"),
    path("khalti-verify/", KhaltiVerifyView.as_view(), name="khaltiverify"),
    path("index",views.index, name="index"),
    path("register",CustomerRegistrationView.as_view(), name="customerregistration"),
    path("logout",CustomerLogoutView.as_view(), name ="customerlogout"),
    path("login/",CustomerLoginView.as_view(), name ="customerlogin"),
    
    path("profile/",CustomerProfileView.as_view(), name ="customerprofile"),
    path("profile/order-<int:pk>/",CustomerOrderDetailView.as_view(),name="customerorderdetail"),
    path("search/", SearchView.as_view(),name="search"),
    path("search2/", SearchBaseView.as_view(),name="searchbase"),
    path("forgot-password/", PasswordForgotView.as_view(), name="passwordforgot"),
    path("password-reset/<email>/<token>/", PasswordResetView.as_view(), name="passwordreset"),



    #admin url pattern
    path("admin-login/", AdminLoginView.as_view(), name="adminlogin"),
    path("admin-message/",AdminMessageView.as_view(),name="adminmessage"),
    path("admin-home/", AdminHomeView.as_view(),name="adminhome"),
    path("admin-order/<int:pk>/", AdminOrderDetailView.as_view(),name="orderdetailpage"),
    path("admin-all-orders/", AdminOrderListView.as_view(),name="adminorderlist"),
    path("admin-order-<int:pk>-change/", AdminOrderStatusChangeView.as_view(),name="adminorderstatuschange"),
    path("admin-product-list/", AdminProductView.as_view(), name="adminproductlist"),
    path("admin-product/add/",AdminProductCreateView.as_view(), name ="adminproductcreate"),
    path("productupdate/<pk>/", ProductUpdateView.as_view(), name="product-update"),
    path("products_delete/<int:id>/delete/", product_delete_view, name="product-delete"),
    path("adminlogout",AdminLogoutView.as_view(), name ="adminlogout"),


    #####for wish-list purpose#####################################################################################3
    path("wishlist1/add_to_wishlist/<int:id>/",views.add_to_wishlist, name = "user_wishlist"),
    
    path("wishlist", views.wishlist, name = "wishlist"),
   
   


  
    
]
