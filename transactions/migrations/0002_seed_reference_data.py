from django.db import migrations


STATUSES = ["Бизнес", "Личное", "Налог"]

TYPES = ["Пополнение", "Списание"]

CATEGORIES = {
    "Пополнение": ["Выручка", "Прочие поступления"],
    "Списание": ["Инфраструктура", "Маркетинг"],
}

SUBCATEGORIES = {
    "Инфраструктура": ["VPS", "Proxy"],
    "Маркетинг": ["Farpost", "Avito"],
}


def seed(apps, schema_editor):
    Status = apps.get_model("transactions", "Status")
    OperationType = apps.get_model("transactions", "OperationType")
    Category = apps.get_model("transactions", "Category")
    Subcategory = apps.get_model("transactions", "Subcategory")

    for name in STATUSES:
        Status.objects.get_or_create(name=name)

    types = {}
    for name in TYPES:
        types[name], _ = OperationType.objects.get_or_create(name=name)

    categories = {}
    for type_name, category_names in CATEGORIES.items():
        for category_name in category_names:
            categories[category_name], _ = Category.objects.get_or_create(
                name=category_name, type=types[type_name]
            )

    for category_name, subcategory_names in SUBCATEGORIES.items():
        for subcategory_name in subcategory_names:
            Subcategory.objects.get_or_create(
                name=subcategory_name, category=categories[category_name]
            )


def unseed(apps, schema_editor):
    Status = apps.get_model("transactions", "Status")
    OperationType = apps.get_model("transactions", "OperationType")
    Category = apps.get_model("transactions", "Category")
    Subcategory = apps.get_model("transactions", "Subcategory")

    Subcategory.objects.filter(
        name__in=[n for names in SUBCATEGORIES.values() for n in names]
    ).delete()
    Category.objects.filter(
        name__in=[n for names in CATEGORIES.values() for n in names]
    ).delete()
    OperationType.objects.filter(name__in=TYPES).delete()
    Status.objects.filter(name__in=STATUSES).delete()


class Migration(migrations.Migration):
    dependencies = [
        ("transactions", "0001_initial"),
    ]

    operations = [
        migrations.RunPython(seed, unseed),
    ]
