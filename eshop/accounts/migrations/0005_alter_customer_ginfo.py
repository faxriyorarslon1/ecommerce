# Generated by Django 4.1.4 on 2022-12-11 21:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0004_alter_customer_debt_alter_customer_discard_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='customer',
            name='ginfo',
            field=models.TextField(null=True, verbose_name="Umumiy ma'lumot"),
        ),
    ]