# Generated by Django 4.2.11 on 2024-04-18 23:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('post', '0007_tag_post_tags'),
    ]

    operations = [
        migrations.AlterField(
            model_name='post',
            name='tags',
            field=models.ManyToManyField(blank=True, to='post.tag'),
        ),
    ]
