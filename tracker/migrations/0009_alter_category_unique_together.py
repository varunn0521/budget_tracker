# Generated by Django 5.1.3 on 2024-11-25 14:52

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('tracker', '0008_alter_category_type'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='category',
            unique_together={('user', 'name', 'type')},
        ),
    ]
