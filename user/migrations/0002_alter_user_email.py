# Generated by Django 4.1.1 on 2022-09-23 11:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("user", "0001_initial"),
    ]

    operations = [
        migrations.AlterField(
            model_name="user",
            name="email",
            field=models.EmailField(
                blank=True, max_length=128, unique=True, verbose_name="사용자 이메일"
            ),
        ),
    ]
