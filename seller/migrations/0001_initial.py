# Generated by Django 4.0.3 on 2022-04-26 05:11

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Seller',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('fname', models.CharField(max_length=40)),
                ('lname', models.CharField(max_length=40)),
                ('Email', models.EmailField(max_length=254, unique=True)),
                ('password', models.CharField(max_length=40)),
                ('mobile', models.CharField(max_length=12)),
            ],
        ),
        migrations.CreateModel(
            name='Product',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('product_name', models.CharField(max_length=50)),
                ('product_description', models.TextField()),
                ('product_pic', models.FileField(default='', upload_to='product')),
                ('product_price', models.IntegerField()),
                ('quantity', models.IntegerField()),
                ('product_owner', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='seller.seller')),
            ],
        ),
    ]
