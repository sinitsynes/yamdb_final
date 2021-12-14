import datetime as dt

from rest_framework import serializers
from rest_framework.relations import SlugRelatedField
from rest_framework.validators import UniqueTogetherValidator

from django.contrib.auth import get_user_model
from django.contrib.auth.tokens import default_token_generator
from django.db.models import Avg
from django.shortcuts import get_object_or_404

from reviews.models import Category, Genre, Title, Review, Comment

User = get_user_model()


class BasicUserSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = (
            'username',
            'email',
            'first_name',
            'last_name',
            'bio',
            'role'
        )
        read_only_fields = ('role',)

        validators = [
            UniqueTogetherValidator(
                queryset=User.objects.all(),
                fields=('username', 'email')
            )
        ]

    def validate_username(self, value):
        if value == 'me':
            raise serializers.ValidationError(
                'Нельзя использовать username «me»'
            )
        return value


class FullUserSerializer(BasicUserSerializer):

    class Meta(BasicUserSerializer.Meta):
        read_only_fields = None


class SignupSerializer(BasicUserSerializer):
    username = serializers.CharField()
    email = serializers.EmailField(max_length=254)

    class Meta(BasicUserSerializer.Meta):
        fields = (
            'username',
            'email'
        )
        validators = []

    def validate(self, data):
        try:
            User.objects.get(
                username=data.get('username'),
                email=data.get('email')
            )
        except User.DoesNotExist:
            serializer = BasicUserSerializer(data=data)
            serializer.is_valid(raise_exception=True)
        return data


class ActivationCodeSerializer(serializers.Serializer):
    confirmation_code = serializers.CharField()
    username = serializers.CharField()

    class Meta:
        fields = ('username', 'confirmation_code')

    def validate(self, data):
        user = get_object_or_404(User, username=data.get('username'))
        code_is_valid = default_token_generator.check_token(
            user=user,
            token=data.get('confirmation_code')
        )
        if not code_is_valid:
            raise serializers.ValidationError(
                'Код подтверждения не валиден'
            )
        return data


class CategorySerializer(serializers.ModelSerializer):

    class Meta:
        fields = ('name', 'slug')
        model = Category


class GenreSerializer(serializers.ModelSerializer):

    class Meta:
        fields = ('name', 'slug')
        model = Genre


class TitleSerializer(serializers.ModelSerializer):
    genre = SlugRelatedField(
        queryset=Genre.objects.all(), slug_field='slug', many=True)
    category = SlugRelatedField(
        queryset=Category.objects.all(), slug_field='slug')
    rating = serializers.SerializerMethodField()

    class Meta:
        fields = (
            'id', 'name', 'year', 'rating',
            'description', 'genre', 'category'
        )
        read_only_fields = ('rating',)
        model = Title

    def validate_year(self, value):
        current_year = dt.date.today().year
        if value > current_year:
            raise serializers.ValidationError(
                'Нельзя добавить фильм из будущего'
            )
        return value

    def get_rating(self, obj):
        reviews = Review.objects.filter(title=obj.id)
        if not reviews.exists():
            return None
        return round(reviews.aggregate(Avg('score'))['score__avg'])

    def to_representation(self, instance):
        title = super().to_representation(instance)
        title['genre'] = GenreSerializer(instance.genre, many=True).data
        title['category'] = CategorySerializer(
            instance.category, source=title).data
        return title


class ReviewSerializer(serializers.ModelSerializer):
    author = serializers.SlugRelatedField(
        slug_field='username',
        read_only=True,
    )

    class Meta:
        fields = ('id', 'text', 'author', 'score', 'pub_date')
        model = Review

    def validate(self, data):
        request = self.context['request']
        if request.method != 'POST':
            return data
        title_id = self.context['view'].kwargs.get('title_id')
        if Review.objects.filter(
            title=title_id, author=request.user
        ).exists():
            raise serializers.ValidationError(
                'Вы можете оставлять только одно ревью'
            )
        return data


class CommentSerializer(serializers.ModelSerializer):
    author = serializers.SlugRelatedField(
        slug_field='username', read_only=True
    )

    class Meta:
        fields = ('id', 'text', 'author', 'pub_date')
        model = Comment
