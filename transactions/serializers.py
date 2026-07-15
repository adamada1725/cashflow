from rest_framework import serializers

from .models import CashFlowRecord, Category, OperationType, Status, Subcategory


class StatusSerializer(serializers.ModelSerializer):
    class Meta:
        model = Status
        fields = ["id", "name"]


class OperationTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = OperationType
        fields = ["id", "name"]


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ["id", "name", "type"]


class SubcategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Subcategory
        fields = ["id", "name", "category"]


class CashFlowRecordSerializer(serializers.ModelSerializer):
    amount_rub = serializers.DecimalField(
        max_digits=12, decimal_places=2, read_only=True
    )
    status_name = serializers.CharField(source="status.name", read_only=True)
    type_name = serializers.CharField(source="type.name", read_only=True)
    category_name = serializers.CharField(source="category.name", read_only=True)
    subcategory_name = serializers.CharField(source="subcategory.name", read_only=True)

    class Meta:
        model = CashFlowRecord
        fields = [
            "id",
            "created_at",
            "status",
            "status_name",
            "type",
            "type_name",
            "category",
            "category_name",
            "subcategory",
            "subcategory_name",
            "amount",
            "amount_rub",
            "comment",
        ]
        extra_kwargs = {"amount": {"min_value": 1}}

    def validate(self, attrs):
        category = attrs.get("category") or getattr(self.instance, "category", None)
        op_type = attrs.get("type") or getattr(self.instance, "type", None)
        subcategory = attrs.get("subcategory") or getattr(
            self.instance, "subcategory", None
        )

        if category and op_type and category.type_id != op_type.id:
            raise serializers.ValidationError(
                {"category": "Выбранная категория не относится к выбранному типу."}
            )
        if subcategory and category and subcategory.category_id != category.id:
            raise serializers.ValidationError(
                {
                    "subcategory": (
                        "Выбранная подкатегория не относится к выбранной категории."
                    )
                }
            )
        return attrs
