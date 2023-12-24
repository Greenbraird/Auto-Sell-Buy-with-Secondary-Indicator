## RSI-and-SMA-Strategy-by-upbit

Python Auto Sell and Buy for Upbit Api

version : 2.1.0
<br>2.1.0 추가된 기능

1. 손절기능(기본적으로 그 라인에서 사졌을 때만 작동)
ex. SOL-KRW가 1번방에는 사졌고 3번방에서는 안 사졌으면
1번방에서만 손절기능이 작동하고 3번방에서는 조건이 되어도 작동하지 않음

2. log 기능
무엇이 사졌는지 팔아졌는지 확인할 수 있음

3. 전날 종가와 오늘 고가가 10%를 넘어가면 제외되고 2일 뒤에 돌아옴.
(가지고 있었다면 전부 매도 후 제외됨)

4. 반등시 익절 기능
하락장이라고 판단 되었을 때,
0.3%이상 반등하서 올라가면 가지고 있는 코인에 25%를 매도

5. 코인 갯수 50개까지 증가


## Documentation
https://pyupbit.readthedocs.io/en/latest/
</br>https://github.com/sharebook-kr/pyupbit

## installation

```
pip install pyupbit
pip install pandas
```

## 공지

본 프로그램을 사용해서 얻은 **이익및 손해**는 **본인**에게 있음을 알려드립니다.
SecondaryIndicator.py 안에 RSI 뿐만 아니라 SMA_MACD, EMA_MACD, SMA, Bollinger Bands등 다양한 보조지표들이 존재하므로
자신에게 맞는 매매 방법을 찾았다면 응용해 사용하실 수 있습니다.

## 사용법

1. 시작
![스크린샷 2023-11-28 000609](https://github.com/Greenbraird/Auto-Sell-Buy-with-Secondary-Indicator/assets/87434273/e65f650e-7be0-4fb1-8c16-19038358914a)

main을 실행하면 위와 같이 두개의 창이 나오게 되는데 하는 코인을 자동으로 돌릴 코인을 선택하는 창이고 하나는 자동을 돌리기 전 세팅하는 창입니다.

2. 로그인
![스크린샷 2023-11-28 000854](https://github.com/Greenbraird/Auto-Sell-Buy-with-Secondary-Indicator/assets/87434273/0abd0457-2042-4332-86b0-71772d2bcb67)

위 초록 부분에 자신의 Upbit API access키와 secret키를 넣고 로그인 버튼을 부르면

![스크린샷 2023-11-28 001037](https://github.com/Greenbraird/Auto-Sell-Buy-with-Secondary-Indicator/assets/87434273/1734d982-af22-4613-b452-28651991af5e)

자신의 KRW 잔고가 나타나게 됩니다.

3. 코인 선택

![스크린샷 2023-11-28 001246](https://github.com/Greenbraird/Auto-Sell-Buy-with-Secondary-Indicator/assets/87434273/c9cb5c8d-5571-4121-ba6a-7fd338de0f0b)

자신이 원하는 코인 선택 후 확인 버튼을 누르면 창이 꺼지면

![스크린샷 2023-11-28 001421](https://github.com/Greenbraird/Auto-Sell-Buy-with-Secondary-Indicator/assets/87434273/cc3e1861-6357-44c6-8e52-62eafba8e41e)

다음과 같이 빨간불에서 노란불로 바꿔게 됩니다.

4. 세팅 값 조정

![스크린샷 2023-11-28 001635](https://github.com/Greenbraird/Auto-Sell-Buy-with-Secondary-Indicator/assets/87434273/897439a5-7070-4cdd-9c1d-a6ba6ac27940)

이후 셋팅 값을 조절 후 자동을 눌려 주면

![스크린샷 2023-11-28 001721](https://github.com/Greenbraird/Auto-Sell-Buy-with-Secondary-Indicator/assets/87434273/d8ce06d0-1b43-40c0-91e1-2ec00ec75ac9)
![스크린샷 2023-11-28 001752](https://github.com/Greenbraird/Auto-Sell-Buy-with-Secondary-Indicator/assets/87434273/9858b817-133f-469f-8ee6-6de1d353a67b)

이렇게 돌아가게 됩니다.

5. 코인 리스트 조정

이후에 거래를 잠시 중단하고 싶거나 거래를 다시 하고 싶은 코인이 생기면 
![스크린샷 2023-11-28 001835](https://github.com/Greenbraird/Auto-Sell-Buy-with-Secondary-Indicator/assets/87434273/b52e479c-dc34-4db3-93da-c9b6e8899413)

코인 리스크 클릭 후 

![스크린샷 2023-11-28 003943](https://github.com/Greenbraird/Auto-Sell-Buy-with-Secondary-Indicator/assets/87434273/356e8f15-67f0-4f85-b8a4-98d85d94bf75)

coin list 창에서 유동적으로 관리 할 수 있습니다.

## 추가되어야 할 기능
1. 전날 높은 상승장으로 마감한 종목들은 하락을 대비해 잠시 자동 거래에서 제외
2. 비 로그인시 자동을 돌렸을 때 팅기는 문제 해결
3. SecondaryIndicator.py 더 많은 지표 값 추가하기
