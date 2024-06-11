
from django.db import models


class Product(models.Model):
    title = models.CharField(max_length=120)
    description = models.TextField(blank=True, null=True)
    price = models.DecimalField(decimal_places=2, max_digits=5)
    summary = models.TextField(blank=False, null=False)
    featured = models.BooleanField(default=False)
    is_18_plus = models.BooleanField(default=False)

    category = models.ForeignKey('Category', on_delete=models.SET_NULL, blank=True, null=True, related_name='products')
    tags = models.ManyToManyField('Tag', blank=True, related_name='products')

    orders = models.ManyToManyField('Order', through='OrderProduct')
    stores = models.ManyToManyField('Store', through='StoreInventory', related_name='products')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    image = models.ImageField(upload_to='products/', null=True, blank=True)

    @property
    def additional_metadata(self):
        cache_key = f"product_supplier_data_{self.id}"

        cached_data = cache.get(cache_key)

        if cached_data:
            return cached_data

        time.sleep(1)
        supplier_data = {
            "storage_type": "fridge",
            "allegriens": [],
        }

        cache.set(f"product_supplier_data_{self.id}", supplier_data, 60 * 60 * 24)
        return supplier_data

    def __str__(self):
        return f"{self.title} - {self.price}"

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)

        # Compless image to 200x200 (convert to JPEG)
        if self.image:
            image = Image.open(self.image)
            image.thumbnail((200, 200))

            thumb_name, thumb_extension = os.path.splitext(self.image.name)

            thumb_filename = thumb_name + "_thumb" + ".jpg"

            temp_thumb = BytesIO()
            image.convert("RGB").save(temp_thumb, format='JPEG')
            temp_thumb.seek(0)

            # set save=False, otherwise it will run in an infinite loop
            self.image.save(thumb_filename,
                            SimpleUploadedFile(
                                thumb_filename,
                                temp_thumb.read(),
                                content_type=f"image/jpeg",
                            ),
                            save=False)
            super().save(*args, **kwargs)