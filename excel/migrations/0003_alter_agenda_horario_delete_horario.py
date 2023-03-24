# Generated by Django 4.1.7 on 2023-03-24 20:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('excel', '0002_horario_alter_service_numeracion_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='agenda',
            name='horario',
            field=models.CharField(choices=[('09', '09:00 AM'), ('10', '10:00 AM'), ('11', '11:00 AM'), ('12', '12:00 PM'), ('', ''), ('17', '05:00 PM'), ('18', '06:00 PM'), ('19', '07:00 PM'), ('20', '08:00 PM'), ('21', '09:00 PM'), ('22', '10:00 PM')], max_length=10),
        ),
        migrations.DeleteModel(
            name='Horario',
        ),
    ]
