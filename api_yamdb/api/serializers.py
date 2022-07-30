from rest_framework import serializers
from rest_framework.validators import UniqueTogetherValidator
from reviews.models import Category, Genre, Title


class CategorySerializer(serializers.ModelSerializer):
    """Сериализатор для модели Category."""
    class Meta:
        fields = ('name', 'slug')
        model = Category


class GenreSerializer(serializers.ModelSerializer):
    """Сериализатор для модели Genre."""
    class Meta:
        fields = ('name', 'slug')
        model = Genre


class TitleReadSerializer(serializers.ModelSerializer):
    """Сериализатор для модели Title."""
    raiting = serializers.SerializerMethodField()
    genre = GenreSerializer(read_only=True, many=True)
    category = serializers.SlugRelatedField(queryset=Category.objects.all(),
                                            slug_field='slug')

    class Meta:
        fields = ('id', 'name', 'year', 'raiting', 'description', 'genre',
                  'category')
        model = Title

        validators = [

            UniqueTogetherValidator(
                queryset=Title.objects.all(),
                fields=['name', 'year'],
                message=("Произведение уже существует")
            )
        ]

    def get_raiting(self, obj):
        reviews = obj.reviews.all()
        sum = 0
        for review in reviews:
            sum += review.score
        if len(reviews) != 0:
            return int(sum / len(reviews))
        return 0

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        print(instance)
        representation['category'] = {'name': instance.category.name,
                                      'slug': instance.category.slug}
        return representation


class TitleCreateUpdateSerializer(serializers.ModelSerializer):
    """Сериализатор для модели Title."""
    raiting = serializers.SerializerMethodField()
    genre = serializers.SlugRelatedField(queryset=Genre.objects.all(),
                                         slug_field='slug', many=True)
    category = serializers.SlugRelatedField(queryset=Category.objects.all(),
                                            slug_field='slug')

    class Meta:
        fields = ('id', 'name', 'year', 'raiting', 'description', 'genre',
                  'category')
        model = Title

        validators = [

            UniqueTogetherValidator(
                queryset=Title.objects.all(),
                fields=['name', 'year'],
                message=("Произведение уже существует")
            )
        ]

    def get_raiting(self, obj):
        reviews = obj.reviews.all()
        sum = 0
        for review in reviews:
            sum += review.score
        if len(reviews) != 0:
            return int(sum / len(reviews))
        return 0

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation['category'] = {'name': instance.category.name,
                                      'slug': instance.category.slug}
        genres = instance.genre.all()
        i = 0
        for genre in genres:
            representation['genre'][i] = {'name': genre.name,
                                          'slug': genre.slug}
            i += 1
        genres = representation['genre']
        return representation
