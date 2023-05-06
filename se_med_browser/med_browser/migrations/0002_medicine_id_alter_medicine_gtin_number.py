# Generated by Django 4.2.1 on 2023-05-06 17:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("med_browser", "0001_initial"),
    ]

    operations = [
        migrations.AddField(
            model_name="medicine",
            name="id",
            field=models.BigAutoField(
                auto_created=True,
                default=1,
                primary_key=True,
                serialize=False,
                verbose_name="ID",
            ),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name="medicine",
            name="GTIN_number",
            field=models.CharField(max_length=2000),
        ),
    ]
