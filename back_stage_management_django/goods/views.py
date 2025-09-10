from rest_framework import viewsets
from .models import SpecificationCategory, Product
from .serializers import SpecificationCategorySerializer, ProductSerializer

class SpecificationCategoryViewSet(viewsets.ModelViewSet):
    queryset = SpecificationCategory.objects.all()
    serializer_class = SpecificationCategorySerializer

class ProductViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer

