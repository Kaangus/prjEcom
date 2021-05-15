from PIL import Image
from django.forms import ModelChoiceField, ModelForm, ValidationError
from django.contrib import admin

from .models import *


class ImageAdminForm(ModelForm):


    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['image'].help_text = "Minimum image size is {}x{}".format(
            *Product.MIN_RESOLUTION
        )

    # def clean_image(self):
    #     image = self.cleaned_data['image']
    #     img = Image.open(image)
    #     min_height, min_width = Product.MIN_RESOLUTION
    #     max_height, max_width = Product.MAX_RESOLUTION
    #     if image.size > Product.MAX_SIZE:
    #         raise ValidationError("Image is too big ( > 3MB)")
    #     if img.height < min_height or img.width < min_width:
    #         raise ValidationError("Image is too small( < {}x{})".format(*Product.MIN_RESOLUTION))
    #     if img.height > max_height or img.width > max_width:
    #         raise ValidationError("Image is too big( > {}x{})".format(*Product.MAX_RESOLUTION))
    #     return image

class PizzaAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'is_discounted')
    form = ImageAdminForm

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == 'category':
            return ModelChoiceField(Category.objects.filter(slug='pizza'))
        return super().formfield_for_foreignkey(db_field, request, **kwargs)


class SusiAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'is_discounted')
    form = ImageAdminForm

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == 'category':
            return ModelChoiceField(Category.objects.filter(slug='susi'))
        return super().formfield_for_foreignkey(db_field, request, **kwargs)


admin.site.register(Category)
admin.site.register(Pizza, PizzaAdmin)
admin.site.register(Susi, SusiAdmin)
admin.site.register(CartProduct)
admin.site.register(Cart)
admin.site.register(Customer)
