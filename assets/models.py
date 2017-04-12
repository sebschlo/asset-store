from __future__ import unicode_literals

from django.db import models
from django.core.validators import RegexValidator
from django.core.exceptions import ValidationError

# Create your models here.
class Asset(models.Model):
    """
    The Asset is the main object for this project. It holds the name, type and class fields, which describe it. 
    """
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
        """
        Don't allow non-compatible asset_classes
        """
        if (self.asset_type == 'satellite' and (self.asset_class == 'dish' or self.asset_class == 'yagi')) or \
           (self.asset_type == 'antenna' and (self.asset_class == 'dove' or self.asset_class == 'rapideye')):
            raise ValidationError('Incompatible asset class for asset type')

    def __str__(self):
        return '%s' % self.name

    def __unicode__(self):
        return u'%s' % self.name


class AssetDetail(models.Model):
    """
    The AssetDetail is a generic key/value object, which is related to the Asset.
    Additionally, it specifies which type the value has, and allows for retrieving
    the value already cast in the appropriate type.
    """
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

    @property
    def get_val(self):
        """
        Override attribute getter to cast val into appropriate type
        """
        if self.val_type is 'S':
            return self.val
        elif self.val_type is 'I':
            return int(self.val)
        elif self.val_type is 'B':
            return bool(self.val)
        elif self.val_type is 'F':
            return float(self.val)


    def __setattr__(self, key, val):
        """
        Override attribute setter to store val's type
        """
        if key == 'val' and val and not self.val_type:
            if type(val) is str or type(val) is unicode:
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

    def clean(self):
        """
        Add validation here so that you can't add erroneous details in the admin site  
        """
        if self.asset.asset_class == 'dish':
            if not ((self.key == 'diameter' and self.val_type == 'F') or \
                            (self.key == 'radome' and self.val_type == 'B')):
                raise ValidationError('Unexpected asset detail for dish')

        if self.asset.asset_class == 'yagi':
            if not (self.key == 'gain' and self.val_type == 'F'):
                raise ValidationError('Unexpected asset detail for yagi')

    def __str__(self):
        return '{%s: %s}' % (self.key, self.val)

    def __unicode__(self):
        return u'{%s: %s}' % (self.key, self.val)