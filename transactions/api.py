from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import viewsets

from .filters import CashFlowRecordFilter
from .models import CashFlowRecord, Category, OperationType, Status, Subcategory
from .serializers import (
    CashFlowRecordSerializer,
    CategorySerializer,
    OperationTypeSerializer,
    StatusSerializer,
    SubcategorySerializer,
)


class StatusViewSet(viewsets.ModelViewSet):
    queryset = Status.objects.all()
    serializer_class = StatusSerializer


class OperationTypeViewSet(viewsets.ModelViewSet):
    queryset = OperationType.objects.all()
    serializer_class = OperationTypeSerializer


class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.select_related("type").all()
    serializer_class = CategorySerializer
    filterset_fields = ["type"]


class SubcategoryViewSet(viewsets.ModelViewSet):
    queryset = Subcategory.objects.select_related("category").all()
    serializer_class = SubcategorySerializer
    filterset_fields = ["category"]


class CashFlowRecordViewSet(viewsets.ModelViewSet):
    queryset = CashFlowRecord.objects.select_related(
        "status", "type", "category", "subcategory"
    ).all()
    serializer_class = CashFlowRecordSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_class = CashFlowRecordFilter
