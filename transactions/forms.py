from decimal import ROUND_HALF_UP, Decimal

from django import forms

from .models import CashFlowRecord, Category, OperationType, Status, Subcategory


class CashFlowRecordForm(forms.ModelForm):
    amount = forms.DecimalField(
        label="Сумма, ₽",
        min_value=Decimal("0.01"),
        max_digits=12,
        decimal_places=2,
        widget=forms.NumberInput(attrs={"step": "0.01", "class": "form-control"}),
    )

    class Meta:
        model = CashFlowRecord
        fields = [
            "created_at",
            "status",
            "type",
            "category",
            "subcategory",
            "amount",
            "comment",
        ]
        widgets = {
            "created_at": forms.DateInput(
                format="%Y-%m-%d", attrs={"type": "date", "class": "form-control"}
            ),
            "status": forms.Select(attrs={"class": "form-select"}),
            "type": forms.Select(attrs={"class": "form-select", "id": "id_type"}),
            "category": forms.Select(
                attrs={"class": "form-select", "id": "id_category"}
            ),
            "subcategory": forms.Select(
                attrs={"class": "form-select", "id": "id_subcategory"}
            ),
            "comment": forms.Textarea(
                attrs={"class": "form-control", "rows": 3}
            ),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["created_at"].input_formats = ["%Y-%m-%d"]
        if self.instance and self.instance.pk:
            self.initial["amount"] = self.instance.amount_rub

        type_id = self.data.get("type") or self.initial.get("type")
        if self.instance and self.instance.pk and not self.data:
            type_id = self.instance.type_id
        if type_id:
            self.fields["category"].queryset = Category.objects.filter(
                type_id=type_id
            )
        else:
            self.fields["category"].queryset = Category.objects.none()

        category_id = self.data.get("category") or self.initial.get("category")
        if self.instance and self.instance.pk and not self.data:
            category_id = self.instance.category_id
        if category_id:
            self.fields["subcategory"].queryset = Subcategory.objects.filter(
                category_id=category_id
            )
        else:
            self.fields["subcategory"].queryset = Subcategory.objects.none()

    def clean_amount(self):
        rub = self.cleaned_data["amount"]
        kopecks = (rub * 100).to_integral_value(rounding=ROUND_HALF_UP)
        return int(kopecks)

    def clean(self):
        cleaned_data = super().clean()
        category = cleaned_data.get("category")
        op_type = cleaned_data.get("type")
        subcategory = cleaned_data.get("subcategory")

        if category and op_type and category.type_id != op_type.id:
            self.add_error(
                "category", "Выбранная категория не относится к выбранному типу."
            )
        if subcategory and category and subcategory.category_id != category.id:
            self.add_error(
                "subcategory",
                "Выбранная подкатегория не относится к выбранной категории.",
            )
        return cleaned_data


class StatusForm(forms.ModelForm):
    class Meta:
        model = Status
        fields = ["name"]
        widgets = {"name": forms.TextInput(attrs={"class": "form-control"})}


class OperationTypeForm(forms.ModelForm):
    class Meta:
        model = OperationType
        fields = ["name"]
        widgets = {"name": forms.TextInput(attrs={"class": "form-control"})}


class CategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = ["name", "type"]
        widgets = {
            "name": forms.TextInput(attrs={"class": "form-control"}),
            "type": forms.Select(attrs={"class": "form-select"}),
        }


class SubcategoryForm(forms.ModelForm):
    class Meta:
        model = Subcategory
        fields = ["name", "category"]
        widgets = {
            "name": forms.TextInput(attrs={"class": "form-control"}),
            "category": forms.Select(attrs={"class": "form-select"}),
        }
