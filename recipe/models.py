from django.db import models
from django.contrib.auth.models import User
import uuid


class BaseModel(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now_add=True)


class Rating(BaseModel):
    recipe_id = models.ForeignKey('Recipe', on_delete=models.CASCADE, related_name='ratings')
    user_id = models.ForeignKey(User, on_delete=models.CASCADE)
    rating_number = models.IntegerField(default=0)

    def __str__(self):
        return f"Rating: {self.rating}"


class Review(BaseModel):
    recipe_id = models.ForeignKey('Recipe', on_delete=models.CASCADE, related_name='reviews')
    user_id = models.ForeignKey(User, on_delete=models.CASCADE)
    review_text = models.TextField()

    def __str__(self):
        return f"Rating: {self.review}"


class Favorites(BaseModel):
    recipe_id = models.ForeignKey('Recipe', on_delete=models.CASCADE, related_name='favorites')
    user_id = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return f"Rating: {self.recipe.title}"


class Recipe(BaseModel):
    title = models.CharField(max_length=100)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    description = models.TextField()
    ingredients = models.TextField()
    instructions = models.TextField()
    # category = models.ForeignKey('Category', on_delete=models.SET_NULL, null=True, blank=True)

    def __str__(self):
        return self.title




