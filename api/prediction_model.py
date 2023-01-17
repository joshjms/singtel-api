import pandas as pd
from datetime import datetime, timedelta
from xgboost import XGBRegressor

from app.models import Device
from app.serializers import PredictionSerializer

def run_prediction():
    data = PredictionSerializer(Device.objects.all(), many=True).data
    df_type = {}
    last_week_cnt = {}
    for data_idx in range(len(data)):
        data_dict = data[data_idx]['sales']
        offer = pd.DataFrame.from_dict(data[data_idx]['campaigns'])
        offer = offer.drop(columns=['id'])
        offer['start'] = pd.to_datetime(offer['start'], format='%Y-%m-%d')

        if len(data_dict)==0:
            continue

        df = pd.DataFrame.from_dict(data_dict)
        for j in range(len(df)):
            week = df.loc[j,'week']
            df.loc[j,'start_date'] = pd.to_datetime(week['start'], format='%Y-%m-%d')
            df.loc[j,'end_date'] = pd.to_datetime(week['start'], format='%Y-%m-%d')
        df = df.drop(columns=['week','id'])

        df['count'] = 0
        df['week'] = 0
        df['prv'] = 0
        week_cnt = 0
        for i in range(1,len(df)):
            df.loc[i,'week'] = week_cnt
            week_cnt += 1
            df.loc[i,'prv'] = df.loc[i-1, 'amount']

            for j in range(len(offer)):
                start_date = offer.iloc[j]['start']
                if df.iloc[i]['start_date'] <= start_date <= df.iloc[i]['end_date']:
                    df.loc[i,'count'] += offer.iloc[j]['amount']
        
        last_week_cnt[data[data_idx]['name']] = week_cnt

        df = df[1:]
        df_type[data[data_idx]['name']] = df.drop(columns=['start_date', 'end_date'])

    df_list = []
    for device_type in df_type:
        df_list.append(df_type[device_type])
    df_all = pd.concat(df_list, ignore_index=True)
    df_all = df_all.reset_index().drop(columns=['index'])

    x_train = df_all.drop(columns=['amount'])
    y_train = df_all['amount']
    model = XGBRegressor(n_estimators=1000, max_depth=6, subsample=0.7, colsample_bytree=0.9)
    model.fit(x_train, y_train)

    preds = {}
    for device in ['iPhone 14', 'Galaxy S22', 'Galaxy S23']:
        preds[device] = []
        date = None
        prv = None
        pred_ahead = None                
        if device == 'Galaxy S23':
            date = datetime.strptime('2023-02-12','%Y-%m-%d')
            prv = 115260
            pred_ahead = 6
            if device not in last_week_cnt:
                last_week_cnt[device] = 1
        elif device == 'Galaxy S22':
            date = datetime.strptime('2023-01-15','%Y-%m-%d')
            prv = 19270
            pred_ahead = 7
        else:
            date = datetime.strptime('2023-01-15','%Y-%m-%d')
            prv = 69850
            pred_ahead = 10

        week_cnt = last_week_cnt[device]
        for i in range(pred_ahead):
            features = {}
            start_date = date + timedelta(weeks=i)
            end_date = date + timedelta(weeks=i+1)
            features['count'] = 0
            for j in range(len(offer)):
                start_offer = offer.iloc[j]['start']
                if start_date <= start_offer < end_date:
                    features['count'] += offer.iloc[j]['amount']
            
            features['week'] = week_cnt
            week_cnt += 1
            
            features['prv'] = prv
            features_df = pd.DataFrame.from_dict([features])
            pred = model.predict(features_df)
            preds[device].append(pred[0])
            prv = pred[0]
    print(preds)
    return preds

# JV ORZZZZZZ AWOO