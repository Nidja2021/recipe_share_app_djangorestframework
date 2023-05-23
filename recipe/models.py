import uuid

from django.contrib.auth.models import User
from django.db import models
from category.models import Category

# Category = apps.get_model('category', 'Category')


class BaseModel(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now_add=True)


class Recipe(BaseModel):
    title = models.CharField(max_length=100)
    author = models.ForeignKey(User, null=False, blank=False, on_delete=models.CASCADE, related_name='recipes')
    description = models.TextField()
    ingredients = models.TextField()
    instructions = models.TextField()
    recipe_image = models.ImageField(upload_to="recipe_images", null=True, blank=True)
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, blank=True)

    def __str__(self):
        return self.title


class Rating(BaseModel):
    recipe_id = models.ForeignKey('Recipe', on_delete=models.CASCADE, related_name='rating')
    author_id = models.ForeignKey(User, on_delete=models.CASCADE)
    rating_number = models.IntegerField(default=0)

    def __str__(self):
        return f"Rating: {self.rating}"


class Review(BaseModel):
    recipe_id = models.ForeignKey('Recipe', on_delete=models.CASCADE, related_name='review')
    author_id = models.ForeignKey(User, on_delete=models.CASCADE)
    review_text = models.TextField()

    def __str__(self):
        return f"Rating: {self.review}"


class Favorite(BaseModel):
    recipe_id = models.ForeignKey('Recipe', on_delete=models.CASCADE, related_name='favorite')
    author_id = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return f"Rating: {self.recipe.title}"

