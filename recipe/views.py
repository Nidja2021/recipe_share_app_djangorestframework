import uuid

from rest_framework.views import APIView
from rest_framework import status
from rest_framework.request import Request
from rest_framework.response import Response

from .models import Recipe, Rating, Review, Favorites
from .serializers import RecipeSerializer, RatingSerializer, ReviewSerializer, FavoritesSerializer


class RecipeView(APIView):
    def get(self, request: Request):
        try:
            recipes = Recipe.objects.all()
            serializer = RecipeSerializer(recipes, many=True)
            return Response(
                { 'data': serializer.data },
                status=status.HTTP_200_OK
            )
        except Exception as e:
            print(e)
            return Response(
                {'data': {}},
                status=status.HTTP_400_BAD_REQUEST
            )

    def post(self, request: Request):
        try:
            data = request.data
            serializer = RecipeSerializer(data=data)
            if not serializer.is_valid():
                return Response(
                    {'data': {}, 'message': serializer.errors},
                    status=status.HTTP_400_BAD_REQUEST
                )
            serializer.save()
            return Response(
                {'data': serializer.data, 'message': 'Recipe has been created successfully.'},
                status=status.HTTP_201_CREATED
            )
        except Exception as e:
            print(e)
            return Response(
                {'data': {}, 'message': "Something was wrong."},
                status=status.HTTP_400_BAD_REQUEST
            )


class RecipeDetailView(APIView):
    def get(self, request: Request, pk: uuid):
        try:
            recipe = Recipe.objects.get(pk=pk)
        except Exception as e:
            return Response(
                {'message': 'Recipe not found.'},
                status=status.HTTP_404_NOT_FOUND
            )

        serializer = RecipeSerializer(recipe)
        return Response(
            {'data': serializer.data},
            status=status.HTTP_200_OK
        )

    def put(self, request: Request, pk: uuid):
        try:
            recipe = Recipe.objects.get(pk=pk)
        except Exception as e:
            return Response(
                {'message': 'Recipe not found.'},
                status=status.HTTP_404_NOT_FOUND
            )
        serializer = RecipeSerializer(recipe, data=request.data)
        if not serializer.is_valid():
            return Response(
                {'error': serializer.errors},
                status=status.HTTP_400_BAD_REQUEST
            )
        serializer.save()
        return Response(
            {'data': serializer.data},
            status=status.HTTP_200_OK
        )

    def patch(self, request: Request, pk: uuid):
        try:
            recipe = Recipe.objects.get(pk=pk)
            serializer = RecipeSerializer(recipe, data=request.data, partial=True)
            if not serializer.is_valid():
                return Response(
                    {'data': {}},
                    status=status.HTTP_400_BAD_REQUEST
                )
            serializer.save()
            return Response(
                {'data': serializer.data},
                status=status.HTTP_200_OK
            )
        except Exception as e:
            print(e)
            return Response(
                {'data': {}},
                status=status.HTTP_400_BAD_REQUEST
            )

    def delete(self, request: Request, pk: uuid):
        try:
            recipe = Recipe.objects.get(pk=pk)
        except Exception as e:
            return Response(
                {'message': 'Recipe not found.'},
                status=status.HTTP_404_NOT_FOUND
            )
        recipe.delete()
        return Response(
            {'message': 'Recipe has been deleted successfully.'},
            status=status.HTTP_204_NO_CONTENT
        )


class RatingView(APIView):
    def post(self, request: Request, recipe_id: uuid):
        try:
            recipe = Recipe.objects.get(pk=recipe_id)
        except Exception as e:
            print(e)
            return Response(
                {'message': 'Recipe not found'},
                status=status.HTTP_404_NOT_FOUND
            )
        data = request.data
        serializer = RatingSerializer(data=data)
        if not serializer.is_valid():
            return Response(
                {'error': serializer.errors},
                status=status.HTTP_400_BAD_REQUEST
            )
        serializer.save()
        return Response(
            {'data': serializer.data},
            status=status.HTTP_404_NOT_FOUND
        )


