import requests
from rest_framework.serializers import ModelSerializer, SerializerMethodField, ValidationError
 
from shop.models import Category, Product, Article
 

class ArticleSerializer(ModelSerializer):
    
    class Meta:
        model = Article
        fields = ['id', 'date_created', 'date_updated', 'name', 'price', 'product',]

    def validate_name(self, value):
        if Article.objects.filter(name=value).exists():
            raise ValidationError('Category already exists')
        return value
        
    def validate_price(self, value):
        if value < 1:
            raise ValidationError("Price must be superior to 1€")
        return value


class ProductListSerializer(ModelSerializer):

    class Meta:
        model = Product
        fields = ['id', 'name', 'date_created', 'date_updated', 'ecoscore', 'category','active']

    def get_category(self):
        serializer = CategoryDetailSerializer(many=True) 
        return serializer.data
    

class ProductDetailSerializer(ModelSerializer):
    articles = SerializerMethodField()
    category = SerializerMethodField()
    class Meta:
        model = Product
        fields = ['id', 'date_created', 'date_updated', 'name', 'category', 'articles', 'description','ecoscore']

    def validate_name(self, value):
        return value





class CategoryListSerializer(ModelSerializer):
    class Meta:
        model = Category
        fields = ['id', 'name', 'date_created', 'date_updated', 'description']
        
    def validate_name(self, value):
        if Category.objects.filter(name=value).exists():
            raise ValidationError(value + 'Category already exists')
        return value
    # def validate(self, data):
    #     # Effectuons le contrôle sur la présence du nom dans la description
    #     if data['name'] not in data['description']:
    #     # Levons une ValidationError si ça n'est pas le cas
    #         raise ValidationError('Name must be in description')
    #     return data
    
class CategoryDetailSerializer(ModelSerializer):
 
    products = SerializerMethodField()
    class Meta:
        model = Category
        fields = ['id', 'description' ,'date_created', 'date_updated', 'name', 'products',]

    def get_products(self, instance):


        # On applique le filtre sur notre queryset pour n'avoir que les produits actifs
        queryset = instance.products.filter(active=True)
        # Le serializer est créé avec le queryset défini et toujours défini en tant que many=True
        serializer = ProductListSerializer(queryset, many=True)
        # la propriété '.data' est le rendu de notre serializer que nous retournons ici
        return serializer.data
    
class CategoryAllSerializer(ModelSerializer):
 
    products = SerializerMethodField()
    class Meta:
        model = Category
        fields = ['id', 'description' ,'date_created', 'date_updated', 'name', 'products',]

    def get_products(self, instance):
        queryset = instance.products.all()
        serializer = ProductListSerializer(queryset, many=True)
        return serializer.data