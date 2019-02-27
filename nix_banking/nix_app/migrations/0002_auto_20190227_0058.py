# Generated by Django 2.1.7 on 2019-02-27 03:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('nix_app', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='transfer',
            name='transfer_type',
            field=models.CharField(choices=[('CC', 'CC'), ('TED', 'TED'), ('DOC', 'DOC')], default='DOC', max_length=3, verbose_name='Tipo da transferência'),
        ),
    ]