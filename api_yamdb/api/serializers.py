from django.shortcuts import get_object_or_404
from rest_framework import serializers
from rest_framework.validators import UniqueTogetherValidator

from reviews.models import Category, Genre, Title, TitleGenre


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


class TitleCreateUpdateSerializer(serializers.ModelSerializer):
    """Сериализатор для модели Title."""
    genre = serializers.SerializerMethodField()
    raiting = serializers.SerializerMethodField()
    category = serializers.SlugRelatedField(queryset=Category.objects.all(), slug_field='slug')

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

    def get_genre(self, obj):
        genres = obj.genres.all()
        list_genre = []
        for genre in genres:
            serializer = GenreSerializer(genre.genre)
            list_genre.append(serializer.data)
        return list_genre

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        print(instance)
        representation['category'] = {'name': instance.category.name, 'slug': instance.category.slug}
        return representation

    def create(self, validated_data):
        print("!!!!!!", self.initial_data)
        print("22222", validated_data)
        if 'genre' not in self.initial_data:
            title = Title.objects.create(**validated_data)
            return title
        genres = self.initial_data.pop('genre')
        for genre in genres:
            print("GGGGG", genre)
            current_genre = get_object_or_404(Genre, slug=genre)
        title = Title.objects.create(**validated_data)
        for genre in genres:
            TitleGenre.objects.create(title=title, genre=current_genre)
        return title
