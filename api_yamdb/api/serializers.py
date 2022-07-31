from random import choice

from django.core.mail import send_mail
from rest_framework import serializers
from rest_framework.exceptions import ValidationError
from rest_framework.generics import get_object_or_404
from rest_framework.validators import UniqueTogetherValidator, UniqueValidator

from reviews.models import (ROLE_CHOICES, Category, Comment, Genre, Review,
                            Title, User)


class UserSerializer(serializers.ModelSerializer):
    """Сериализатор для модели user."""

    role = serializers.ChoiceField(choices=ROLE_CHOICES, default="user")

    class Meta:
        model = User
        fields = ("username", "email", "first_name",
                  "last_name", "bio", "role"
                  )


class UserMeSerializer(serializers.ModelSerializer):
    """Сериализатор для своей учётной записи users/me."""

    class Meta:
        model = User
        fields = ("username", "email", "first_name",
                  "last_name", "bio", "role"
                  )
        read_only_fields = ('username', "email", "role")


class AuthSignupSerializer(serializers.ModelSerializer):
    """Сериализатор для самостоятельной регистрации.
    И получения кода подтверждения"""

    email = serializers.EmailField(
        required=True,
        validators=[UniqueValidator(queryset=User.objects.all())]
    )
    confirmation_code = serializers.CharField(read_only=True)

    class Meta:
        model = User
        fields = ("username", "email", "confirmation_code")

    def to_representation(self, instance):
        return {
            'username': instance.username,
            'email': instance.email
        }

    def validate(self, data):
        if data['username'] == 'me':
            raise serializers.ValidationError(
                'Имя пользователя не может ME!')
        return data

    def generate_confirmation_code(self):
        pool = "1234567890"
        random_str = []
        for _ in range(4):
            random_str.append(choice(pool))
        return "".join(random_str)

    def create(self, validated_data):
        user = User(**validated_data)
        code = self.generate_confirmation_code()
        user.confirmation_code = code
        user.save()
        to_email = []
        to_email.append(validated_data["email"])
        send_mail(
            subject='YaMDB confirmation code',
            message=f' Your confirmation code is: {code}.',
            from_email='yamdb@yamdb.fake',
            recipient_list=to_email,
            fail_silently=False
        )
        return user


class AuthTokenSerializer(serializers.ModelSerializer):
    """Сериализатор для получения access-токена."""

    username = serializers.CharField(write_only=True)
    confirmation_code = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ("username", "confirmation_code")


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
    """Сериализатор для модели Title при GET-запросе."""

    rating = serializers.SerializerMethodField()
    genre = GenreSerializer(read_only=True, many=True)
    category = serializers.SlugRelatedField(queryset=Category.objects.all(),
                                            slug_field='slug')

    class Meta:
        fields = ('id', 'name', 'year', 'rating', 'description', 'genre',
                  'category')
        model = Title

        validators = [

            UniqueTogetherValidator(
                queryset=Title.objects.all(),
                fields=['name', 'year'],
                message=("Произведение уже существует")
            )
        ]

    def get_rating(self, obj):
        if not obj.reviews.all().exists():
            return
        reviews = obj.reviews.all()
        sum = 0
        for review in reviews:
            sum += review.score
        return int(sum / len(reviews))

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation['category'] = {'name': instance.category.name,
                                      'slug': instance.category.slug}
        return representation


class TitleCreateUpdateSerializer(serializers.ModelSerializer):
    """Сериализатор для модели Title при запросах POST, PATCH, DELETE."""

    rating = serializers.SerializerMethodField()
    genre = serializers.SlugRelatedField(queryset=Genre.objects.all(),
                                         slug_field='slug', many=True)
    category = serializers.SlugRelatedField(queryset=Category.objects.all(),
                                            slug_field='slug')

    class Meta:
        fields = ('id', 'name', 'year', 'rating', 'description', 'genre',
                  'category')
        model = Title

        validators = [

            UniqueTogetherValidator(
                queryset=Title.objects.all(),
                fields=['name', 'year'],
                message=("Произведение уже существует")
            )
        ]

    def validate(self, data):
        if 'genre' in self.initial_data:
            genres = data["genre"]
            for genre in genres:
                if not Genre.objects.filter(pk=genre.pk).exists():
                    raise ValidationError('Такого жанра в базе не'
                                          'существует')
        if 'category' in self.initial_data:
            category = data["category"]
            if not Category.objects.filter(pk=category.pk).exists():
                raise ValidationError('Такой категории в базе не'
                                      'существует')
        return data

    def get_rating(self, obj):
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


class ReviewSerializer(serializers.ModelSerializer):
    """Сериализатор для модели Review."""

    author = serializers.SlugRelatedField(
        default=serializers.CurrentUserDefault(),
        slug_field='username',
        read_only=True
    )

    def validate(self, data):
        request = self.context['request']
        author = request.user
        title_id = self.context['view'].kwargs.get('title_id')
        title = get_object_or_404(Title, pk=title_id)
        if request.method == 'POST':
            if Review.objects.filter(title=title, author=author).exists():
                raise ValidationError('Вы не можете добавить более'
                                      'одного отзыва на произведение')
        return data

    class Meta:
        model = Review
        fields = ('id', 'text', 'author', 'score', 'pub_date')


class CommentSerializer(serializers.ModelSerializer):
    """Сериализатор для модели Comment."""

    review = serializers.SlugRelatedField(
        slug_field='text',
        read_only=True
    )
    author = serializers.SlugRelatedField(
        slug_field='username',
        read_only=True
    )

    class Meta:
        model = Comment
        fields = '__all__'
