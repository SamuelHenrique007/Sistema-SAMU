from django.db import migrations


class Migration(migrations.Migration):
    dependencies = [
        ('admin_app', '0001_initial'),
    ]

    operations = [
        migrations.DeleteModel(
            name='SenhaUsuario',
        ),
    ]

