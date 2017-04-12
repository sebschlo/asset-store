from rest_framework import serializers
from assets.models import Asset, AssetDetail


class AssetSerializer(serializers.ModelSerializer):
    def validate(self, attrs):
        """
        Ensure valid asset classes are used
        """
        a_type = attrs.get('asset_type', '')
        a_class = attrs.get('asset_class', '')
        if (a_type == 'satellite' and (a_class == 'dish' or a_class == 'yagi')) or \
           (a_type == 'antenna' and (a_class == 'dove' or a_class == 'rapideye')):
            raise serializers.ValidationError('Incompatible asset class for asset type')
        return attrs

    class Meta:
        model = Asset
        fields = ('name', 'asset_type', 'asset_class')