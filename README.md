# 질소 산화물 발생량 예측 모델 
https://ixorell.netlify.app/nox%20web/

```python

import os
import sys

!git clone https://github.com/KpmgFuture-Academy/fa04_fin_NOXTRUN


repo_path = os.path.abspath("fa04_fin_NOXTRUN")
sys.path.append(repo_path)

from preprocessing.utils import preprocessing

import pandas as pd
df = pd.read_csv(f"{os.path.abspath(os.getcwd())}/fa04_fin_NOXTRUN/datasets/영흥발전소.csv", encoding="cp949")

hogi = 3 # 3~4호기 정수값 입력.
train, val, test = preprocessing(df, hogi= hogi, multi_encoding= True)

```

##
![Firebase](https://img.shields.io/badge/Firebase-%23FFCA28.svg?style=flat&logo=firebase&logoColor=white)
![HTML5](https://img.shields.io/badge/HTML5-%23E34F26.svg?style=flat&logo=html5&logoColor=white)
![CSS3](https://img.shields.io/badge/CSS3-%231572B6.svg?style=flat&logo=css3&logoColor=white)
![JavaScript](https://img.shields.io/badge/JavaScript-%23F7DF1E.svg?style=flat&logo=javascript&logoColor=black)
