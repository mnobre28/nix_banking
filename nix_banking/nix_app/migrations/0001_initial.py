# Generated by Django 2.1.7 on 2019-02-23 22:39

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Transfer',
            fields=[
                ('creation_date', models.DateField(auto_created=True, verbose_name='Data de criação')),
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('payers_name', models.CharField(default='', max_length=128, verbose_name='Nome do pagador')),
                ('payers_bank', models.CharField(default='', max_length=128, verbose_name='Banco do pagador')),
                ('payers_agency', models.CharField(default='', max_length=128, verbose_name='Agência do pagador')),
                ('payers_account', models.CharField(default='', max_length=128, verbose_name='Conta do pagador')),
                ('receivers_name', models.CharField(default='', max_length=128, verbose_name='Nome do recebedor')),
                ('receivers_bank', models.CharField(default='', max_length=128, verbose_name='Banco do recebedor')),
                ('receivers_agency', models.CharField(default='', max_length=128, verbose_name='Agência do recebedor')),
                ('receivers_account', models.CharField(default='', max_length=128, verbose_name='Conta do recebedor')),
                ('transfer_value', models.PositiveIntegerField(default=1, verbose_name='Valor da Transferência')),
                ('transfer_type', models.IntegerField(choices=[('CC', 'CC'), ('TED', 'TED'), ('DOC', 'DOC')], default='DOC', verbose_name='Tipo da transferência')),
                ('is_deleted', models.BooleanField(default=False)),
            ],
        ),
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('name', models.CharField(default='', max_length=128, verbose_name='Nome')),
                ('cnpj', models.CharField(default='', max_length=14, verbose_name='CNPJ')),
            ],
        ),
        migrations.AddField(
            model_name='transfer',
            name='user_id',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='transfers', to='nix_app.User', verbose_name='Transferências'),
        ),
    ]
