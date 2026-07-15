from django.contrib import messages
from django.db.models import ProtectedError
from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse_lazy
from django.views.generic import CreateView, DeleteView, ListView, UpdateView, View

from .filters import CashFlowRecordFilter
from .forms import (
    CashFlowRecordForm,
    CategoryForm,
    OperationTypeForm,
    StatusForm,
    SubcategoryForm,
)
from .models import CashFlowRecord, Category, OperationType, Status, Subcategory


class CashFlowRecordListView(ListView):
    model = CashFlowRecord
    template_name = "transactions/record_list.html"
    context_object_name = "records"
    paginate_by = 25

    def get_queryset(self):
        qs = CashFlowRecord.objects.select_related(
            "status", "type", "category", "subcategory"
        )
        self.filterset = CashFlowRecordFilter(self.request.GET, queryset=qs)
        return self.filterset.qs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["filter"] = self.filterset
        querystring = self.request.GET.copy()
        querystring.pop("page", None)
        context["querystring"] = querystring.urlencode()
        return context


class CashFlowRecordCreateView(CreateView):
    model = CashFlowRecord
    form_class = CashFlowRecordForm
    template_name = "transactions/record_form.html"
    success_url = reverse_lazy("transactions:record-list")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = "Новая запись"
        return context

    def form_valid(self, form):
        messages.success(self.request, "Запись создана.")
        return super().form_valid(form)


class CashFlowRecordUpdateView(UpdateView):
    model = CashFlowRecord
    form_class = CashFlowRecordForm
    template_name = "transactions/record_form.html"
    success_url = reverse_lazy("transactions:record-list")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = "Редактирование записи"
        return context

    def form_valid(self, form):
        messages.success(self.request, "Запись обновлена.")
        return super().form_valid(form)


class CashFlowRecordDeleteView(DeleteView):
    model = CashFlowRecord
    template_name = "transactions/record_confirm_delete.html"
    success_url = reverse_lazy("transactions:record-list")

    def form_valid(self, form):
        messages.success(self.request, "Запись удалена.")
        return super().form_valid(form)


REFERENCE_REGISTRY = {
    "status": {
        "model": Status,
        "form": StatusForm,
        "title": "Статусы",
        "singular": "Статус",
    },
    "type": {
        "model": OperationType,
        "form": OperationTypeForm,
        "title": "Типы",
        "singular": "Тип",
    },
    "category": {
        "model": Category,
        "form": CategoryForm,
        "title": "Категории",
        "singular": "Категория",
    },
    "subcategory": {
        "model": Subcategory,
        "form": SubcategoryForm,
        "title": "Подкатегории",
        "singular": "Подкатегория",
    },
}


class ReferenceDashboardView(ListView):
    template_name = "transactions/reference_dashboard.html"

    def get_queryset(self):
        return None

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["statuses"] = Status.objects.all()
        context["types"] = OperationType.objects.all()
        context["categories"] = Category.objects.select_related("type").all()
        context["subcategories"] = Subcategory.objects.select_related(
            "category", "category__type"
        ).all()
        context["active_tab"] = self.request.GET.get("tab", "status")
        return context


class ReferenceCreateView(CreateView):
    template_name = "transactions/reference_form.html"

    def dispatch(self, request, *args, **kwargs):
        self.kind = kwargs["kind"]
        self.config = REFERENCE_REGISTRY[self.kind]
        self.model = self.config["model"]
        self.form_class = self.config["form"]
        return super().dispatch(request, *args, **kwargs)

    def get_success_url(self):
        return f"{reverse_lazy('transactions:reference-dashboard')}?tab={self.kind}"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = f"Новая запись: {self.config['singular']}"
        context["kind"] = self.kind
        return context

    def form_valid(self, form):
        messages.success(self.request, f"{self.config['singular']} добавлен(а).")
        return super().form_valid(form)


class ReferenceUpdateView(UpdateView):
    template_name = "transactions/reference_form.html"

    def dispatch(self, request, *args, **kwargs):
        self.kind = kwargs["kind"]
        self.config = REFERENCE_REGISTRY[self.kind]
        self.model = self.config["model"]
        self.form_class = self.config["form"]
        return super().dispatch(request, *args, **kwargs)

    def get_success_url(self):
        return f"{reverse_lazy('transactions:reference-dashboard')}?tab={self.kind}"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = f"Редактирование: {self.config['singular']}"
        context["kind"] = self.kind
        return context

    def form_valid(self, form):
        messages.success(self.request, f"{self.config['singular']} обновлён(а).")
        return super().form_valid(form)


class ReferenceDeleteView(View):
    def post(self, request, kind, pk):
        config = REFERENCE_REGISTRY[kind]
        obj = get_object_or_404(config["model"], pk=pk)
        try:
            obj.delete()
            messages.success(request, f"{config['singular']} удалён(а).")
        except ProtectedError:
            messages.error(
                request,
                f"Нельзя удалить «{obj}» — есть записи ДДС или зависимые "
                "справочники, которые на него ссылаются.",
            )
        return redirect(f"{reverse_lazy('transactions:reference-dashboard')}?tab={kind}")
