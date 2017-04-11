from __future__ import unicode_literals

from django.db import models

# Create your models here.
class Asset(models.Model):
    name = models.CharField(max_length=64, unique=True, primary_key=True)
    type_names = (
        ('S', 'satellite'),
        ('A', 'antenna')
    )
    asset_type = models.CharField(max_length=1, choices=type_names)
    class_names = (
        ('D', 'dove'),
        ('R', 'rapideye'),
        ('I', 'dish',),
        ('Y', 'yagi')
    )
    asset_class = models.CharField(max_length=1, choices=class_names)

class AssetDetail(models.Model):
    asset = models.ForeignKey(Asset)
    key = models.CharField(max_length=20)
    type_names = (
        ('F', 'float'),
        ('B', 'boolean'),
        ('I', 'integer'),
        ('S', 'string')
    )
    val_type = models.CharField(max_length=1, choices=type_names, editable=False)
    val = models.TextField(blank=True)

    # Override attribute getter to cast val into appropriate type
    def __getattr__(self, attrname):
        if attrname == 'val':
            if self.val_type is 'S':
                return self.val
            elif self.val_type is 'I':
                return int(self.val)
            elif self.val_type is 'B':
                return bool(self.val)
            elif self.val_type is 'F':
                return float(self.val)
        else:
            return super(AssetDetail, self).__getattr__(attrname)

    # Override attribute setter to store val's type
    def __setattr__(self, attrname, val):
        if attrname == 'val':
            if type(val) is str:
                self.val_type = 'S'
            elif type(val) is int:
                self.val_type = 'I'
            elif type(val) is bool:
                self.val_type = 'B'
            elif type(val) is float:
                self.val_type = 'F'
            else:
                raise Exception('Unsupported type')
            self.val = str(val)
        else:
            super(AssetDetail, self).__setattr__(attrname, val)


