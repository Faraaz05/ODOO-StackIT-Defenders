# Generated by Django 5.2.4 on 2025-07-12 07:22

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('questions', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Answer',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('description', models.TextField()),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('author', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
                ('question', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='answers', to='questions.question')),
            ],
        ),
        migrations.CreateModel(
            name='Vote',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('vote_type', models.CharField(choices=[('question', 'Question'), ('answer', 'Answer')], max_length=10)),
                ('value', models.SmallIntegerField()),
                ('answer', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='questions.answer')),
                ('question', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='questions.question')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'unique_together': {('user', 'vote_type', 'question', 'answer')},
            },
        ),
    ]
