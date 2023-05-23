from django.urls import path
from .views import CategoryView, CategoryDetailView

urlpatterns = [
    path('', CategoryView.as_view(), name='category-view'),
    path('<uuid:category_id>/', CategoryDetailView.as_view(), name='category-detail-view'),
]
