from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0004_alter_campaign_options_remove_campaign_owner_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='campaign',
            name='allocated_spending',
        ),
        migrations.RemoveField(
            model_name='campaign',
            name='campaign_source',
        ),
        migrations.RemoveField(
            model_name='campaign',
            name='estimated_cost_per_lead',
        ),
        migrations.RemoveField(
            model_name='campaign',
            name='marketing_channels',
        ),
        migrations.RemoveField(
            model_name='campaign',
            name='primary_communication_method',
        ),
        migrations.RemoveField(
            model_name='campaign',
            name='total_budget',
        ),
        migrations.RemoveField(
            model_name='campaign',
            name='tracking_code',
        ),
        migrations.RemoveField(
            model_name='campaign',
            name='utm_parameters',
        ),
        migrations.AddField(
            model_name='campaign',
            name='actual_cost',
            field=models.DecimalField(decimal_places=2, default=0, max_digits=10),
        ),
        migrations.AddField(
            model_name='campaign',
            name='budgeted_cost',
            field=models.DecimalField(decimal_places=2, default=0, max_digits=10),
        ),
        migrations.AddField(
            model_name='campaign',
            name='description',
            field=models.TextField(default=''),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='campaign',
            name='expected_response',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='campaign',
            name='expected_revenue',
            field=models.DecimalField(decimal_places=2, default=0, max_digits=10),
        ),
        migrations.AddField(
            model_name='campaign',
            name='numbers_sent',
            field=models.IntegerField(default=0),
        ),
        migrations.AlterField(
            model_name='campaign',
            name='campaign_owner',
            field=models.CharField(max_length=100),
        ),
        migrations.AlterField(
            model_name='campaign',
            name='status',
            field=models.CharField(choices=[('Draft', 'Draft'), ('Active', 'Active'), ('Completed', 'Completed'), ('Cancelled', 'Cancelled')], default='Draft', max_length=20),
        ),
    ]
