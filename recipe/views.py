import uuid

from rest_framework.views import APIView
from rest_framework import status
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication

from .models import Recipe, Rating, Review, Favorite
from .serializers import RecipeSerializer, RatingSerializer, ReviewSerializer, FavoriteSerializer


class RecipeView(APIView):

    def get_permissions(self):
        if self.request.method == 'POST':
            return [IsAuthenticated()]
        return []

    def get_authentication_classes(self):
        if self.request.method == 'POST':
            return [JWTAuthentication]
        return []

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
            data['author'] = request.user.id

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
    def get_permissions(self):
        if self.request.method == 'GET':
            return []
        return [IsAuthenticated()]

    def get_authentication_classes(self):
        if self.request.method == 'GET':
            return []
        return [JWTAuthentication]

    def get(self, request: Request, pk: uuid):
        try:
            recipe = Recipe.objects.get(pk=pk)
        except Exception as e:
            return Response(
                {'data': {}, 'message': 'Recipe not found.'},
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

    def patch(self, request: Request, recipe_id: uuid):
        try:
            recipe = Recipe.objects.get(pk=recipe_id)
            if recipe.author != request.user:
                print(recipe.author, request.user)
                return Response(
                    {'data': {}, 'message': 'You are not authorized for this action.'},
                    status=status.HTTP_401_UNAUTHORIZED
                )
        except Exception as e:
            print(e)
            return Response(
                {'data': {}, 'message': 'Recipe not found.'},
                status=status.HTTP_400_BAD_REQUEST
            )

        serializer = RecipeSerializer(recipe, data=request.data, partial=True)

        if not serializer.is_valid():
            return Response(
                {'data': {}},
                status=status.HTTP_400_BAD_REQUEST
            )
        # serializer.is_authorized(serializer.data, request.user.id)
        serializer.save()
        return Response(
            {'data': serializer.data},
            status=status.HTTP_200_OK
        )

    def delete(self, request: Request, recipe_id: uuid):
        try:
            recipe = Recipe.objects.get(pk=recipe_id)
            if recipe.author != request.user:
                print(recipe.author, request.user)
                return Response(
                    {'data': {}, 'message': 'You are not authorized for this action.'},
                    status=status.HTTP_401_UNAUTHORIZED
                )
        except Exception as e:
            print(e)
            return Response(
                {'data': {}, 'message': 'Recipe not found.'},
                status=status.HTTP_400_BAD_REQUEST
            )
        recipe.delete()
        return Response(
            {'message': 'Recipe has been deleted successfully.'},
            status=status.HTTP_204_NO_CONTENT
        )


class RatingView(APIView):
    permission_classes = [IsAuthenticated]
    authentication_classes = [JWTAuthentication]

    def post(self, request: Request, recipe_id: uuid):
        try:
            recipe = Recipe.objects.get(pk=recipe_id)
        except Exception as e:
            print(e)
            return Response(
                {'data': {}, 'message': 'Recipe not found.'},
                status=status.HTTP_400_BAD_REQUEST
            )
        rating = Rating.objects.create(
            recipe_id=recipe,
            author_id=request.user,
            rating_number=request.data['rating_number']
        )
        serializer = RatingSerializer(rating)
        return Response(
            {'data': serializer.data, 'message': f'You rated {recipe.title}'},
            status=status.HTTP_201_CREATED
        )


class RatingDetailView(APIView):
    permission_classes = [IsAuthenticated]
    authentication_classes = [JWTAuthentication]

    def patch(self, request: Request, recipe_id: uuid, rating_id: uuid):
        try:
            rating = Rating.objects.get(pk=rating_id, recipe_id=recipe_id)
            if rating.author_id != request.user:
                return Response(
                    {'data': {}, 'message': 'You are not authorized for this action.' },
                    status=status.HTTP_401_UNAUTHORIZED
                )
        except Exception as e:
            print(e)
            return Response(
                {'data': {}, 'message': 'Recipe or Rating not found'},
                status=status.HTTP_404_NOT_FOUND
            )
        data = request.data
        data['recipe_id'] = recipe_id
        data['author_id'] = request.user.id
        serializer = RatingSerializer(rating, data=data)
        if not serializer.is_valid():
            return Response(
                {'error': serializer.errors},
                status=status.HTTP_400_BAD_REQUEST
            )
        serializer.save()
        return Response(
            {'data': serializer.data, 'message': f'You updated rating of {rating.recipe_id.title}'},
            status=status.HTTP_404_NOT_FOUND
        )

    def delete(self, request: Request, recipe_id: uuid, rating_id: uuid):
        try:
            rating = Rating.objects.get(pk=rating_id, recipe_id=recipe_id)
            if rating.author_id != request.user:
                return Response(
                    {'data': {}, 'message': 'You are not authorized for this action.'},
                    status=status.HTTP_401_UNAUTHORIZED
                )
        except Exception as e:
            print(e)
            return Response(
                {'message': 'Recipe or Rating not found'},
                status=status.HTTP_404_NOT_FOUND
            )
        rating.delete()
        return Response(
            {'data': {}, 'message': 'Rating has been deleted successfully.'},
            status=status.HTTP_204_NO_CONTENT
        )


class ReviewView(APIView):
    permission_classes = [IsAuthenticated]
    authentication_classes = [JWTAuthentication]

    def post(self, request: Request, recipe_id: uuid):
        try:
            recipe = Recipe.objects.get(pk=recipe_id)
        except Exception as e:
            print(e)
            return Response(
                {'message': 'Recipe not found'},
                status=status.HTTP_404_NOT_FOUND
            )
        review_data = Review.objects.create(
            recipe_id=recipe,
            author_id=request.user,
            review_text=request.data['review_text']
        )
        serializer = ReviewSerializer(review_data)
        return Response(
            {'data': serializer.data, 'message': f'You reviewed {recipe.title}'},
            status=status.HTTP_404_NOT_FOUND
        )


class ReviewDetailView(APIView):
    permission_classes = [IsAuthenticated]
    authentication_classes = [JWTAuthentication]

    def patch(self, request: Request, recipe_id: uuid, review_id: uuid):
        try:
            review = Review.objects.get(pk=review_id, recipe_id=recipe_id)
            if review.author_id != request.user:
                return Response(
                    {'data': {}, 'message': 'You are not authorized for this action.'},
                    status=status.HTTP_401_UNAUTHORIZED
                )
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
            review = Review.objects.get(pk=review_id, recipe_id=recipe_id)
            if review.author_id != request.user:
                return Response(
                    {'data': {}, 'message': 'You are not authorized for this action.'},
                    status=status.HTTP_401_UNAUTHORIZED
                )
        except Exception as e:
            print(e)
            return Response(
                {'message': 'Recipe or Review not found'},
                status=status.HTTP_404_NOT_FOUND
            )
        review.delete()
        return Response(
            {'data': {}, 'message': 'Review has been deleted successfully.'},
            status=status.HTTP_204_NO_CONTENT
        )


class FavoritesView(APIView):
    permission_classes = [IsAuthenticated]
    authentication_classes = [JWTAuthentication]

    def get(self, request: Request):
        try:
            favorite_recipes = Recipe.objects.filter(favorite__author_id=request.user)
        except Exception as e:
            print(e)
            return Response(
                {'data': {}, 'message': 'Recipes not found'},
                status=status.HTTP_400_BAD_REQUEST
            )
        serializer = FavoriteSerializer(favorite_recipes, many=True)
        return Response(
            {'data': serializer.data, 'message': 'List of favorite recipes'},
            status=status.HTTP_200_OK
        )


class FavoritesDetailView(APIView):
    permission_classes = [IsAuthenticated]
    authentication_classes = [JWTAuthentication]

    def post(self, request: Request, recipe_id: uuid):
        try:
            favorite_recipe = Recipe.objects.get(pk=recipe_id)
        except Exception as e:
            return Response(
                {'data': {}, 'message': 'Recipe not found'},
                status=status.HTTP_404_NOT_FOUND
            )
        favorite = Favorite.objects.create(recipe_id=favorite_recipe, author_id=request.user)
        serializer = FavoriteSerializer(favorite)

        return Response(
            {'data': serializer.data, 'message': f'You favorited {favorite_recipe.title}'},
            status=status.HTTP_201_CREATED
        )

    def delete(self, request: Request, recipe_id: uuid):
        try:
            favorite = Favorite.objects.get(pk=recipe_id)
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