# Generated by Django 4.1.1 on 2022-09-24 14:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("post", "0003_alter_post_hashtags"),
    ]

    operations = [
        migrations.AlterField(
            model_name="post",
            name="hashtags",
            field=models.ManyToManyField(to="post.hashtags"),
        ),
    ]
