from django.urls import path
from .views import RecipeView, RecipeDetailView, RatingView, RatingDetailView, FavoritesView, FavoritesDetailView

urlpatterns = [
    path('', RecipeView.as_view()),
    path('<uuid:pk>/', RecipeDetailView.as_view(), name='recipe-model-view'),
    path('<uuid:recipe_id>/ratings/', RatingView.as_view(), name='rating-model-view'),
    path('<uuid:recipe_id>/<uuid:rating_id>/', RatingDetailView.as_view(), name='rating-detail-model-view'),
    path('<uuid:recipe_id>/reviews/', RatingView.as_view(), name='review-model-view'),
    path('<uuid:recipe_id>/<uuid:review_id>/', RatingDetailView.as_view(), name='review-detail-model-view'),
    path('favorites/', FavoritesView.as_view(), name='favorites-model-view'),
    path('<uuid:recipe_id>/favorites/', FavoritesDetailView.as_view(), name='favorite-detail-model-view'),
]
