import SecondaryIndicator
import pyupbit
import time

def strategy_RSI(upbit ,bitcoin, delay_buy_time, bong ,buy_count =4, buy_price =5000,max_buy_count = 4, delay_time = 60, buy_rsi=30, sell_rsi=70):

    my_balances = upbit.get_balances()
    
    #이 친구를 new main으로 빼자
    for i in my_balances:

        if i['currency'] == bitcoin[4:]:
            avg_buy_price = float(i['avg_buy_price'])
            volum = float(i['balance'])
        
        else:
            avg_buy_price = 0
            volum = 0
    
    #초기화
    if upbit.get_balance(bitcoin) == 0:
        delay_buy_time = int(time.time())
        buy_count = 0 

    #변수 설정
    my_account = upbit.get_balance("KRW")
    now_price = upbit.get_balance(bitcoin)*pyupbit.get_current_price(bitcoin)
    rsi = SecondaryIndicator.EMA_RSI(bitcoin,bong=bong).tail()
    befer_rsi = round(rsi.iloc[-3].values[0], 2)
    now_rsi = round(rsi.iloc[-2].values[0], 2)
    rsi_delta = round((rsi.iloc[-2] - rsi.iloc[-3]).values[0], 2)

    #매수 시점
    if now_rsi <= buy_rsi:
        if rsi_delta >= 0: 
            if delay_buy_time <= int(time.time()) and buy_count < max_buy_count and my_account > buy_price * 1.005:

                print("매수채결", bong,time.strftime('%H:%M:%S',time.localtime()) + ' '+ bitcoin + ' ' +'RSI: ' + str(now_rsi)+ ' delta: ' + str(rsi_delta)+ ' ' +str(now_price))

                upbit.buy_market_order(bitcoin, buy_price)
                
                delay_buy_time = int(time.time()) + delay_time*60
                buy_count += 1

    if avg_buy_price*volum != 0:
        if now_rsi >= sell_rsi or befer_rsi >= sell_rsi :
            if rsi_delta < 0:
                #매도 시점1
                if buy_count < max_buy_count and avg_buy_price*volum < now_price :
                    upbit.sell_market_order(bitcoin, upbit.get_balance(bitcoin))

                    buy_count = 0

                    print("매도 1 채결",bong,time.strftime('%H:%M:%S',time.localtime()) + ' '+ bitcoin + ' ' +'RSI: ' + str(now_rsi)+ ' delta: ' + str(rsi_delta) + ' ' +str(now_price))        #매도 시점2 
            elif buy_count == max_buy_count and  (avg_buy_price*volum)*1.001 < now_price:
                upbit.sell_market_order(bitcoin, upbit.get_balance(bitcoin))

                buy_count = 0

                print("매도 2 채결",bong,time.strftime('%H:%M:%S',time.localtime()) + ' '+ bitcoin + ' ' +'RSI: ' + str(now_rsi) + ' delta: ' + str(rsi_delta)+ ' ' +str(now_price))

    #print(bitcoin , time.strftime('%H:%M:%S',time.localtime()) ,bong, 'RSI: ' , str(now_rsi) , ' delta: ' , str(rsi_delta), str(now_price), delay_buy_time, buy_count)
    
    time.sleep(0.5)
    return delay_buy_time, buy_count