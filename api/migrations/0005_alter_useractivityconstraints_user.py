# Generated by Django 4.2 on 2024-03-27 10:07

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0004_useractivityconstraints_user'),
    ]

    operations = [
        migrations.AlterField(
            model_name='useractivityconstraints',
            name='user',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
    ]
