from django.db import models
from django.core.validators import MinValueValidator


class SpecificationCategory(models.Model):
    """规格类目表"""
    id = models.AutoField(primary_key=True, verbose_name="商品ID")
    name = models.CharField(max_length=50, verbose_name="规格类目名称")
    cid = models.CharField(max_length=50, verbose_name="类目编号")

    class Meta:
        db_table = 'spec_category'
        verbose_name = '商品规格类目'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.name


class Product(models.Model):
    """商品表"""
    id = models.AutoField(primary_key=True, verbose_name="商品ID")
    price = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        validators=[MinValueValidator(0)],
        verbose_name="商品价格"
    )
    stock = models.PositiveIntegerField(default=0, verbose_name="商品库存")

    # 一对多关联规格类目
    spec_category = models.ForeignKey(
        SpecificationCategory,
        on_delete=models.PROTECT,
        related_name='products',  # 注意改为复数形式
        verbose_name="规格类目"
    )
    image = models.CharField(
        max_length=500,
        blank=True,
        null=True,
        verbose_name="商品主图URL"
    )
    selling_points = models.CharField(
        max_length=200,
        blank=True,
        verbose_name="商品卖点"
    )
    description = models.TextField(verbose_name="商品详情描述")

    # 自动记录时间
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="创建时间")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="更新时间")

    class Meta:
        db_table = 'product'
        verbose_name = '商品信息'
        verbose_name_plural = verbose_name
        ordering = ['-created_at']

    def __str__(self):
        return f"商品{self.id}（库存：{self.stock}）"
