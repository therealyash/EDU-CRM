from django.db import migrations, models

class Migration(migrations.Migration):

    dependencies = [
        ('core', '0007_add_contact_position'),
    ]

    operations = [
        migrations.AddField(
            model_name='contact',
            name='address',
            field=models.TextField(blank=True),
        ),
    ]
