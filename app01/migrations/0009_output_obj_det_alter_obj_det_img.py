# Generated by Django 4.2.6 on 2024-04-09 08:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("app01", "0008_obj_det"),
    ]

    operations = [
        migrations.CreateModel(
            name="output_obj_det",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("name", models.CharField(max_length=32, verbose_name="用户")),
                ("img", models.CharField(max_length=128, verbose_name="img")),
            ],
        ),
        migrations.AlterField(
            model_name="obj_det",
            name="img",
            field=models.FileField(
                max_length=128, upload_to="obj_dect/", verbose_name="img"
            ),
        ),
    ]