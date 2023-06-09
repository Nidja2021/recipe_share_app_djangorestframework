# Generated by Django 4.2.1 on 2023-05-22 19:19

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('recipe', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Review',
            fields=[
                ('basemodel_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='recipe.basemodel')),
                ('review_text', models.TextField()),
                ('recipe_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='reviews', to='recipe.recipe')),
                ('user_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            bases=('recipe.basemodel',),
        ),
        migrations.CreateModel(
            name='Rating',
            fields=[
                ('basemodel_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='recipe.basemodel')),
                ('rating_number', models.IntegerField(default=0)),
                ('recipe_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='ratings', to='recipe.recipe')),
                ('user_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            bases=('recipe.basemodel',),
        ),
        migrations.CreateModel(
            name='Favorites',
            fields=[
                ('basemodel_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='recipe.basemodel')),
                ('recipe_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='favorites', to='recipe.recipe')),
                ('user_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            bases=('recipe.basemodel',),
        ),
    ]
