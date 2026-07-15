from django.contrib import admin
from django.urls import include, path
from rest_framework.routers import DefaultRouter

from transactions.api import (
    CashFlowRecordViewSet,
    CategoryViewSet,
    OperationTypeViewSet,
    StatusViewSet,
    SubcategoryViewSet,
)

router = DefaultRouter()
router.register("records", CashFlowRecordViewSet)
router.register("statuses", StatusViewSet)
router.register("types", OperationTypeViewSet)
router.register("categories", CategoryViewSet)
router.register("subcategories", SubcategoryViewSet)

urlpatterns = [
    path("admin/", admin.site.urls),
    path("api/", include(router.urls)),
    path("api-auth/", include("rest_framework.urls")),
    path("", include("transactions.urls")),
]
