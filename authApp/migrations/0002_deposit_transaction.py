# Generated by Django 3.2.7 on 2021-10-15 03:51

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('authApp', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Transaction',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('amount', models.IntegerField(default=0)),
                ('register_date', models.DateTimeField(auto_now_add=True)),
                ('note', models.CharField(max_length=100)),
                ('destiny_account', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='destiny', to='authApp.account')),
                ('origin_account', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='origin', to='authApp.account')),
            ],
        ),
        migrations.CreateModel(
            name='Deposit',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('amount', models.IntegerField(default=0)),
                ('register_date', models.DateTimeField(auto_now_add=True)),
                ('note', models.CharField(max_length=100)),
                ('depositer_name', models.CharField(max_length=50)),
                ('account', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='deposit_account', to='authApp.account')),
            ],
        ),
    ]