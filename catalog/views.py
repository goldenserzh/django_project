from django.db import transaction
from django.db.models import Q
from django.urls import reverse_lazy
from django.views.generic import (
    ListView,
    DetailView,
    CreateView,
    UpdateView,
    DeleteView,
)

from .models import Equipment, EquipmentAttributeValue, Attribute, EquipmentType, Location


class EquipmentListView(ListView):
    model = Equipment
    template_name = "catalog/equipment_list.html"
    context_object_name = "equipment_list"
    paginate_by = 20

    def get_queryset(self):
        qs = Equipment.objects.select_related("type", "location").prefetch_related(
            "attribute_values__attribute"
        )

        search = self.request.GET.get("q")
        type_id = self.request.GET.get("type")
        location_id = self.request.GET.get("location")

        if search:
            qs = qs.filter(
                Q(name__icontains=search)
                | Q(inventory_number__icontains=search)
                | Q(description__icontains=search)
                | Q(attribute_values__value__icontains=search)
            ).distinct()

        if type_id:
            qs = qs.filter(type_id=type_id)

        if location_id:
            qs = qs.filter(location_id=location_id)

        return qs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["types"] = EquipmentType.objects.all()
        context["locations"] = Location.objects.all()
        context["current_type"] = self.request.GET.get("type", "")
        context["current_location"] = self.request.GET.get("location", "")
        context["search_query"] = self.request.GET.get("q", "")
        return context


class EquipmentDetailView(DetailView):
    model = Equipment
    template_name = "catalog/equipment_detail.html"
    context_object_name = "equipment"


class EquipmentCreateUpdateMixin:
    model = Equipment
    fields = ["name", "inventory_number", "type", "location", "description"]
    template_name = "catalog/equipment_form.html"
    success_url = reverse_lazy("catalog:equipment_list")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        equipment_type = None
        if self.request.method == "POST":
            type_id = self.request.POST.get("type")
            if type_id:
                equipment_type = EquipmentType.objects.filter(pk=type_id).first()
        else:
            obj = getattr(self, "object", None)
            equipment_type = obj.type if obj else None

        attributes = Attribute.objects.filter(equipment_type=equipment_type) if equipment_type else []
        context["attributes"] = attributes

        values_by_attr = {}
        if getattr(self, "object", None):
            for av in self.object.attribute_values.all():
                values_by_attr[av.attribute_id] = av.value
        context["values_by_attr"] = values_by_attr
        return context

    @transaction.atomic
    def form_valid(self, form):
        response = super().form_valid(form)
        equipment = self.object

        # Сохраняем значения характеристик
        for attr in Attribute.objects.filter(equipment_type=equipment.type):
            value = self.request.POST.get(f"attr_{attr.id}")
            if value is None:
                continue
            EquipmentAttributeValue.objects.update_or_create(
                equipment=equipment,
                attribute=attr,
                defaults={"value": value},
            )

        return response


class EquipmentCreateView(EquipmentCreateUpdateMixin, CreateView):
    pass


class EquipmentUpdateView(EquipmentCreateUpdateMixin, UpdateView):
    pass


class EquipmentDeleteView(DeleteView):
    model = Equipment
    template_name = "catalog/equipment_confirm_delete.html"
    success_url = reverse_lazy("catalog:equipment_list")

