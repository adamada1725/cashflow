import django_filters
from django import forms

from .models import CashFlowRecord, Category, OperationType, Status, Subcategory


class CashFlowRecordFilter(django_filters.FilterSet):
    date_from = django_filters.DateFilter(
        field_name="created_at",
        lookup_expr="gte",
        label="Дата с",
        widget=forms.DateInput(attrs={"type": "date", "class": "form-control"}),
    )
    date_to = django_filters.DateFilter(
        field_name="created_at",
        lookup_expr="lte",
        label="Дата по",
        widget=forms.DateInput(attrs={"type": "date", "class": "form-control"}),
    )
    status = django_filters.ModelChoiceFilter(
        queryset=Status.objects.all(),
        widget=forms.Select(attrs={"class": "form-select"}),
    )
    type = django_filters.ModelChoiceFilter(
        queryset=OperationType.objects.all(),
        widget=forms.Select(attrs={"class": "form-select"}),
    )
    category = django_filters.ModelChoiceFilter(
        queryset=Category.objects.all(),
        widget=forms.Select(attrs={"class": "form-select"}),
    )
    subcategory = django_filters.ModelChoiceFilter(
        queryset=Subcategory.objects.all(),
        widget=forms.Select(attrs={"class": "form-select"}),
    )

    class Meta:
        model = CashFlowRecord
        fields = ["date_from", "date_to", "status", "type", "category", "subcategory"]