class RatingDetailView(APIView):
    def patch(self, request: Request, recipe_id: uuid, rating_id: uuid):
        try:
            rating = Recipe.objects.get(pk=rating_id, recipe_id=recipe_id)
        except Exception as e:
            print(e)
            return Response(
                {'message': 'Recipe or Rating not found'},
                status=status.HTTP_404_NOT_FOUND
            )
        serializer = RatingSerializer(rating, data=request.data)
        if not serializer.is_valid():
            return Response(
                {'error': serializer.errors},
                status=status.HTTP_400_BAD_REQUEST
            )
        serializer.save()
        return Response(
            {'data': serializer.data},
            status=status.HTTP_404_NOT_FOUND
        )

    def delete(self, request: Request, recipe_id: uuid, rating_id: uuid):
        try:
            rating = Recipe.objects.get(pk=rating_id, recipe_id=recipe_id)
        except Exception as e:
            print(e)
            return Response(
                {'message': 'Recipe or Rating not found'},
                status=status.HTTP_404_NOT_FOUND
            )
        rating.delete()
        return Response(
            {'message': 'Rating has been deleted successfully.'},
            status=status.HTTP_204_NO_CONTENT
        )


class ReviewView(APIView):
    def post(self, request: Request, recipe_id: uuid):
        try:
            Recipe.objects.get(pk=recipe_id)
        except Exception as e:
            print(e)
            return Response(
                {'message': 'Recipe not found'},
                status=status.HTTP_404_NOT_FOUND
            )
        serializer = ReviewSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(
                {'error': serializer.errors},
                status=status.HTTP_400_BAD_REQUEST
            )
        serializer.save()
        return Response(
            {'data': serializer.data},
            status=status.HTTP_404_NOT_FOUND
        )


class ReviewDetailView(APIView):
    def patch(self, request: Request, recipe_id: uuid, review_id: uuid):
        try:
            review = Recipe.objects.get(pk=review_id, recipe_id=recipe_id)
        except Exception as e:
            print(e)
            return Response(
                {'message': 'Recipe or Review not found'},
                status=status.HTTP_404_NOT_FOUND
            )
        serializer = ReviewSerializer(review, data=request.data)
        if not serializer.is_valid():
            return Response(
                {'error': serializer.errors},
                status=status.HTTP_400_BAD_REQUEST
            )
        serializer.save()
        return Response(
            {'data': serializer.data},
            status=status.HTTP_404_NOT_FOUND
        )

    def delete(self, request: Request, recipe_id: uuid, review_id: uuid):
        try:
            review = Recipe.objects.get(pk=review_id, recipe_id=recipe_id)
        except Exception as e:
            print(e)
            return Response(
                {'message': 'Recipe or Review not found'},
                status=status.HTTP_404_NOT_FOUND
            )
        review.delete()
        return Response(
            {'message': 'Review has been deleted successfully.'},
            status=status.HTTP_204_NO_CONTENT
        )


class FavoritesView(APIView):
    def get(self, request: Request):
        pass


class FavoritesDetailView(APIView):
    def post(self, request: Request, recipe_id: uuid):
        try:
            Favorites.objects.get(pk=recipe_id)
        except Exception as e:
            return Response(
                {'message': 'Recipe not found'},
                status=status.HTTP_404_NOT_FOUND
            )
        serializer = FavoritesSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(
                {'message': serializer.errors},
                status=status.HTTP_400_BAD_REQUEST
            )
        serializer.save()
        return Response(
            {'data': serializer.data},
            status=status.HTTP_201_CREATED
        )

    def delete(self, request: Request, recipe_id: uuid):
        try:
            favorite = Favorites.objects.get(pk=recipe_id)
        except Exception as e:
            return Response(
                {'message': 'Recipe not found'},
                status=status.HTTP_404_NOT_FOUND
            )
        favorite.delete()
        return Response(
            {'message': 'Favorite has been deleted successfully.'},
            status=status.HTTP_204_NO_CONTENT
        )