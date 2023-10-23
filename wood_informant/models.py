from django.db import models

class Statuses(models.Model):
    status_id = models.BigAutoField(primary_key=True)
    status = models.CharField(max_length=12)

    def __str__(self):
        return f'{self.status}'

class Products(models.Model):
    product_id = models.BigAutoField(primary_key=True)
    product = models.CharField(max_length=55)

    def __str__(self):
        return f'{self.product}'

class Cities(models.Model):
    city_id = models.BigAutoField(primary_key=True)
    city = models.CharField(max_length=124)

    def __str__(self):
        return f'{self.city}'

class Regions(models.Model):
    region_id = models.BigAutoField(primary_key=True)
    region = models.CharField(max_length=124)

    def __str__(self):
        return f'{self.region}'

class Countries(models.Model):
    country_id = models.BigAutoField(primary_key=True)
    country = models.CharField(max_length=55)

    def __str__(self):
        return f'{self.country}'

class Types(models.Model):
    type_id = models.BigAutoField(primary_key=True)
    type = models.CharField(max_length=40)

    def __str__(self):
        return f'{self.type}'

class SubTypes(models.Model):
    subtype_id = models.BigAutoField(primary_key=True)
    subtype = models.CharField(max_length=40)

    def __str__(self):
        return f'{self.subtype}'

class WoodTypes(models.Model):
    wood_type_id = models.BigAutoField(primary_key=True)
    wood_type = models.CharField(max_length=40)

    def __str__(self):
        return f'{self.wood_type}'

class WoodSubTypes(models.Model):
    wood_subtype_id = models.BigAutoField(primary_key=True)
    wood_subtype = models.CharField(max_length=40)

    def __str__(self):
        return f'{self.wood_subtype}'

class Wets(models.Model):
    wet_id = models.BigAutoField(primary_key=True)
    wet = models.CharField(max_length=40)

    def __str__(self):
        return f'{self.wet}'

class Actual(models.Model):
    post_id = models.IntegerField()
    status = models.ForeignKey(
        to=Statuses,
        on_delete=models.PROTECT,
    )
    product = models.ForeignKey(
        to=Products,
        on_delete=models.PROTECT,
    )
    title = models.CharField(max_length=252)
    city = models.ForeignKey(
        to=Cities,
        null=True,
        blank=True,
        on_delete=models.PROTECT,
    )
    region = models.ForeignKey(
        to=Regions,
        null=True,
        blank=True,
        on_delete=models.PROTECT,
    )
    country = models.ForeignKey(
        to=Countries,
        null=True,
        blank=True,
        on_delete=models.PROTECT,
    )
    price = models.DecimalField(max_digits=10, decimal_places=2)
    type = models.ForeignKey(
        to=Types,
        null=True,
        blank=True,
        on_delete=models.PROTECT,
    )
    subtype = models.ForeignKey(
        to=SubTypes,
        null=True,
        blank=True,
        on_delete=models.PROTECT,
    )
    wood_type = models.ForeignKey(
        to=WoodTypes,
        null=True,
        blank=True,
        on_delete=models.PROTECT,
    )
    wood_subtype = models.ForeignKey(
        to=WoodSubTypes,
        null=True,
        blank=True,
        on_delete=models.PROTECT,
    )
    wet = models.ForeignKey(
        to=Wets,
        null=True,
        blank=True,
        on_delete=models.PROTECT,
    )
    length = models.CharField(max_length=20, null=True, blank=True,)
    width = models.CharField(max_length=20, null=True, blank=True,)
    thickness = models.CharField(max_length=20, null=True, blank=True,)
    discription = models.CharField(max_length=3500)
    post_date = models.DateTimeField(null=True, blank=True,)
    parse_date = models.DateField()
    post_views = models.IntegerField(null=True, blank=True,)
    post_url = models.URLField()
    additional_regions = models.BooleanField(default=False)

    class Meta:
        verbose_name = 'Актуальные объявления'
        verbose_name_plural = 'Актуальные объявления'

class Previous(models.Model):
    post_id = models.IntegerField()
    status = models.ForeignKey(
        to=Statuses,
        on_delete=models.PROTECT,
    )
    product = models.ForeignKey(
        to=Products,
        on_delete=models.PROTECT,
    )
    title = models.CharField(max_length=252, null=True, blank=True)
    city = models.ForeignKey(
        to=Cities,
        null=True,
        blank=True,
        on_delete=models.PROTECT,
    )
    region = models.ForeignKey(
        to=Regions,
        null=True,
        blank=True,
        on_delete=models.PROTECT,
    )
    country = models.ForeignKey(
        to=Countries,
        null=True,
        blank=True,
        on_delete=models.PROTECT,
    )
    price = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    type = models.ForeignKey(
        to=Types,
        null=True,
        blank=True,
        on_delete=models.PROTECT,
    )
    subtype = models.ForeignKey(
        to=SubTypes,
        null=True,
        blank=True,
        on_delete=models.PROTECT,
    )
    wood_type = models.ForeignKey(
        to=WoodTypes,
        null=True,
        blank=True,
        on_delete=models.PROTECT,
    )
    wood_subtype = models.ForeignKey(
        to=WoodSubTypes,
        null=True,
        blank=True,
        on_delete=models.PROTECT,
    )
    wet = models.ForeignKey(
        to=Wets,
        null=True,
        blank=True,
        on_delete=models.PROTECT,
    )
    length = models.CharField(max_length=20, null=True, blank=True)
    width = models.CharField(max_length=20, null=True, blank=True)
    thickness = models.CharField(max_length=20, null=True, blank=True)
    discription = models.CharField(max_length=3500, null=True, blank=True)
    post_date = models.DateTimeField(null=True)
    parse_date = models.DateField()
    post_views = models.IntegerField(null=True, blank=True)
    post_url = models.URLField(null=True, blank=True)
    additional_regions = models.BooleanField(default=False)

    class Meta:
        verbose_name = 'Прошлые версии объявления'
        verbose_name_plural = 'Прошлые версии объявления'

class Profile(models.Model):
    external_id = models.TextField(
        verbose_name='Внешний ID пользователя',
        unique=True,
    )
    name = models.TextField(
        verbose_name='Имя пользователя',
        null=True
    )

    def __str__(self):
        return f'#{self.external_id} {self.name}'

    class Meta:
        verbose_name = 'Профиль'
        verbose_name_plural = 'Профили'


class Message(models.Model):
    profile = models.ForeignKey(
        to='wood_informant.Profile',
        verbose_name='Профиль',
        on_delete=models.PROTECT,
    )
    text = models.CharField(
        max_length=100,
        verbose_name='Текст',
    )
    created_at = models.DateTimeField(
        verbose_name='Время получения',
        auto_now_add=True,
    )

    def __str__(self):
        return f'Сообщение {self.pk} от {self.profile}'

    class Meta:
        verbose_name = 'Сообщение'
        verbose_name_plural = 'Сообщения'

