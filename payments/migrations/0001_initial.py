# Generated by Django 2.0.5 on 2018-05-31 13:50

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('accounts', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Payment',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('amount', models.DecimalField(decimal_places=10, max_digits=20)),
                ('direction', models.CharField(choices=[('incoming', 'Incoming'), ('outgoing', 'Outgoing')], max_length=8)),
                ('account', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='payments', to='accounts.Account')),
                ('to_account', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='accounts.Account')),
            ],
        ),
    ]
