# Generated by Django 4.0.1 on 2023-01-31 18:54

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('myapp', '0005_alter_group_avatar_alter_posts_img_alter_user_avatar'),
    ]

    operations = [
        migrations.AlterField(
            model_name='group',
            name='admin',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
    ]
