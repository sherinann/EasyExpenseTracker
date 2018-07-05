# Generated by Django 2.0.7 on 2018-07-05 12:29

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('userprofile', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Budget',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=250)),
                ('color', models.IntegerField()),
                ('created', models.DateTimeField()),
                ('userprofile', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='userprofile.Profile')),
            ],
        ),
        migrations.CreateModel(
            name='BudgetCategory',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=250)),
                ('amount', models.DecimalField(decimal_places=2, max_digits=12)),
                ('created', models.DateTimeField()),
                ('budget', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='budget.Budget')),
            ],
        ),
        migrations.CreateModel(
            name='Expense',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('amount', models.DecimalField(decimal_places=2, max_digits=12)),
                ('created', models.DateTimeField()),
                ('category', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='budget.BudgetCategory')),
            ],
        ),
        migrations.CreateModel(
            name='Income',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=250)),
                ('amount', models.DecimalField(decimal_places=2, max_digits=12)),
                ('created', models.DateTimeField()),
                ('budget', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='budget.Budget')),
            ],
        ),
    ]
