from django.contrib import admin

# Register your models here.
from .models import Product, SpecificationCategory  # 导入你的模型

# 注册商品模型
@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('id', 'price', 'stock', 'spec_category')
    search_fields = ('selling_points', 'description')

# 注册规格类目模型
@admin.register(SpecificationCategory)
class SpecCategoryAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'cid')