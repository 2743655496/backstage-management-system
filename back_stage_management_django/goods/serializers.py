from rest_framework import serializers
from .models import SpecificationCategory, Product


class SpecificationCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = SpecificationCategory
        fields = '__all__'
        # 或者指定字段：
        # fields = ['id', 'name', 'cid']
        extra_kwargs = {
            'id': {'read_only': True}  # ID是自动生成的，设为只读
        }


class ProductSerializer(serializers.ModelSerializer):
    # 嵌套显示完整的规格类目信息
    spec_category = SpecificationCategorySerializer(read_only=True)

    # 如果只需要显示规格类目ID（而不是整个对象），可以这样：
    spec_category_id = serializers.PrimaryKeyRelatedField(
        queryset=SpecificationCategory.objects.all(),
        source='spec_category',
        write_only=True
    )

    class Meta:
        model = Product
        fields = '__all__'
        # 或者明确指定字段：
        # fields = [
        #     'id', 'price', 'stock', 'spec_category',
        #     'image', 'selling_points', 'description',
        #     'created_at', 'updated_at'
        # ]
        extra_kwargs = {
            'id': {'read_only': True},
            'created_at': {'read_only': True},
            'updated_at': {'read_only': True}
        }

    # 自定义验证示例（可选）
    def validate_price(self, value):
        if value <= 0:
            raise serializers.ValidationError("价格必须大于0")
        return value

    def validate_stock(self, value):
        if value < 0:
            raise serializers.ValidationError("库存不能为负数")
        return value