from django.db import migrations, models

class Migration(migrations.Migration):

    dependencies = [
        ('core', '0008_add_contact_address'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='contact',
            name='first_name',
        ),
        migrations.RemoveField(
            model_name='contact',
            name='last_name',
        ),
        migrations.RemoveField(
            model_name='contact',
            name='company',
        ),
        migrations.RemoveField(
            model_name='contact',
            name='position',
        ),
        migrations.RemoveField(
            model_name='contact',
            name='address',
        ),
        migrations.AddField(
            model_name='contact',
            name='name',
            field=models.CharField(default='', max_length=100),
            preserve_default=False,
        ),
    ]
