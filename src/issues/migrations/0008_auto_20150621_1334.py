# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.core.files.storage
import issues.models


class Migration(migrations.Migration):

    dependencies = [
        ('issues', '0007_auto_20150617_2036'),
    ]

    operations = [
        migrations.AlterField(
            model_name='issueattachment',
            name='file',
            field=models.FileField(storage=django.core.files.storage.FileSystemStorage(b'F:\\projects_with_udi\\OpenCommunity\\uploads'), upload_to=issues.models.issue_attachment_path, max_length=200, verbose_name='File'),
        ),
    ]
