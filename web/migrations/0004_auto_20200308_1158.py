# Generated by Django 2.2 on 2020-03-08 11:58

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('web', '0003_auto_20200308_0029'),
    ]

    operations = [
        migrations.CreateModel(
            name='CategoriesModel',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('wrapper_folder', models.CharField(max_length=100, verbose_name='外层文件夹名')),
                ('category', models.CharField(max_length=50, verbose_name='分类名称')),
            ],
        ),
        migrations.AlterField(
            model_name='blogmodel',
            name='categories',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.DO_NOTHING, to='web.CategoriesModel', verbose_name='博客分类'),
            preserve_default=False,
        ),
    ]
