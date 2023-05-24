from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.viewsets import ReadOnlyModelViewSet, ModelViewSet
from rest_framework.decorators import action
from rest_framework import status

from shop.models import Category, Product, Article
from shop.serializers import CategoryDetailSerializer, CategoryListSerializer, ProductListSerializer, ProductDetailSerializer, ArticleSerializer, CategoryAllSerializer
from shop.permissions import IsAdminAuthenticated, IsStaffAuthenticated
 
class MultipleSerializerMixin:

    detail_serializer_class = None

    def get_serializer_class(self):
        if self.action == 'retrieve' and self.detail_serializer_class is not None:
            return self.detail_serializer_class
        return super().get_serializer_class()


class CategoryViewset(MultipleSerializerMixin, ReadOnlyModelViewSet):
 
    serializer_class = CategoryListSerializer
    # Ajoutons un attribut de classe qui nous permet de définir notre serializer de détail
    detail_serializer_class = CategoryDetailSerializer
 
    def get_queryset(self):
        return Category.objects.filter(active=True)
 
    def get_serializer_class(self):
    # retrive == détail
        if self.action == 'retrieve':
            return self.detail_serializer_class
        return super().get_serializer_class()
    
    @action(detail=True, methods=['post'])
    def disable(self, request, pk):
        self.get_object().disable()
        return Response()



class ProductViewset(MultipleSerializerMixin, ReadOnlyModelViewSet):

    serializer_class = ProductListSerializer

    detail_serializer_class = ProductDetailSerializer

    def get_queryset(self):
        queryset = Product.objects.filter(active=True)
        category_id = self.request.GET.get('category_id')
        if category_id is not None:
            queryset = queryset.filter(category_id=category_id)
        return queryset
    def get_serializer_class(self):
        if self.action == 'retrieve':
            return self.detail_serializer_class
        return super().get_serializer_class()
    @action(detail=True, methods=['post'])
    def disable(self, request, pk):
        self.get_object().disable()
        return Response()
    
class ArticleViewset(ReadOnlyModelViewSet):
 
    serializer_class = ArticleSerializer
 
    def get_queryset(self):
        queryset = Article.objects.filter(active=True)
        product_id = self.request.GET.get('product_id')
        if product_id is not None:
            queryset = queryset.filter(product_id=product_id)
        return queryset
    @action(detail=True, methods=['post'])
    def disable(self, request, pk):
        self.get_object().disable()
        return Response()
    
class AdminProductViewset(MultipleSerializerMixin, ModelViewSet):
 
    serializer_class = ProductListSerializer
    detail_serializer_class = ProductDetailSerializer
    
    # permission_classes = [IsAdminAuthenticated, IsStaffAuthenticated]
 
    def get_queryset(self):
        return Product.objects.all()




class AdminCategoryViewset(MultipleSerializerMixin, ModelViewSet):
 
    serializer_class = CategoryListSerializer
    detail_serializer_class = CategoryDetailSerializer
    serializer_all_class = CategoryAllSerializer

    
    # permission_classes = [IsAdminAuthenticated, IsStaffAuthenticated]

    def get_serializer_class(self):
        if self.action == 'retrieve' and self.serializer_all_class is not None:
            return self.serializer_all_class
        return super().get_serializer_class()
    
    
    def get_queryset(self):
        return Category.objects.all()
    


class AdminArticlesViewset(MultipleSerializerMixin, ModelViewSet):
 
    serializer_class = ArticleSerializer
    
    permission_classes = [IsAdminAuthenticated, IsStaffAuthenticated]
 
    def get_queryset(self):
        return Article.objects.all()