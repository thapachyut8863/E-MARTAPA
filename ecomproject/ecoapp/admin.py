from django.contrib import admin
from .models import *


# Register your models here.
class CommentAdmin(admin.ModelAdmin):
    list_display = ['subject','comment', 'status','create_at']
    list_filter = ['status']
    readonly_fields = ('subject','comment','ip','user','product','rate','id')
    
admin.site.register(Comment,CommentAdmin)

admin.site.register([Admin, Customer, Category, Product, Cart, CartProduct ,Wish,WishProduct,Order,ProductImage,Contact])