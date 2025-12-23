from django.urls import path

from . import views

app_name = "catalog"

urlpatterns = [
    path("", views.EquipmentListView.as_view(), name="equipment_list"),
    path("equipment/add/", views.EquipmentCreateView.as_view(), name="equipment_add"),
    path(
        "equipment/<int:pk>/",
        views.EquipmentDetailView.as_view(),
        name="equipment_detail",
    ),
    path(
        "equipment/<int:pk>/edit/",
        views.EquipmentUpdateView.as_view(),
        name="equipment_edit",
    ),
    path(
        "equipment/<int:pk>/delete/",
        views.EquipmentDeleteView.as_view(),
        name="equipment_delete",
    ),
]


