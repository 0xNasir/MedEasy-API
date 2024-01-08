import django_filters
from django_filters.rest_framework import FilterSet
from rest_framework import viewsets, mixins, status
from rest_framework.pagination import PageNumberPagination
from rest_framework.parsers import MultiPartParser
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response

from medicine.models import Product
from medicine.serializer import ProductSerializer, RetrieveProductSerializer

from django.core.cache import cache
import time
import redis

redis_instance = redis.StrictRedis(host='127.0.0.1', port=6379, db=1)

"""
DjangoFilterBackend is used here for filtering functionality.
Here we implement filterset for product.
It will lookup name, min price and max price.
"""


class ProductFilter(FilterSet):
    name = django_filters.CharFilter(field_name='name', lookup_expr='icontains')
    unit_price_min = django_filters.NumberFilter(field_name='unit_price', lookup_expr='gte')
    unit_price_max = django_filters.NumberFilter(field_name='unit_price', lookup_expr='lte')

    class Meta:
        model = Product
        fields = ['name']


"""
Product API view contains all CRUD operation.
GenericViewSet is used here so that individual API action can bind here or stopped.
Removing a mixin will unbind a method.
"""


class ProductAPIView(viewsets.GenericViewSet,
                     mixins.ListModelMixin,
                     mixins.CreateModelMixin,
                     mixins.UpdateModelMixin,
                     mixins.RetrieveModelMixin,
                     mixins.DestroyModelMixin,
                     PageNumberPagination):
    queryset = Product.objects.order_by('id')
    filterset_class = ProductFilter
    """
    As we have file upload, we cannot use json parser,
    So we define here MultiPartParser as our parser classes.
    """
    parser_classes = [MultiPartParser]

    """
    No authentication for get and retrieve api. Anyone can see the product without authentication
    For creating, updating and deleting, authentication is required
    """

    def get_permissions(self):
        if self.action in ['list', 'retrieve']:
            return [AllowAny()]
        return [IsAuthenticated()]

    """
    Override the get serializer method so that, list and retieve endpoints get a detailed response.
    In create and update, it will view minimum information.
    """

    def get_serializer_class(self):
        if self.action in ['list', 'retrieve']:
            return RetrieveProductSerializer
        return ProductSerializer

    """
    Override the list methid to get the custom query filter.
    Also handle the redis cache
    """

    def list(self, request, *args, **kwargs):
        name = self.request.GET.get('name')
        price_min = self.request.GET.get('unit_price_min')
        price_max = self.request.GET.get('unit_price_max')

        """
        Generate a redis key to query in redis cache list
        or to store in cache list against redis key
        """
        redis_key: str = ''
        redis_key += name if name else ''
        redis_key += '_' + price_min if price_min else ''
        redis_key += '_' + price_max if price_max else ''

        """
        Check whether the query data is cached in redis.
        If found send the cached data to user response.
        """

        if redis_key in cache:
            queryset = cache.get(redis_key)
            page = self.paginate_queryset(queryset)
            if page is not None:
                serializer = self.get_serializer(page, many=True)
                return self.get_paginated_response(serializer.data)

            serializer = self.get_serializer(queryset, many=True)
            return Response(serializer.data)

        """
        If query data is not found, then filter from main database.
        Then store in redis cache against the redis key.
        """
        queryset = self.get_queryset()
        if name:
            queryset = queryset.filter(name__icontains=self.request.GET.get('name'))

        if self.request.GET.get('unit_price_min'):
            queryset = queryset.filter(unit_price__gte=self.request.GET.get('unit_price_min'))

        if self.request.GET.get('unit_price_max'):
            queryset = queryset.filter(unit_price__lte=self.request.GET.get('unit_price_max'))

        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            if redis_key:
                cache.set(redis_key, serializer.data)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)
        if redis_key:
            cache.set(redis_key, serializer.data)
        return Response(serializer.data)

    def create(self, request, *args, **kwargs):
        """
        Create API endpoint is to create a product item. It will receive serialized data then validate the data.
        After validating, it will assign user to current logged in user. Then save the serializer.
        """
        serializer = ProductSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.validated_data['added_by'] = self.request.user
        serializer.save()
        return Response(serializer.data, status.HTTP_201_CREATED)
