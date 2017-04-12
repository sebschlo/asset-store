from __future__ import unicode_literals

from django.db import models
from django.core.validators import RegexValidator
from django.core.exceptions import ValidationError

# Create your models here.
class Asset(models.Model):
    name_validator = RegexValidator(
        r'^[0-9a-zA-Z][0-9a-zA-Z_-]{3,63}$',
        message='4-64 chars; only alphanumeric ascii, underscore and dash allowed; must start with alphanumeric.')
    name = models.CharField(max_length=64, unique=True, primary_key=True, validators=[name_validator])
    type_names = (
        ('satellite', 'Satellite Asset Type'),
        ('antenna', 'Antenna Asset Type')
    )
    asset_type = models.CharField(max_length=9, choices=type_names)
    class_names = (
        ('dove', 'Dove (satellite class)'),
        ('rapideye', 'Rapideye (satellite class)'),
        ('dish', 'Dish (antenna class)'),
        ('yagi', 'Yagi (antenna class)'),
    )
    asset_class = models.CharField(max_length=8, choices=class_names)

    def clean(self):
        # Don't allow non-compatible asset_classes
        if (self.asset_type == 'satellite' and (self.asset_class == 'dish' or self.asset_class == 'yagi')) or \
           (self.asset_type == 'antenna' and (self.asset_class == 'dove' or self.asset_class == 'rapideye')):
            raise ValidationError('Incompatible asset class for asset type')

    def __str__(self):
        return '%s' % self.name

    def __unicode__(self):
        return u'%s' % self.name

class AssetDetail(models.Model):
    asset = models.ForeignKey(Asset)
    key = models.CharField(max_length=20)
    type_names = (
        ('F', 'float'),
        ('B', 'boolean'),
        ('I', 'integer'),
        ('S', 'string')
    )
    val_type = models.CharField(max_length=1, choices=type_names)
    val = models.TextField(blank=True)

    # Override attribute getter to cast val into appropriate type
    @property
    def get_val(self):
        if self.val_type is 'S':
            return self.val
        elif self.val_type is 'I':
            return int(self.val)
        elif self.val_type is 'B':
            return bool(self.val)
        elif self.val_type is 'F':
            return float(self.val)

    # Override attribute setter to store val's type
    def __setattr__(self, key, val):
        if key == 'val' and val:
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
            super(AssetDetail, self).__setattr__(key, str(val))
        super(AssetDetail, self).__setattr__(key, val)

    def __str__(self):
        return '{%s, %s}' % (self.key, self.val)

    def __unicode__(self):
        return u'{%s, %s}' % (self.key, self.val)