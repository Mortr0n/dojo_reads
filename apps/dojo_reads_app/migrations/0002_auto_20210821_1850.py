# Generated by Django 2.2 on 2021-08-22 00:50

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('dojo_reads_app', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='book',
            name='added_by',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='books_added', to='login_registration_app.User'),
        ),
    ]