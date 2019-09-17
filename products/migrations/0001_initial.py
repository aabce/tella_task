# Generated by Django 2.2.5 on 2019-09-15 12:02

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Product',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.TextField()),
                ('description', models.TextField()),
                ('img', models.ImageField(blank=True, null=True, upload_to='products')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='product', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
