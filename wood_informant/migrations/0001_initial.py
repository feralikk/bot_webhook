# Generated by Django 4.0.5 on 2022-06-29 09:35

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Cities',
            fields=[
                ('city_id', models.BigAutoField(primary_key=True, serialize=False)),
                ('city', models.CharField(max_length=124)),
            ],
        ),
        migrations.CreateModel(
            name='Countries',
            fields=[
                ('country_id', models.BigAutoField(primary_key=True, serialize=False)),
                ('country', models.CharField(max_length=55)),
            ],
        ),
        migrations.CreateModel(
            name='Products',
            fields=[
                ('product_id', models.BigAutoField(primary_key=True, serialize=False)),
                ('product', models.CharField(max_length=55)),
            ],
        ),
        migrations.CreateModel(
            name='Profile',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('external_id', models.TextField(unique=True, verbose_name='Внешний ID пользователя')),
                ('name', models.TextField(null=True, verbose_name='Имя пользователя')),
            ],
            options={
                'verbose_name': 'Профиль',
                'verbose_name_plural': 'Профили',
            },
        ),
        migrations.CreateModel(
            name='Regions',
            fields=[
                ('region_id', models.BigAutoField(primary_key=True, serialize=False)),
                ('region', models.CharField(max_length=124)),
            ],
        ),
        migrations.CreateModel(
            name='Statuses',
            fields=[
                ('status_id', models.BigAutoField(primary_key=True, serialize=False)),
                ('status', models.CharField(max_length=12)),
            ],
        ),
        migrations.CreateModel(
            name='SubTypes',
            fields=[
                ('subtype_id', models.BigAutoField(primary_key=True, serialize=False)),
                ('subtype', models.CharField(max_length=40)),
            ],
        ),
        migrations.CreateModel(
            name='Types',
            fields=[
                ('type_id', models.BigAutoField(primary_key=True, serialize=False)),
                ('type', models.CharField(max_length=40)),
            ],
        ),
        migrations.CreateModel(
            name='Wets',
            fields=[
                ('wet_id', models.BigAutoField(primary_key=True, serialize=False)),
                ('wet', models.CharField(max_length=40)),
            ],
        ),
        migrations.CreateModel(
            name='WoodSubTypes',
            fields=[
                ('wood_subtype_id', models.BigAutoField(primary_key=True, serialize=False)),
                ('wood_subtype', models.CharField(max_length=40)),
            ],
        ),
        migrations.CreateModel(
            name='WoodTypes',
            fields=[
                ('wood_type_id', models.BigAutoField(primary_key=True, serialize=False)),
                ('wood_type', models.CharField(max_length=40)),
            ],
        ),
        migrations.CreateModel(
            name='Previous',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('post_id', models.IntegerField()),
                ('title', models.CharField(blank=True, max_length=252, null=True)),
                ('price', models.DecimalField(blank=True, decimal_places=2, max_digits=10, null=True)),
                ('length', models.CharField(blank=True, max_length=20, null=True)),
                ('width', models.CharField(blank=True, max_length=20, null=True)),
                ('thickness', models.CharField(blank=True, max_length=20, null=True)),
                ('discription', models.CharField(blank=True, max_length=3500, null=True)),
                ('post_date', models.DateField(null=True)),
                ('parse_date', models.DateField()),
                ('post_views', models.IntegerField(blank=True, null=True)),
                ('post_url', models.URLField(blank=True, null=True)),
                ('additional_regions', models.BooleanField(default=False)),
                ('city', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, to='wood_informant.cities')),
                ('country', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, to='wood_informant.countries')),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='wood_informant.products')),
                ('region', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, to='wood_informant.regions')),
                ('status', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='wood_informant.statuses')),
                ('subtype', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, to='wood_informant.subtypes')),
                ('type', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, to='wood_informant.types')),
                ('wet', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, to='wood_informant.wets')),
                ('wood_subtype', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, to='wood_informant.woodsubtypes')),
                ('wood_type', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, to='wood_informant.woodtypes')),
            ],
            options={
                'verbose_name': 'Прошлые версии объявления',
                'verbose_name_plural': 'Прошлые версии объявления',
            },
        ),
        migrations.CreateModel(
            name='Message',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('text', models.CharField(max_length=100, verbose_name='Текст')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='Время получения')),
                ('profile', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='wood_informant.profile', verbose_name='Профиль')),
            ],
            options={
                'verbose_name': 'Сообщение',
                'verbose_name_plural': 'Сообщения',
            },
        ),
        migrations.CreateModel(
            name='Actual',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('post_id', models.IntegerField()),
                ('title', models.CharField(max_length=252)),
                ('price', models.DecimalField(decimal_places=2, max_digits=10)),
                ('length', models.CharField(blank=True, max_length=20, null=True)),
                ('width', models.CharField(blank=True, max_length=20, null=True)),
                ('thickness', models.CharField(blank=True, max_length=20, null=True)),
                ('discription', models.CharField(max_length=3500)),
                ('post_date', models.DateField(blank=True, null=True)),
                ('parse_date', models.DateField()),
                ('post_views', models.IntegerField(blank=True, null=True)),
                ('post_url', models.URLField()),
                ('additional_regions', models.BooleanField(default=False)),
                ('city', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, to='wood_informant.cities')),
                ('country', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, to='wood_informant.countries')),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='wood_informant.products')),
                ('region', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, to='wood_informant.regions')),
                ('status', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='wood_informant.statuses')),
                ('subtype', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, to='wood_informant.subtypes')),
                ('type', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, to='wood_informant.types')),
                ('wet', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, to='wood_informant.wets')),
                ('wood_subtype', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, to='wood_informant.woodsubtypes')),
                ('wood_type', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, to='wood_informant.woodtypes')),
            ],
            options={
                'verbose_name': 'Актуальные объявления',
                'verbose_name_plural': 'Актуальные объявления',
            },
        ),
    ]
