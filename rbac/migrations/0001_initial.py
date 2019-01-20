# Generated by Django 2.1.4 on 2019-01-19 12:37

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Menu',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('title', models.CharField(max_length=32, verbose_name='一级菜单名称')),
                ('icon', models.CharField(max_length=32, verbose_name='图标')),
            ],
        ),
        migrations.CreateModel(
            name='Permission',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('title', models.CharField(max_length=32, verbose_name='标题')),
                ('url', models.CharField(max_length=128, verbose_name='含正则的URL')),
                ('name', models.CharField(max_length=32, unique=True, verbose_name='URL的别名')),
                ('menu', models.ForeignKey(blank=True, help_text='null表示不是菜单,非null表示是二级菜单', null=True, on_delete=True, to='rbac.Menu', verbose_name='所属菜单')),
                ('pid', models.ForeignKey(blank=True, help_text='对于非菜单权限需要选择一个可以成为菜单的权限，用户做默认展开和选中菜单', null=True, on_delete=True, related_name='parent', to='rbac.Permission', verbose_name='关联的权限')),
            ],
        ),
        migrations.CreateModel(
            name='Role',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('title', models.CharField(max_length=32, verbose_name='角色昵称')),
                ('permission', models.ManyToManyField(blank=True, to='rbac.Permission', verbose_name='所拥有的权限')),
            ],
        ),
        migrations.CreateModel(
            name='UserInfo',
            fields=[
                ('create_data', models.DateField(auto_created=True, null=True)),
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('username', models.CharField(max_length=32, verbose_name='用户名')),
                ('email', models.EmailField(max_length=254, null=True, verbose_name='邮箱')),
                ('password', models.CharField(max_length=16, verbose_name='密码')),
                ('roles', models.ManyToManyField(to='rbac.Role', verbose_name='用户的角色')),
            ],
        ),
    ]
