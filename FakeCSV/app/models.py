from django.db import models
from django.contrib.auth.models import User
# Create your models here.

COLUMN_SEPARATORS = (
    (',', 'Comma (,)'),
    (';', 'Semicolon (;)'),
    ('|', 'Pipe (|)'),
    (' ', 'Space ( )'),
    ('\\t', 'Tab (   )'),
)


STRING_CHARACTERS = (
    ('"', 'Double Quote (")'),
    ("'", "Single Quote (')"),
)


class Schema(models.Model):
    title = models.CharField(max_length=50)
    modified = models.DateField(auto_now=True)
    column_separator = models.CharField(max_length=25, choices=COLUMN_SEPARATORS)
    string_separator = models.CharField(max_length=25, choices=STRING_CHARACTERS)
    user = models.ForeignKey(User, on_delete=models.CASCADE)


class SchemaColumn(models.Model):
    column_name = models.CharField(max_length=50)
    type = models.CharField(max_length=20)
    order = models.IntegerField()
    min_number = models.IntegerField(blank=True, null=True)
    max_number = models.IntegerField(blank=True, null=True)
    table = models.ForeignKey(Schema, on_delete=models.CASCADE)

    def __str__(self):
        return self.column_name


class DataSet(models.Model):
    status = models.CharField(max_length=50)
    table = models.ForeignKey(Schema, on_delete=models.CASCADE)
    created = models.DateTimeField(auto_now_add=True)
    file = models.FileField(upload_to='csv')

    def __str__(self):
        return self.name

    @property
    def get_file_url(self):
        if self.file and hasattr(self.file, 'url'):
            return self.file.url
