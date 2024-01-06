import django_filters
from django_filters.rest_framework import FilterSet
from rest_framework import viewsets, mixins, status
from rest_framework.parsers import MultiPartParser
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response

from medicine.models import Product
from medicine.serializer import ProductSerializer

# Create your views here.

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
                     mixins.DestroyModelMixin):
    queryset = Product.objects.order_by('id')
    serializer_class = ProductSerializer
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
