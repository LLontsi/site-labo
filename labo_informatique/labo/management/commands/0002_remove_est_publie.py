from django.db import migrations

class Migration(migrations.Migration):

    dependencies = [
        ('labo', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='presentation',
            name='est_publie',
        ),
    ]