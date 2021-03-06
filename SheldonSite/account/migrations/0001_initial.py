# Generated by Django 3.2.9 on 2022-01-14 17:55

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Profile',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('user_rank', models.IntegerField(choices=[(0, 'Admin'), (1, 'Uprzywilejowany'), (2, 'Zwykly'), (3, 'Gosc'), (4, 'Niepotwierdzony')], default=4, verbose_name='Ranga')),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'Uprawnienia dodatkowe',
                'verbose_name_plural': 'Uprawnienia dodatkowe',
            },
        ),
    ]
