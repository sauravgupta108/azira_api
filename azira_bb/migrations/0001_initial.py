# Generated by Django 3.0.3 on 2020-02-25 15:50

import azira_bb.models.utils
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
            name='AzUser',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=30)),
                ('hobbies', models.CharField(max_length=100)),
                ('city', models.CharField(blank=True, max_length=50, null=True)),
            ],
            bases=(models.Model, azira_bb.models.utils.TimeStamp),
        ),
        migrations.CreateModel(
            name='Designation',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=64)),
            ],
            bases=(models.Model, azira_bb.models.utils.TimeStamp),
        ),
        migrations.CreateModel(
            name='Organization',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50)),
                ('status', models.SmallIntegerField(choices=[(41, 'ACTIVE'), (42, 'INACTIVE')], default=41)),
            ],
            bases=(models.Model, azira_bb.models.utils.TimeStamp),
        ),
        migrations.CreateModel(
            name='Project',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50)),
                ('status', models.SmallIntegerField(choices=[(1, 'ACTIVE'), (2, 'INACTIVE'), (3, 'INITIATED'), (4, 'CLOSED'), (5, 'PROBLEM')], default=3)),
                ('start_date', models.DateField()),
                ('end_date', models.DateField(blank=True, null=True)),
            ],
            bases=(models.Model, azira_bb.models.utils.TimeStamp),
        ),
        migrations.CreateModel(
            name='Sprint',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50)),
                ('status', models.SmallIntegerField(choices=[(21, 'ACTIVE'), (22, 'INACTIVE'), (23, 'STUCK'), (24, 'COMPLETED')], default=22)),
                ('start_date', models.DateField()),
                ('end_date', models.DateField()),
                ('project', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='azira_bb.Project')),
            ],
            bases=(models.Model, azira_bb.models.utils.TimeStamp),
        ),
        migrations.CreateModel(
            name='Team',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=80)),
                ('lead', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='team_lead', to='azira_bb.AzUser')),
                ('manager', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='project_manager', to='azira_bb.AzUser')),
                ('members', models.ManyToManyField(related_name='team_member', to='azira_bb.AzUser')),
                ('project', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='azira_bb.Project')),
                ('sprint', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='azira_bb.Sprint')),
            ],
            bases=(models.Model, azira_bb.models.utils.TimeStamp),
        ),
        migrations.CreateModel(
            name='SprintFlow',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50)),
                ('options', models.TextField()),
                ('project', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='azira_bb.Project')),
                ('sprint', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='azira_bb.Sprint')),
            ],
            bases=(models.Model, azira_bb.models.utils.TimeStamp),
        ),
        migrations.CreateModel(
            name='ProjectAccess',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('owner', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='azira_bb.AzUser')),
                ('project', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='azira_bb.Project')),
            ],
            bases=(models.Model, azira_bb.models.utils.TimeStamp),
        ),
        migrations.CreateModel(
            name='Notification',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('content', models.CharField(max_length=500)),
                ('to', models.ManyToManyField(to='azira_bb.AzUser')),
            ],
            bases=(models.Model, azira_bb.models.utils.TimeStamp),
        ),
        migrations.CreateModel(
            name='Issue',
            fields=[
                ('id', models.CharField(max_length=20, primary_key=True, serialize=False, unique=True)),
                ('title', models.CharField(max_length=150)),
                ('description', models.TextField(blank=True, null=True)),
                ('assigned_to', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='azira_bb.AzUser')),
                ('flow', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='azira_bb.SprintFlow')),
                ('project', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='azira_bb.Project')),
                ('sprint', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='azira_bb.Sprint')),
            ],
            bases=(models.Model, azira_bb.models.utils.TimeStamp),
        ),
        migrations.CreateModel(
            name='Email',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('subject', models.CharField(max_length=128)),
                ('body', models.TextField()),
                ('to', models.ManyToManyField(to='azira_bb.AzUser')),
            ],
            bases=(models.Model, azira_bb.models.utils.TimeStamp),
        ),
        migrations.CreateModel(
            name='Comment',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('description', models.TextField()),
                ('by', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='azira_bb.AzUser')),
                ('issue', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='azira_bb.Issue')),
            ],
            bases=(models.Model, azira_bb.models.utils.TimeStamp),
        ),
        migrations.AddField(
            model_name='azuser',
            name='designation',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='azira_bb.Designation'),
        ),
        migrations.AddField(
            model_name='azuser',
            name='organization',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='azira_bb.Organization'),
        ),
        migrations.AddField(
            model_name='azuser',
            name='user',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
    ]
