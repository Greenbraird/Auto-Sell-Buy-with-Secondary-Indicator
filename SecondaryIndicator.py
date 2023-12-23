"업비트에서 데이터를 가져와 보조 지표를 만드는 모듈"
import pyupbit
import pandas as pd

# row 생략 없이 출력
pd.set_option('display.max_rows', None)
# col 생략 없이 출력
pd.set_option('display.max_columns', None)

def SMA(bitcoin = "KRW-BTC", bong = 'minute1'):
    df = pyupbit.get_ohlcv(bitcoin, bong, count=102)[['close']]

    #단순이동평균선 10 
    df["MA10"] = round(df['close'].rolling(window=10).mean(),5)

    #단순이동평균선 30
    df["MA30"] = round(df['close'].rolling(window=30).mean(),5)

    #단순이동평균선 100
    df["MA100"] = round(df['close'].rolling(window=100).mean(),5)
    

    return df.dropna()

def SMA_MACD(bitcoin = "KRW-BTC", bong = 'minute1', shorttrem = 12, longtrem =26): 
    df = pyupbit.get_ohlcv(bitcoin, bong)[['close']]
    df['STMA'] = df['close'].rolling(window=shorttrem).mean()

    df['LTMA'] = df['close'].rolling(window=longtrem).mean()

    df['MACD_L'] =  df['STMA'] - df['LTMA']

    df['signal'] = df['MACD_L'].rolling(window=9).mean()

    df['MACD_H'] = df['MACD_L'] - df['signal']
    return df.dropna()

def EMA_MACD(bitcoin = "KRW-BTC", bong = 'minute1', shorttrem = 12, longtrem =26):
    df = pyupbit.get_ohlcv(bitcoin, bong)[['close']]
    df['STMA'] = df['close'].ewm(span=shorttrem-1, min_periods=shorttrem).mean()

    df['LTMA'] = df['close'].ewm(span=longtrem-1,min_periods =longtrem).mean()

    df['MACD_L'] =  df['STMA'] - df['LTMA']

    df['signal'] = df['MACD_L'].ewm(span=8,min_periods =9).mean()

    df['MACD_H'] = abs(df['MACD_L']) - abs(df['signal'] )
    return df.dropna()

def EMA_RSI(bitcoin = "KRW-BTC", bong = 'minute15', period =14,data=25):

    try:
        df = pyupbit.get_ohlcv(bitcoin, bong,data)['close']
    except:
        df = pyupbit.get_ohlcv(bitcoin,period='minute15',count=25)['close']
    
    delta = df.diff()

    ups, downs = delta.copy(), delta.copy()

    ups[ups<0] = 0
    downs[downs>0] = 0
    au = ups.ewm(com = period-1, min_periods = period).mean()
    ad = downs.abs().ewm(com = period-1, min_periods = period).mean()
    RS = au/ad
    RSI = pd.DataFrame(100-(100/(1+RS)))

    return RSI.dropna()

def Bor(bitcoin = "KRW-BTC", bong = 'minute1'):
    df = pyupbit.get_ohlcv(bitcoin, bong)[['close']]

    #단순이동평균
    df["MA"] = df['close'].rolling(window=30).mean()

    #표준편차
    df["STD"] = df['close'].rolling(window=30).std()

    df['upper'] = df['MA'] + (df['STD'] * 2)
    df['lower'] = df['MA'] - (df['STD'] * 2)

    #band의 %값
    df['PB'] = (df['close']-df['lower']) / (df['upper']-df['lower'])

    #band의 폭
    df['BandWidth'] = (df['close'] - df['lower']) / df['MA'] * 100

if __name__ == '__main__':
    sma = SMA(bong="minute5")
    print(sma.iloc[1,1])
    print(sma)



