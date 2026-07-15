from django.contrib import admin

from .models import CashFlowRecord, Category, OperationType, Status, Subcategory


@admin.register(Status)
class StatusAdmin(admin.ModelAdmin):
    list_display = ("id", "name")
    search_fields = ("name",)


@admin.register(OperationType)
class OperationTypeAdmin(admin.ModelAdmin):
    list_display = ("id", "name")
    search_fields = ("name",)


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ("id", "name", "type")
    list_filter = ("type",)
    search_fields = ("name",)


@admin.register(Subcategory)
class SubcategoryAdmin(admin.ModelAdmin):
    list_display = ("id", "name", "category")
    list_filter = ("category__type", "category")
    search_fields = ("name",)


@admin.register(CashFlowRecord)
class CashFlowRecordAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "created_at",
        "status",
        "type",
        "category",
        "subcategory",
        "amount_rub",
    )
    list_filter = ("status", "type", "category", "subcategory")
    search_fields = ("comment",)
    date_hierarchy = "created_at"

    @admin.display(description="Сумма, р.")
    def amount_rub(self, obj):
        return obj.amount_rub
