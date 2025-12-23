from django.contrib import admin

from .models import (
    Location,
    EquipmentType,
    Attribute,
    Equipment,
    EquipmentAttributeValue,
    Passport,
)


@admin.register(Location)
class LocationAdmin(admin.ModelAdmin):
    list_display = ("name", "parent")
    search_fields = ("name",)


class AttributeInline(admin.TabularInline):
    model = Attribute
    extra = 1


@admin.register(EquipmentType)
class EquipmentTypeAdmin(admin.ModelAdmin):
    list_display = ("name",)
    search_fields = ("name",)
    inlines = [AttributeInline]


class EquipmentAttributeValueInline(admin.TabularInline):
    model = EquipmentAttributeValue
    extra = 1


class PassportInline(admin.TabularInline):
    model = Passport
    extra = 1


@admin.register(Equipment)
class EquipmentAdmin(admin.ModelAdmin):
    list_display = ("name", "inventory_number", "type", "location")
    list_filter = ("type", "location")
    search_fields = ("name", "inventory_number", "description")
    inlines = [EquipmentAttributeValueInline, PassportInline]


@admin.register(Passport)
class PassportAdmin(admin.ModelAdmin):
    list_display = ("equipment", "file", "uploaded_at")
    search_fields = ("equipment__name", "equipment__inventory_number")
