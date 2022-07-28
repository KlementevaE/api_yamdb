from rest_framework import serializers
# from rest_framework.relations import SlugRelatedField
# from rest_framework.validators import UniqueTogetherValidator
# from rest_framework_simplejwt.serializers import TokenObtainPairSerializer


from reviews.models import User


class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ("username", "email", "first_name",
                  "last_name", "bio", "role"
                  )


class AuthSignupSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(required=True)
    confirmation_code = serializers.CharField(read_only=True)

    class Meta:
        model = User
        fields = ("username", "email", "confirmation_code")

    def to_representation(self, instance):
        return {
            'username': instance.username,
            'email': instance.email
        }


class AuthTokenSerializer(serializers.ModelSerializer):
    username = serializers.CharField(write_only=True)
    confirmation_code = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ("username", "confirmation_code")
