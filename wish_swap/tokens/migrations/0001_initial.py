# Generated by Django 3.1.5 on 2021-01-28 15:42

from django.db import migrations, models
import django.db.models.deletion
import encrypted_fields.fields


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Dex',
            fields=[
                ('name', models.CharField(max_length=100, primary_key=True, serialize=False)),
            ],
        ),
        migrations.CreateModel(
            name='Token',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('token_address', models.CharField(max_length=100)),
                ('token_abi', models.JSONField(default=None, null=True)),
                ('swap_address', models.CharField(max_length=100)),
                ('swap_owner', models.CharField(default='', max_length=100)),
                ('swap_abi', models.JSONField(default=None, null=True)),
                ('swap_secret', encrypted_fields.fields.EncryptedTextField(default='')),
                ('fee_address', models.CharField(max_length=100)),
                ('fee', models.IntegerField(default=None, null=True)),
                ('decimals', models.IntegerField()),
                ('symbol', models.CharField(max_length=50)),
                ('network', models.CharField(max_length=100)),
                ('is_original', models.BooleanField(default=False)),
                ('dex', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='tokens', to='tokens.dex')),
            ],
        ),
    ]
