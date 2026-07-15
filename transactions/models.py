from decimal import Decimal

from django.core.exceptions import ValidationError
from django.core.validators import MinValueValidator
from django.db import models
from django.utils import timezone


class Status(models.Model):
    name = models.CharField("Название", max_length=100, unique=True)

    class Meta:
        verbose_name = "Статус"
        verbose_name_plural = "Статусы"
        ordering = ["name"]

    def __str__(self):
        return self.name


class OperationType(models.Model):
    name = models.CharField("Название", max_length=100, unique=True)

    class Meta:
        verbose_name = "Тип"
        verbose_name_plural = "Типы"
        ordering = ["name"]

    def __str__(self):
        return self.name


class Category(models.Model):
    name = models.CharField("Название", max_length=150)
    type = models.ForeignKey(
        OperationType,
        verbose_name="Тип",
        related_name="categories",
        on_delete=models.CASCADE,
    )

    class Meta:
        verbose_name = "Категория"
        verbose_name_plural = "Категории"
        ordering = ["type__name", "name"]
        constraints = [
            models.UniqueConstraint(
                fields=["name", "type"], name="unique_category_per_type"
            )
        ]

    def __str__(self):
        return f"{self.name} ({self.type.name})"


class Subcategory(models.Model):
    name = models.CharField("Название", max_length=150)
    category = models.ForeignKey(
        Category,
        verbose_name="Категория",
        related_name="subcategories",
        on_delete=models.CASCADE,
    )

    class Meta:
        verbose_name = "Подкатегория"
        verbose_name_plural = "Подкатегории"
        ordering = ["category__name", "name"]
        constraints = [
            models.UniqueConstraint(
                fields=["name", "category"], name="unique_subcategory_per_category"
            )
        ]

    def __str__(self):
        return f"{self.name} ({self.category.name})"


class CashFlowRecord(models.Model):
    created_at = models.DateField("Дата создания", default=timezone.localdate)
    status = models.ForeignKey(
        Status, verbose_name="Статус", related_name="records", on_delete=models.PROTECT
    )
    type = models.ForeignKey(
        OperationType,
        verbose_name="Тип",
        related_name="records",
        on_delete=models.PROTECT,
    )
    category = models.ForeignKey(
        Category,
        verbose_name="Категория",
        related_name="records",
        on_delete=models.PROTECT,
    )
    subcategory = models.ForeignKey(
        Subcategory,
        verbose_name="Подкатегория",
        related_name="records",
        on_delete=models.PROTECT,
    )
    amount = models.PositiveBigIntegerField(
        "Сумма, коп.", validators=[MinValueValidator(1)]
    )
    comment = models.TextField("Комментарий", blank=True)

    class Meta:
        verbose_name = "Запись ДДС"
        verbose_name_plural = "Записи ДДС"
        ordering = ["-created_at", "-id"]

    def __str__(self):
        return f"{self.created_at} — {self.type} — {self.amount_rub} р."

    @property
    def amount_rub(self) -> Decimal:
        return (Decimal(self.amount) / 100).quantize(Decimal("0.01"))

    def clean(self):
        errors = {}
        if self.category_id and self.type_id and self.category.type_id != self.type_id:
            errors["category"] = (
                "Выбранная категория не относится к выбранному типу."
            )
        if (
            self.subcategory_id
            and self.category_id
            and self.subcategory.category_id != self.category_id
        ):
            errors["subcategory"] = (
                "Выбранная подкатегория не относится к выбранной категории."
            )
        if errors:
            raise ValidationError(errors)
