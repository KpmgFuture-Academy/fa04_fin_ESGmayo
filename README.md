# 질소 산화물 발생량 예측 모델 
https://ixorell.netlify.app/nox%20web/

## gihub file 로드
```python
import os
import sys
!git clone https://github.com/KpmgFuture-Academy/fa04_fin_NOXTRUN
repo_path = os.path.abspath("fa04_fin_NOXTRUN")
sys.path.append(repo_path)
```

## 모델 학습
```python
## 1. 데이터 로딩
import pandas as pd
df = pd.read_csv(f"{os.path.abspath(os.getcwd())}/fa04_fin_NOXTRUN/datasets/영흥발전소.csv", encoding="cp949")

## 2. hyper parameters 설정
hogi = 3 # 3~4호기 정수값 입력.
multi_encoding = True
batch_size = 8
window_size = 4


## 3. 데이터 loader 객체 생성
from preprocessing.utils import preprocessing, torch_loader
train, val, test = preprocessing(df, hogi= hogi, multi_encoding= multi_encoding)
train_loader, val_loader, test_loader = torch_loader(train, val, test, batch_size= batch_size, window_size= window_size)

## 4. 모델 선언
from models.models import TimeSeries

features = len(train.columns.tolist()) -1
model = TimeSeries(in_ch= features, out_ch= 1, hidden_size= 128, multi_encoding= multi_encoding)

## 5. 모델 학습
from train.training import training
import torch
from torch.optim import Adam
from torch.nn import SmoothL1Loss
from utils import plot_train_val_loss

device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
optimizer = Adam(model.parameters(), lr=1e-4)

train_loss, val_loss = training(model=model,
                                optimizer= optimizer,
                                loss_fn=  SmoothL1Loss(),
                                num_epochs= 50,
                                train_loader= train_loader,
                                val_loader= val_loader,
                                device= device)
plot_train_val_loss(train_loss, val_loss)

## 6. test 결과 확인
from utils import make_result_df, plot_pred_target
from train.training import test
from matrix.matrix import  r2_score, rmse, AL1_loss

predict, target = test(test_loader, model, device)
pred_df = make_result_df(predict, target)

r2 = r2_score(target, predict)
print(f"R²Score: {r2:.4f}")

overall_rmse= rmse(target, predict)
print(f"RMSE: {overall_rmse:.4f}")

overall_loss = AL1_loss(target, predict)
print(f"AL1 Loss: {overall_loss:.4f}")

plot_pred_target(pred_df)
```

##
![Firebase](https://img.shields.io/badge/Firebase-%23FFCA28.svg?style=flat&logo=firebase&logoColor=white)
![HTML5](https://img.shields.io/badge/HTML5-%23E34F26.svg?style=flat&logo=html5&logoColor=white)
![CSS3](https://img.shields.io/badge/CSS3-%231572B6.svg?style=flat&logo=css3&logoColor=white)
![JavaScript](https://img.shields.io/badge/JavaScript-%23F7DF1E.svg?style=flat&logo=javascript&logoColor=black)
