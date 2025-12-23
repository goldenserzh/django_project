from django.db import models


class Location(models.Model):
    """
    Цех или площадка, можно сделать иерархию (завод -> цех -> участок).
    """
    name = models.CharField("Название", max_length=200)
    parent = models.ForeignKey(
        "self",
        verbose_name="Родитель",
        on_delete=models.CASCADE,
        related_name="children",
        null=True,
        blank=True,
    )

    class Meta:
        verbose_name = "Площадка / цех"
        verbose_name_plural = "Площадки / цеха"

    def __str__(self):
        return self.name


class EquipmentType(models.Model):
    """
    Тип оборудования (насос, двигатель, станок и т.п.).
    У разных типов будут разные характеристики.
    """
    name = models.CharField("Название типа", max_length=200, unique=True)

    class Meta:
        verbose_name = "Тип оборудования"
        verbose_name_plural = "Типы оборудования"

    def __str__(self):
        return self.name


class Attribute(models.Model):
    """
    Описание возможной характеристики для определённого типа оборудования.
    Например: мощность, давление, производитель.
    """
    TYPE_TEXT = "text"
    TYPE_INT = "int"
    TYPE_FLOAT = "float"

    VALUE_TYPE_CHOICES = [
        (TYPE_TEXT, "Текст"),
        (TYPE_INT, "Целое число"),
        (TYPE_FLOAT, "Число с точкой"),
    ]

    equipment_type = models.ForeignKey(
        EquipmentType,
        verbose_name="Тип оборудования",
        on_delete=models.CASCADE,
        related_name="attributes",
    )
    name = models.CharField("Название характеристики", max_length=200)
    value_type = models.CharField(
        "Тип значения",
        max_length=20,
        choices=VALUE_TYPE_CHOICES,
        default=TYPE_TEXT,
    )

    class Meta:
        verbose_name = "Характеристика"
        verbose_name_plural = "Характеристики"
        unique_together = ("equipment_type", "name")

    def __str__(self):
        return f"{self.equipment_type}: {self.name}"


class Equipment(models.Model):
    """
    Конкретная единица оборудования.
    """
    name = models.CharField("Название", max_length=255)
    inventory_number = models.CharField(
        "Инвентарный номер",
        max_length=100,
        unique=True,
    )
    type = models.ForeignKey(
        EquipmentType,
        verbose_name="Тип оборудования",
        on_delete=models.PROTECT,
        related_name="equipment",
    )
    location = models.ForeignKey(
        Location,
        verbose_name="Площадка / цех",
        on_delete=models.PROTECT,
        related_name="equipment",
    )
    description = models.TextField("Описание", blank=True)

    class Meta:
        verbose_name = "Оборудование"
        verbose_name_plural = "Оборудование"

    def __str__(self):
        return f"{self.name} ({self.inventory_number})"


class EquipmentAttributeValue(models.Model):
    """
    Значение конкретной характеристики для конкретной единицы оборудования.
    """
    equipment = models.ForeignKey(
        Equipment,
        verbose_name="Оборудование",
        on_delete=models.CASCADE,
        related_name="attribute_values",
    )
    attribute = models.ForeignKey(
        Attribute,
        verbose_name="Характеристика",
        on_delete=models.CASCADE,
        related_name="values",
    )
    value = models.CharField("Значение", max_length=255)

    class Meta:
        verbose_name = "Значение характеристики"
        verbose_name_plural = "Значения характеристик"
        unique_together = ("equipment", "attribute")

    def __str__(self):
        return f"{self.attribute.name}: {self.value}"


class Passport(models.Model):
    """
    Скан-копия паспорта или документа на оборудование.
    """
    equipment = models.ForeignKey(
        Equipment,
        verbose_name="Оборудование",
        on_delete=models.CASCADE,
        related_name="passports",
    )
    file = models.FileField("Файл паспорта", upload_to="passports/")
    uploaded_at = models.DateTimeField("Загружен", auto_now_add=True)

    class Meta:
        verbose_name = "Паспорт"
        verbose_name_plural = "Паспорта"

    def __str__(self):
        return f"Паспорт для {self.equipment}"
