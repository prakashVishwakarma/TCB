# Generated by Django 5.1 on 2024-11-07 13:31

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Cake',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('discount', models.DecimalField(decimal_places=2, max_digits=10)),
                ('name', models.CharField(max_length=255)),
                ('price', models.DecimalField(decimal_places=2, max_digits=10)),
                ('weight', models.DecimalField(decimal_places=2, max_digits=10)),
                ('earliest_delivery', models.CharField(max_length=255)),
                ('unique_quality', models.CharField(max_length=255)),
                ('CakeMessage', models.CharField(max_length=255)),
            ],
        ),
        migrations.CreateModel(
            name='CakeCareGuidelines',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('cake_care_guidelines', models.CharField(max_length=255)),
            ],
        ),
        migrations.CreateModel(
            name='CakeCategory',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('cake_image', models.URLField(max_length=500)),
                ('category_name', models.CharField(max_length=255)),
            ],
        ),
        migrations.CreateModel(
            name='CakeFlavour',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('cake_flavour', models.CharField(max_length=500)),
            ],
        ),
        migrations.CreateModel(
            name='CakeImage',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('cake_image', models.URLField(max_length=500)),
            ],
        ),
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('cake_image', models.URLField(max_length=500)),
                ('category_name', models.CharField(max_length=255)),
            ],
        ),
        migrations.CreateModel(
            name='ClientsSayAboutUs',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('client_says', models.CharField(max_length=255)),
                ('client_name', models.CharField(max_length=255)),
            ],
        ),
        migrations.CreateModel(
            name='DeliverySpecifics',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('delivery_specifics', models.CharField(max_length=255)),
            ],
        ),
        migrations.CreateModel(
            name='ExploreMoreWithUs',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('cake_image', models.URLField(max_length=500)),
                ('cake_name', models.CharField(max_length=255)),
                ('price', models.DecimalField(decimal_places=2, max_digits=10)),
            ],
        ),
        migrations.CreateModel(
            name='FinishType',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('finish_type', models.CharField(max_length=500)),
            ],
        ),
        migrations.CreateModel(
            name='ImageCarousel',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('cake_image', models.URLField(max_length=500)),
            ],
        ),
        migrations.CreateModel(
            name='KindlyNote',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('kindly_note', models.CharField(max_length=255)),
            ],
        ),
        migrations.CreateModel(
            name='OurBestsellers',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('cake_image', models.URLField(max_length=500)),
                ('cake_name', models.CharField(max_length=255)),
            ],
        ),
        migrations.CreateModel(
            name='SpongeType',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('sponge_type', models.CharField(max_length=500)),
            ],
        ),
        migrations.CreateModel(
            name='TrendingNow',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('cake_image', models.URLField(max_length=500)),
                ('cake_name', models.CharField(max_length=255)),
                ('price', models.DecimalField(decimal_places=2, max_digits=10)),
            ],
        ),
        migrations.CreateModel(
            name='UserModel',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('full_name', models.CharField(max_length=255)),
                ('email', models.EmailField(max_length=255, unique=True)),
                ('password', models.CharField(max_length=255)),
                ('mobile_number', models.CharField(blank=True, max_length=15, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='AddToCart',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('quantity', models.DecimalField(decimal_places=2, max_digits=10)),
                ('cake', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='App.cake')),
                ('user_model', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='App.usermodel')),
            ],
        ),
        migrations.AddField(
            model_name='cake',
            name='cake_flavour',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='App.cakeflavour'),
        ),
        migrations.AddField(
            model_name='cake',
            name='cake_image',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='App.cakeimage'),
        ),
        migrations.AddField(
            model_name='cake',
            name='category',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='App.category'),
        ),
        migrations.AddField(
            model_name='cake',
            name='finish_type',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='App.finishtype'),
        ),
        migrations.CreateModel(
            name='ProductDescription',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('cake_care_guidelines', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='App.cakecareguidelines')),
                ('delivery_specifics', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='App.deliveryspecifics')),
                ('kindly_note', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='App.kindlynote')),
            ],
        ),
        migrations.AddField(
            model_name='cake',
            name='product_pescription',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='App.productdescription'),
        ),
        migrations.AddField(
            model_name='cake',
            name='sponge_type',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='App.spongetype'),
        ),
        migrations.CreateModel(
            name='Personalization',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('add_delivery_date', models.DecimalField(decimal_places=2, max_digits=10)),
                ('add_delivery_time', models.DecimalField(decimal_places=2, max_digits=10)),
                ('personal_message', models.CharField(max_length=255)),
                ('name', models.CharField(max_length=255)),
                ('number', models.DecimalField(decimal_places=2, max_digits=15)),
                ('add_to_cart', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='App.addtocart')),
                ('user_model', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='App.usermodel')),
            ],
        ),
        migrations.CreateModel(
            name='CakeOrderHistory',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('discount', models.DecimalField(decimal_places=2, max_digits=10)),
                ('name', models.CharField(max_length=255)),
                ('price', models.DecimalField(decimal_places=2, max_digits=10)),
                ('weight', models.DecimalField(decimal_places=2, max_digits=10)),
                ('earliest_delivery', models.CharField(max_length=255)),
                ('unique_quality', models.CharField(max_length=255)),
                ('cake_message', models.CharField(max_length=255)),
                ('quantity', models.DecimalField(decimal_places=2, max_digits=10)),
                ('ordered_on', models.CharField(max_length=255)),
                ('order_id', models.DecimalField(decimal_places=2, max_digits=10)),
                ('status', models.CharField(max_length=255)),
                ('shipping_address', models.CharField(max_length=255)),
                ('payment_method', models.CharField(max_length=255)),
                ('cake_flavour', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='App.cakeflavour')),
                ('cake_image', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='App.cakeimage')),
                ('category', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='App.category')),
                ('finish_type', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='App.finishtype')),
                ('product_pescription', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='App.productdescription')),
                ('sponge_type', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='App.spongetype')),
                ('user_model', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='App.usermodel')),
            ],
        ),
        migrations.CreateModel(
            name='Addresses',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('flat_no', models.CharField(max_length=255)),
                ('street', models.CharField(max_length=255)),
                ('society_name', models.CharField(max_length=255)),
                ('area', models.CharField(max_length=255)),
                ('landmark', models.CharField(max_length=255)),
                ('google_location_url', models.URLField(max_length=255)),
                ('pincode', models.DecimalField(decimal_places=2, max_digits=10)),
                ('city', models.CharField(max_length=255)),
                ('mobile_number', models.CharField(blank=True, max_length=15, null=True)),
                ('alternate_mobile_number', models.CharField(blank=True, max_length=15, null=True)),
                ('address_type', models.CharField(max_length=255)),
                ('user_model', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='App.usermodel')),
            ],
        ),
    ]
