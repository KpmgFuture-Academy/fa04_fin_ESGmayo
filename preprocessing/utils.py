import pandas as pd
import numpy as np
from sklearn.linear_model import LinearRegression
from sklearn.preprocessing import MinMaxScaler
import ast

def 호기(df, hogi):
    return df[df['호기'] == hogi].copy()

def preprocess_features(df, hogi, multi_encoding):
    df_ = 호기(df, hogi)
    df_['NOX'] = (df_['NOX'] * (46.0 / 22.4) * df_['유량'] * 1e-6)

    if multi_encoding:
        df_.drop(['호기', '일자', '가동시간', '발전최대', '발전최소', '대기시간', '가동시간_multi_hot'], axis=1, inplace=True)
    else:
        df_.drop(['호기', '일자', '발전최대', '가동시간_multi_hot', '발전최소', '대기시간'], axis=1, inplace=True)

    return df_.reset_index(drop=True)

def processing_split(train_df, val_df, test_df, hogi, multi_encoding):
    train_df_hogi = preprocess_features(train_df, hogi, multi_encoding)
    val_df_hogi = preprocess_features(val_df, hogi, multi_encoding)
    test_df_hogi = preprocess_features(test_df, hogi, multi_encoding)
    return train_df_hogi, val_df_hogi, test_df_hogi

def preprocessing(df, hogi, multi_encoding):
    df = df.copy()
    df['일자'] = pd.to_datetime(df['일자'])
    df['호기'] = df['호기'].astype(int)
    
    # ↓ 먼저 나누기
    train_df = df[:1872].reset_index(drop=True)
    val_df = df[1872:2340].reset_index(drop=True)
    test_df = df[2340:].reset_index(drop=True)
    
    # 유량 보정
    for i in [3, 4, 5, 6]:
        df_ = 호기(train_df, hogi=i)
        df_copy = df_[df_['유량'] != 0].copy()

        features = ['발전총량(MW)', '발전최대', '가동시간', '산소', '측정온도']
        model = LinearRegression().fit(df_copy[features], df_copy['유량'])

        zero_mask = df_['유량'] == 0
        df_.loc[zero_mask, '유량'] = model.predict(df_.loc[zero_mask, features])
        train_df.update(df_)

    if multi_encoding:
        df['가동시간_multi_hot'] = df['가동시간_multi_hot'].apply(ast.literal_eval)
        
        for i in range(24):
            df[f'{i+1}시 가동유무'] = df['가동시간_multi_hot'].apply(lambda x: x[i])

        train_df = df[:1872].reset_index(drop=True)
        val_df = df[1872:2340].reset_index(drop=True)
        test_df = df[2340:].reset_index(drop=True)

        # 이제 split
        train, val, test = processing_split(train_df, val_df, test_df, hogi, multi_encoding)

        # 여기서 '가동시간_multi_hot'은 이미 drop된 상태이므로 접근하지 않음!
        bin_feats = [f'{i+1}시 가동유무' for i in range(24)]
        features = ['발전총량(MW)', '유량', '산소', '측정온도', '온도', '습도', '풍속']

        minmax = MinMaxScaler()
        train[features] = minmax.fit_transform(train[features].astype('float32'))
        val[features] = minmax.transform(val[features].astype('float32'))
        test[features] = minmax.transform(test[features].astype('float32'))

        for df_ in [train, val, test]:
            df_[bin_feats] = df_[bin_feats].astype('float32')


    elif not multi_encoding:
        train_df = df[:1872].reset_index(drop=True)
        val_df = df[1872:2340].reset_index(drop=True)
        test_df = df[2340:].reset_index(drop=True)
        train, val, test = processing_split(train_df, val_df, test_df, hogi, multi_encoding)
        features = ['발전총량(MW)', '유량', '산소', '측정온도', '온도', '습도', '풍속', '가동시간']

        minmax = MinMaxScaler()
        train[features] = minmax.fit_transform(train[features].astype('float32'))
        val[features] = minmax.transform(val[features].astype('float32'))
        test[features] = minmax.transform(test[features].astype('float32'))

    else:
        raise ValueError("multi_encoding은 True 또는 False여야 합니다.")

    return train, val, test

import torch
from torch.utils.data import TensorDataset, DataLoader

class SlidingWindowDataset(torch.utils.data.Dataset):
    def __init__(self, df, features, target, window_size):
        self.x = df[features].values.astype('float32')
        self.y = df[target].values.astype('float32')
        self.window_size = window_size

    def __len__(self):
        return len(self.x) - self.window_size + 1

    def __getitem__(self, idx):
        x_window = self.x[idx : idx + self.window_size]       # 0~n행
        y_target = self.y[idx + self.window_size - 1]         # n행 (동일 종료점)
        return torch.tensor(x_window), torch.tensor([y_target], dtype=torch.float32)

def torch_loader(train, val, test, batch_size, window_size):
    
    target = 'NOX'
    features = [col for col in train.columns if col != target ]
    
    train_dataset = SlidingWindowDataset(train, features, target, window_size= window_size)
    train_loader = DataLoader(train_dataset, batch_size=batch_size, shuffle=False)
    val_dataset = SlidingWindowDataset(val, features, target, window_size= window_size)
    val_loader = DataLoader(val_dataset, batch_size=batch_size, shuffle=False)
    test_dataset = SlidingWindowDataset(test, features, target, window_size= window_size)
    test_loader = DataLoader(test_dataset, batch_size=batch_size, shuffle=False)
    return train_loader, val_loader, test_loader
