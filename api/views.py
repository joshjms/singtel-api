from xgboost import XGBRegressor
import json
from datetime import datetime, timedelta
import pandas as pd
from django.shortcuts import render

from app.models import Producer, Device, Week, Sale, PredictedSale, Transaction
from app.serializers import ProducerSerializer, DeviceInfoSerializer, WeekInfoSerializer, DeviceSaleSerializer, DevicePredictedSaleSerializer, WeekSaleSerializer, WeekPredictedSaleSerializer, SaleSerializer, PredictedSaleSerializer, DeviceSerializer, WeekSerializer, TransactionInfoSerializer, TransactionSerializer, PredictionSerializer

from requests import api
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAdminUser, IsAuthenticated, AllowAny

from django.http import JsonResponse

from datetime import datetime


@api_view(["GET"])
def sale_list(request):
    sales = Sale.objects.all()
    serializer = SaleSerializer(sales, many=True)
    return JsonResponse(
        data=serializer.data,
        safe=False,
        status=200,
    )


@api_view(["GET"])
def device_list(request):
    devices = Device.objects.all()
    serializer = DeviceInfoSerializer(devices, many=True)
    return JsonResponse(
        data=serializer.data,
        safe=False,
        status=200,
    )


@api_view(["GET"])
def device_detail(request):
    device_name = request.GET['device']

    if Device.objects.filter(name=device_name).exists() == False:
        return JsonResponse(
            data={
                'message': 'Device Type Not Found'
            },
            safe=False,
            status=404,
        )

    device = Device.objects.get(name=device_name)
    serializer = DeviceSerializer(device)

    return JsonResponse(
        data=serializer.data,
        safe=False,
        status=200,
    )


@api_view(["GET"])
def transaction_list(request):
    transactions = Transaction.objects.all()
    serializer = TransactionSerializer(transactions, many=True)

    return JsonResponse(
        data=serializer.data,
        safe=False,
        status=200,
    )


@api_view(["GET"])
def device_train(request):
    devices = Device.objects.all()
    serializer = PredictionSerializer(devices, many=True)
    return JsonResponse(
        data=serializer.data,
        safe=False,
        status=200,
    )

from .prediction_model import run_prediction

@api_view(["POST"])
def run_prediction_model(request):
    predictions = run_prediction()

    devices = Device.objects.all()
    for device in devices:
        device_data = DeviceSerializer(device).data
        device_name = device_data['name']
        device_eol = device_data['isEOL']
        if device_eol == True:
            continue
        device_sales = sorted(device_data['sales'], key=lambda d: d['week']['id'])
        if len(device_sales) > 0:
            last_sale_week = int(device_sales[-1]['week']['id'])
        else:
            last_sale_week = 54
        for w in range(last_sale_week + 1, last_sale_week + 1 + len(predictions[device_name])):
            week = Week.objects.get(id=w)
            amount = predictions[device_name][w - last_sale_week - 1]
            obj, created = PredictedSale.objects.update_or_create(
                week=week, device=device,
                defaults={'device': device, 'week': week, 'amount': amount}
            )

    return JsonResponse(
        data={
            'message': 'Prediction model ran successfully!',
        },
        safe=False,
        status=201,
    )

@api_view(["POST"])
def sale_create(request):
    data = request.data
    week = Week.objects.get(start__lte=datetime.now(), end__gte=datetime.now())
    amount = data['amount']
    device = Device.objects.get(name=data['device'])

    obj, created = Sale.objects.update_or_create(
        week=week,
        defaults={'device': device, 'week': week, 'amount': amount}
    )

    return JsonResponse(
        data={
            'message': 'Data updated successfully!',
        },
        safe=False,
        status=201,
    )
