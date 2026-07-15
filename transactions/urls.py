from django.urls import path

from . import views

app_name = "transactions"

urlpatterns = [
    path("", views.CashFlowRecordListView.as_view(), name="record-list"),
    path("records/create/", views.CashFlowRecordCreateView.as_view(), name="record-create"),
    path(
        "records/<int:pk>/edit/",
        views.CashFlowRecordUpdateView.as_view(),
        name="record-update",
    ),
    path(
        "records/<int:pk>/delete/",
        views.CashFlowRecordDeleteView.as_view(),
        name="record-delete",
    ),
    path(
        "references/",
        views.ReferenceDashboardView.as_view(),
        name="reference-dashboard",
    ),
    path(
        "references/<str:kind>/create/",
        views.ReferenceCreateView.as_view(),
        name="reference-create",
    ),
    path(
        "references/<str:kind>/<int:pk>/edit/",
        views.ReferenceUpdateView.as_view(),
        name="reference-update",
    ),
    path(
        "references/<str:kind>/<int:pk>/delete/",
        views.ReferenceDeleteView.as_view(),
        name="reference-delete",
    ),
]
