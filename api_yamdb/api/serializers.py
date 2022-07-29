from random import choice
from django.core.mail import send_mail
from rest_framework import serializers
from rest_framework.validators import UniqueValidator

from reviews.models import User, ROLE_CHOICES


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
