# Generated by Django 5.1.5 on 2025-01-28 14:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('onlineshop', '0002_alter_comment_created_at_alter_order_product'),
    ]

    operations = [
        migrations.AlterField(
            model_name='comment',
            name='created_at',
            field=models.DateTimeField(auto_now_add=True),
        ),
    ]
