# Generated by Django 3.2 on 2021-04-26 23:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('grabaciones', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='grabaciones',
            name='duration',
            field=models.DecimalField(blank=True, decimal_places=2, max_digits=4, null=True),
        ),
        migrations.AlterField(
            model_name='grabaciones',
            name='resolution',
            field=models.CharField(blank=True, max_length=20, null=True),
        ),
        migrations.AlterField(
            model_name='grabaciones',
            name='size',
            field=models.IntegerField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='grabaciones',
            name='status',
            field=models.CharField(blank=True, max_length=10, null=True),
        ),
        migrations.AlterField(
            model_name='grabaciones',
            name='url',
            field=models.URLField(blank=True, null=True),
        ),
    ]