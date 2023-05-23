from rest_framework import serializers
from django.contrib.auth.models import User
from .models import Recipe, Rating, Review, Favorite


class RecipeSerializer(serializers.ModelSerializer):

    class Meta:
        model = Recipe
        exclude = ['created_at', 'updated_at']


class RatingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Rating
        exclude = ['created_at', 'updated_at']


class ReviewSerializer(serializers.ModelSerializer):
    class Meta:
        model = Review
        exclude = ['created_at', 'updated_at']


class FavoriteSerializer(serializers.ModelSerializer):
    recipe_id = serializers.PrimaryKeyRelatedField(queryset=Recipe.objects.all(), source='recipe', write_only=True)
    author_id = serializers.PrimaryKeyRelatedField(queryset=User.objects.all(), source='author', write_only=True)
    class Meta:
        model = Favorite
        exclude = ['created_at', 'updated_at']


