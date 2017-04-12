from rest_framework import serializers
from assets.models import Asset, AssetDetail

class AssetDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = AssetDetail
        fields = ('key', 'val_type', 'val')

class AssetSerializer(serializers.ModelSerializer):
    details = AssetDetailSerializer(source='assetdetail_set', many=True)

    def validate(self, attrs):
        """
        Ensure valid asset classes and asset details are used
        """
        # Ensure valid asset class
        a_type = attrs.get('asset_type', '')
        a_class = attrs.get('asset_class', '')
        if (a_type == 'satellite' and (a_class == 'dish' or a_class == 'yagi')) or \
           (a_type == 'antenna' and (a_class == 'dove' or a_class == 'rapideye')):
            raise serializers.ValidationError('Incompatible asset class for asset type')

        # Ensure only acceptable asset details are used
        details = attrs.get('assetdetail_set', [])
        for det in details:
            key = det.get('key', '')
            val_type = det.get('val_type', '')
            if a_class == 'dish':
                if not ((key == 'diameter' and val_type == 'F') or \
                        (key == 'radome' and val_type == 'B')):
                    raise serializers.ValidationError('Incompatible asset detail for dish')
            if a_class == 'yagi':
                if not (key == 'gain' and val_type == 'F'):
                    raise serializers.ValidationError('Unexpected asset detail for yagi')

        return attrs

    def create(self, validated_data):
        details_data = validated_data.pop('assetdetail_set')
        asset = Asset.objects.create(**validated_data)

        # Create related objects
        for det in details_data:
            AssetDetail.objects.create(asset=asset, **det)

        return asset

    class Meta:
        model = Asset
        fields = ('name', 'asset_type', 'asset_class', 'details')