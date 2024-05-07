from rest_framework import serializers
from .models import Product, Category, ProductImageUrl


class ProductSerializer(serializers.ModelSerializer):

    class Meta:
        model = Product
        fields = '__all__'

class ProductImageUrlSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductImageUrl
        fields = ['image']


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['id', 'name']


class ProductCreateSerializer(serializers.ModelSerializer):
    category = CategorySerializer()
    image_urls = ProductImageUrlSerializer(many=True, source='product')

    class Meta:
        model = Product
        fields = ['id', 'name', 'width', 'length', 'description', 'category', 'price', 'image_urls']

    def create(self, validated_data):

        image_urls_data = validated_data.pop('product')
        product = Product.objects.create(**validated_data)

        if image_urls_data:
            for image_data in image_urls_data:
                ProductImageUrl.objects.create(product=product, **image_data)

            return product


class ProductUpdateSerializer(serializers.ModelSerializer):
    image_urls = ProductImageUrlSerializer(many=True, source='product')

    class Meta:
        model = Product
        fields = ['id', 'name', 'width', 'length', 'description', 'category', 'price', 'image_urls']

    def update(self, instance, validated_data):
        image_urls_data = validated_data.pop('product')

        for field in ['name', 'width', 'length', 'description', 'category', 'price']:
            setattr(instance, field, validated_data.get(field, getattr(instance, field)))

        instance.save()

        # Handle ProductImageUrl updates
        existing_image_ids = [image['id'] for image in image_urls_data if 'id' in image]
        ProductImageUrl.objects.filter(product=instance).exclude(id__in=existing_image_ids).delete()

        for image_url_data in image_urls_data:
            image_id = image_url_data.get('id', None)
            image_url = image_url_data.get('image')

            if image_id:

                existing_image_url = ProductImageUrl.objects.get(id=image_id)
                existing_image_url.image = image_url
                existing_image_url.save()
            else:

                ProductImageUrl.objects.create(product=instance, image=image_url)

        return instance