# Generated by Django 5.1.2 on 2024-12-08 12:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0003_campaign_remove_contact_owner'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='campaign',
            options={},
        ),
        migrations.RemoveField(
            model_name='campaign',
            name='owner',
        ),
        migrations.AddField(
            model_name='campaign',
            name='campaign_owner',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
        migrations.AlterField(
            model_name='campaign',
            name='name',
            field=models.CharField(max_length=200),
        ),
        migrations.AlterField(
            model_name='campaign',
            name='primary_communication_method',
            field=models.CharField(max_length=100),
        ),
        migrations.AlterField(
            model_name='campaign',
            name='type',
            field=models.CharField(max_length=100),
        ),
    ]
