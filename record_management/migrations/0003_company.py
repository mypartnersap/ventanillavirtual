# Generated by Django 4.2.1 on 2023-08-01 14:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('record_management', '0002_record_userowner'),
    ]

    operations = [
        migrations.CreateModel(
            name='Company',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('companyid', models.CharField(max_length=20)),
                ('companyname', models.CharField(max_length=250)),
            ],
            options={
                'verbose_name': 'Empresa',
                'verbose_name_plural': 'Empresas',
            },
        ),
    ]
