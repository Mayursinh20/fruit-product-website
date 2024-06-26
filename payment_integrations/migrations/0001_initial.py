# Generated by Django 5.0.6 on 2024-05-16 12:31

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Payment',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('status', models.CharField(choices=[('SUCCESS', 'success'), ('FAILURE', 'failure'), ('PENDING', 'pending')], max_length=100, null=True)),
                ('amount', models.CharField(max_length=225, null=True)),
                ('razorpay_payment_id', models.CharField(blank=True, help_text='Razorpay payment id', max_length=255, null=True, unique=True, verbose_name='Razorpay payment id')),
                ('razorpay_order_id', models.CharField(help_text='Razorpay order id', max_length=255, verbose_name='Razorpay order id')),
                ('razorpay_signature', models.CharField(blank=True, help_text='Razorpay signature', max_length=255, null=True, verbose_name='Razorpay signature')),
                ('user', models.ForeignKey(help_text='User of Razorpay', on_delete=django.db.models.deletion.CASCADE, related_name='pg_razorpay_user', to=settings.AUTH_USER_MODEL, verbose_name='User of Razorpay')),
            ],
            options={
                'verbose_name': 'Razorpay Payment Detail',
                'verbose_name_plural': 'Razorpay Payment Details',
                'db_table': 'razorpay_details',
            },
        ),
    ]
