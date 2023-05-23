from rest_framework.views import APIView
from rest_framework import status
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication

from .models import Category
from .serializers import CategorySerializer


class CategoryView(APIView):
    def get_permissions(self):
        if self.request.method == 'POST':
            return [IsAuthenticated()]
        return []

    def get_authentication_classes(self):
        if self.request.method == 'POST':
            return [JWTAuthentication]
        return []

    def get(self, request):
        categories = Category.objects.all()
        serializer = CategorySerializer(categories, many=True)
        return Response(
            {'data': serializer.data, 'message': 'All Categories'},
            status=status.HTTP_200_OK
        )

    def post(self, request):
        category = Category.objects.create(name=request.data['name'])
        serializer = CategorySerializer(category)
        return Response(
            {'data': serializer.data, 'message': 'Created Category'},
            status=status.HTTP_201_CREATED
        )


class CategoryDetailView(APIView):
    permission_classes = [IsAuthenticated]
    authentication_classes = [JWTAuthentication]

    def get(self, request, category_id):
        category = Category.objects.get(pk=category_id)
        serializer = CategorySerializer(category)
        return Response(
            {'data': serializer.data, 'message': 'Specific category'},
            status=status.HTTP_200_OK
        )

    def patch(self, request, pk, category_id):
        category = Category.objects.get(pk=category_id)
        data = request.data
        serializer = CategorySerializer(category, data, partial=True)
        return Response(
            {'data': serializer.data, 'message': f'You updated {category}'},
            status=status.HTTP_200_OK
        )

    def delete(self, request, pk, category_id):
        category = Category.objects.get(pk=category_id)
        category.delete()
        return Response(
            {'data': {}, 'message': f'You deleted {category}'},
            status=status.HTTP_200_OK
        )
