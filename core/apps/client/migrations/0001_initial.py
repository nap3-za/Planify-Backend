# Generated by Django 4.2.11 on 2025-01-28 08:46

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='ClientProfile',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=125, verbose_name='name')),
                ('code', models.CharField(max_length=5, verbose_name='code')),
                ('details', models.TextField(blank=True)),
                ('rank', models.CharField(choices=[('AVG', 'Average'), ('GDD', 'Good'), ('BAD', 'Bad')], default='AVG', max_length=3, verbose_name='rank')),
                ('status', models.CharField(choices=[('ACT', 'Active'), ('LEG', 'Legacy'), ('ICT', 'Inactive')], default='ACT', max_length=3, verbose_name='status')),
                ('relation_timestamp', models.DateField(null=True, verbose_name='relation timestamp')),
                ('timestamp', models.DateTimeField(auto_now_add=True)),
            ],
        ),
    ]
