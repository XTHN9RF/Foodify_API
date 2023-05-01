# Generated by Django 4.2 on 2023-05-01 20:32

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('Foodify_API', '0006_alter_order_status'),
    ]

    operations = [
        migrations.CreateModel(
            name='OrderItem',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('quantity', models.IntegerField()),
                ('order', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Foodify_API.order')),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Foodify_API.product')),
            ],
        ),
    ]
