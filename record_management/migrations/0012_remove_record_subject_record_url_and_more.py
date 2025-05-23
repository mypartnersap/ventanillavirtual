# Generated by Django 4.2.1 on 2023-08-22 17:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('record_management', '0011_remove_record_phone_record_contactperson_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='record',
            name='subject',
        ),
        migrations.AddField(
            model_name='record',
            name='url',
            field=models.URLField(blank=True, max_length=300, null=True, verbose_name='Link'),
        ),
        migrations.AlterField(
            model_name='record',
            name='lastName',
            field=models.CharField(blank=True, max_length=100, null=True, verbose_name='Apellido'),
        ),
    ]
