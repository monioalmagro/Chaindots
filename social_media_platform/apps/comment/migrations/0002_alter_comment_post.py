# Generated by Django 4.2.11 on 2024-04-03 07:03

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ("post", "0001_initial"),
        ("comment", "0001_initial"),
    ]

    operations = [
        migrations.AlterField(
            model_name="comment",
            name="post",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                related_name="post_comment_set",
                to="post.post",
            ),
        ),
    ]
