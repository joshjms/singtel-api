from rest_framework import serializers

from .models import Producer, Device, Week, Sale, PredictedSale, Transaction, Campaign


class ProducerSerializer (serializers.ModelSerializer):
    class Meta:
        model = Producer
        fields = ('id', 'name')


class DeviceInfoSerializer (serializers.ModelSerializer):
    producer = ProducerSerializer(read_only=True)

    class Meta:
        model = Device
        fields = ('id', 'name', 'producer', 'isEOL')


class WeekInfoSerializer (serializers.ModelSerializer):
    class Meta:
        model = Week
        fields = ('id', 'start', 'end')


class DeviceSaleSerializer (serializers.ModelSerializer):
    week = WeekInfoSerializer(read_only=True)

    class Meta:
        model = Sale
        fields = ('id', 'week', 'amount')


class WeekSaleSerializer (serializers.ModelSerializer):
    device = DeviceInfoSerializer(read_only=True)

    class Meta:
        model = Sale
        fields = ('id', 'device', 'amount')


class DevicePredictedSaleSerializer(serializers.ModelSerializer):
    week = WeekInfoSerializer(read_only=True)

    class Meta:
        model = PredictedSale
        fields = ('id', 'week', 'amount')


class WeekPredictedSaleSerializer(serializers.ModelSerializer):
    device = DeviceInfoSerializer(read_only=True)

    class Meta:
        model = PredictedSale
        fields = ('id', 'device', 'amount')


class SaleSerializer(serializers.ModelSerializer):
    device = DeviceInfoSerializer(read_only=True)
    week = WeekInfoSerializer(read_only=True)

    class Meta:
        model = Sale
        fields = ('id', 'device', 'week', 'amount')


class PredictedSaleSerializer(serializers.ModelSerializer):
    device = DeviceInfoSerializer(read_only=True)
    week = WeekInfoSerializer(read_only=True)

    class Meta:
        model = PredictedSale
        fields = ('id', 'device', 'week', 'amount')


class CampaignSerializer (serializers.ModelSerializer):
    class Meta:
        model = Campaign
        fields = ('id', 'start', 'end', 'amount')


class WeekSerializer (serializers.ModelSerializer):
    producer = ProducerSerializer(read_only=True)
    sales = WeekSaleSerializer(many=True, read_only=True)
    predicted = WeekPredictedSaleSerializer(many=True, read_only=True)

    class Meta:
        model = Device
        fields = ('id', 'name', 'producer', 'sales', 'predicted')


class TransactionInfoSerializer (serializers.ModelSerializer):
    class Meta:
        model = Transaction
        fields = ('id', 'transactionType', 'transactionDate', 'amount')


class DeviceSerializer (serializers.ModelSerializer):
    producer = ProducerSerializer(read_only=True)
    sales = DeviceSaleSerializer(many=True, read_only=True)
    predicted = DevicePredictedSaleSerializer(many=True, read_only=True)
    transactions = TransactionInfoSerializer(many=True, read_only=True)
    campaigns = CampaignSerializer(many=True, read_only=True)

    class Meta:
        model = Device
        fields = ('id', 'name', 'producer', 'sales',
                  'predicted', 'transactions', 'campaigns', 'isEOL')


class PredictionSerializer (serializers.ModelSerializer):
    sales = DeviceSaleSerializer(many=True, read_only=True)
    campaigns = CampaignSerializer(many=True, read_only=True)

    class Meta:
        model = Device
        fields = ('id', 'name', 'sales', 'campaigns')


class TransactionSerializer (serializers.ModelSerializer):
    device = DeviceInfoSerializer(read_only=True)

    class Meta:
        model = Transaction
        fields = ('id', 'transactionType',
                  'transactionDate', 'device', 'amount')
