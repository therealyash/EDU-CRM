from django.db import migrations, models

class Migration(migrations.Migration):

    dependencies = [
        ('core', '0006_alter_campaign_options_campaign_content_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='contact',
            name='position',
            field=models.CharField(blank=True, max_length=100),
        ),
    ]
