# Generated by Django 4.1.4 on 2022-12-10 19:33

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('accounts', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=20, verbose_name='nomi')),
                ('slug', models.SlugField(max_length=20)),
            ],
        ),
        migrations.CreateModel(
            name='SubCategory',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=20, verbose_name='nomi')),
                ('slug', models.SlugField(max_length=20)),
                ('category', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='orders.category')),
            ],
        ),
        migrations.CreateModel(
            name='Product',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=30, verbose_name='Nomi')),
                ('pic', models.ImageField(upload_to='product/images/', verbose_name='Rasm')),
                ('code', models.CharField(max_length=10, verbose_name='Kod')),
                ('color', models.CharField(max_length=10, verbose_name='Rangi')),
                ('company', models.CharField(max_length=30, verbose_name='Kompaniya nomi')),
                ('info', models.TextField(verbose_name="Umumiy ma'lumot")),
                ('price', models.IntegerField(verbose_name='Narxi')),
                ('amount', models.IntegerField(verbose_name='Miqdori')),
                ('category', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='orders.category')),
                ('subcategory', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='orders.subcategory')),
            ],
        ),
        migrations.CreateModel(
            name='Order',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('gsum', models.IntegerField(verbose_name='Umumiy summa')),
                ('location', models.CharField(max_length=5, verbose_name='Lokatsiya (Mijoz lokatsiyasi)')),
                ('bonus', models.IntegerField(default=0)),
                ('discount', models.IntegerField(default=0, verbose_name='Chegirma')),
                ('customer', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='accounts.customer', verbose_name='Mijoz')),
                ('products', models.ManyToManyField(to='orders.product', verbose_name='Maxsulotlar')),
            ],
        ),
    ]
