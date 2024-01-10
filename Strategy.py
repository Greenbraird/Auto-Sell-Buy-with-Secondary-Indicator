import SecondaryIndicator
import pyupbit
import time
import tkinter as tk

"""
---------------------------------------------------------------------------
---------------------------- 매수 함수 -------------------------------------
---------------------------------------------------------------------------
"""
def strategy_buy_RSI_and_EMA(upbit,bitcoin,delay_buy_time,entry_bong,entry_rsi,buy_count,buy_price,max_buy_count,delay_time,log_panel):
    
    #초기화
    if upbit.get_balance(bitcoin) == 0:
        delay_buy_time = int(time.time())
        buy_count = 0
    
    else:
        buy_count = max_buy_count

    #기본 변수 설정
    can_buy = upbit.get_balance("KRW") > buy_price * 1.0005
    is_buy_now = delay_buy_time <= int(time.time())
    
    #상승장이면 True 아니면 False
    buy_is_bull_market = None   
    
    #RSI 변수 설정
    buy_rsi = SecondaryIndicator.EMA_RSI(bitcoin,bong=entry_bong).tail()
    buy_befer_rsi = round(buy_rsi.iloc[-3].values[0], 2)
    buy_now_rsi = round(buy_rsi.iloc[-2].values[0], 2)
    buy_rsi_delta = buy_now_rsi - buy_befer_rsi

    #SMA 변수 설정
    buy_sma = SecondaryIndicator.SMA(bitcoin,bong=entry_bong)
    buy_delat1030 = round(buy_sma.iloc[1,1] - buy_sma.iloc[1,2],3)
    #before_delat1030 = round(sma.iloc[0,1] - sma.iloc[0,2],3)
    buy_delat30100 = round(buy_sma.iloc[1,2] - buy_sma.iloc[1,3],3)
    #before_delat30100 = round(sma.iloc[0,2] - sma.iloc[0,3],3)

    if buy_delat1030 > 0 and buy_delat30100 > 0: buy_is_bull_market = True
    #음 값이면 하락장으로 판단
    elif buy_delat1030 < 0 and  buy_delat30100 < 0: buy_is_bull_market = False
    #이 이외의 경우의 수 즉, delat1030과 delat30100이 다른 부호를 가질 경우 장의 장의 흐름이 결정되지 않았다는 뜻
    else: buy_is_bull_market = None

    #------------------매수 조건문------------------
    if buy_is_bull_market:
        pass
    elif buy_is_bull_market == False:
        if is_buy_now and buy_count<max_buy_count and can_buy and buy_now_rsi<entry_rsi and buy_rsi_delta>0:
            upbit.buy_market_order(bitcoin,buy_price)
            delay_buy_time = int(time.time()) + delay_time*60
            buy_count += 1
            buy_log = time.strftime('%H:%M:%S',time.localtime()) + ' ' + bitcoin +' ' + entry_bong +' ' + 'RSI:'+ ' ' + str(buy_now_rsi) + ' ' +'매수 횟수:'+ ' ' + str(buy_count)+ ' ' + '매수되었습니다.\n'
            log_panel.insert(tk.END,buy_log)
    
    print(time.strftime('%H:%M:%S',time.localtime()),'매수', bitcoin, entry_bong)
    return delay_buy_time, buy_count

"""
---------------------------------------------------------------------------
---------------------------- 매도 함수 -------------------------------------
---------------------------------------------------------------------------
"""
def strategy_sell_RSI_and_EMA(upbit,bitcoin,delay_buy_time,close_bong,close_rsi,buy_count,log_panel):
    
    #초기 셋팅
    my_balances = upbit.get_balances()
    avg_buy_price = 0
    volum = 0
    
    for i in my_balances:

        if i['currency'] == bitcoin[4:]:
            avg_buy_price = float(i['avg_buy_price'])
            volum = float(i['balance'])
    
   
    # 산게 있을때만
    if buy_count != 0:

        #------------------변수 설정------------------
        is_benefit = (avg_buy_price*volum)*1.003 < upbit.get_balance(bitcoin)*pyupbit.get_current_price(bitcoin)
        #is_big_benefit = (avg_buy_price*volum)*1.01 < upbit.get_balance(bitcoin)*pyupbit.get_current_price(bitcoin)
        stop_loss = (avg_buy_price*volum)*0.99 > upbit.get_balance(bitcoin)*pyupbit.get_current_price(bitcoin)
    
        #상승장이면 True 아니면 False
        sell_is_bull_market = None

        #RSI 변수 설정
        sell_rsi = SecondaryIndicator.EMA_RSI(bitcoin,bong=close_bong).tail()
        sell_befer_rsi = round(sell_rsi.iloc[-3].values[0], 2)
        sell_now_rsi = round(sell_rsi.iloc[-2].values[0], 2)
        sell_rsi_delta = sell_now_rsi - sell_befer_rsi

        #SMA 변수 설정
        sell_sma = SecondaryIndicator.SMA(bitcoin,bong=close_bong)
        sell_delat1030 = round(sell_sma.iloc[1,1] - sell_sma.iloc[1,2],3)
        before_delat1030 = round(sell_sma.iloc[0,1] - sell_sma.iloc[0,2],3)
        sell_delat30100 = round(sell_sma.iloc[1,2] - sell_sma.iloc[1,3],3)
        #before_delat30100 = round(sma.iloc[0,2] - sma.iloc[0,3],3)
        sell_delat100 = round(sell_sma.iloc[1,3] - sell_sma.iloc[0,3])

        if sell_delat1030 > 0 and sell_delat30100 > 0: sell_is_bull_market = True
        #음 값이면 하락장으로 판단
        elif sell_delat1030 < 0 and  sell_delat30100 < 0: sell_is_bull_market = False
        #이 이외의 경우의 수 즉, delat1030과 delat30100이 다른 부호를 가질 경우 장의 장의 흐름이 결정되지 않았다는 뜻
        else: sell_is_bull_market = None
        #상승장이라고 판단되었을 때 == 정배열

         
        #------------------매도 조건문------------------
        if sell_is_bull_market:
            #close_rsi값 crossover시 25% 판매
            if sell_now_rsi > close_rsi and sell_befer_rsi< close_rsi and is_benefit and upbit.get_balance(bitcoin)*pyupbit.get_current_price(bitcoin) > 10000:
                upbit.sell_market_order(bitcoin,upbit.get_balance(bitcoin)/4)
                sell_log = time.strftime('%H:%M:%S',time.localtime())+' '+ bitcoin+ ' ' +close_bong +' '+ 'RSI' +' '+ str(close_rsi) +' '+ '상승장에서 25% 판매되었습니다.\n'
                log_panel.insert(tk.END,sell_log)
            #close_rsi + 3 값 crossover시 33% 판매    
            elif sell_now_rsi > close_rsi + 3 and sell_befer_rsi< close_rsi + 3 and is_benefit and upbit.get_balance(bitcoin)*pyupbit.get_current_price(bitcoin) > 10000:
                upbit.sell_market_order(bitcoin,upbit.get_balance(bitcoin)/3)
                sell_log = time.strftime('%H:%M:%S',time.localtime())+' '+ bitcoin+' ' +close_bong +' '+ 'RSI' +' '+ str(close_rsi+3) +' '+ '상승장에서 33% 판매되었습니다.\n'
                log_panel.insert(tk.END,sell_log)

        elif sell_is_bull_market == False:
            pass
        
        #결정되지 않은 장
        elif sell_is_bull_market == None:
            if sell_now_rsi > close_rsi and is_benefit and upbit.get_balance(bitcoin)*pyupbit.get_current_price(bitcoin) > 10000:
                upbit.sell_market_order(bitcoin,upbit.get_balance(bitcoin)/2)
                sell_log = time.strftime('%H:%M:%S',time.localtime())+' '+ bitcoin+' ' +close_bong +' '+ 'RSI' +' '+ str(close_rsi) +' '+ '추세가 결정되지 않은 장에서 50% 판매되었습니다.\n'
                log_panel.insert(tk.END,sell_log)

        if sell_delat100 < 0 and is_benefit and upbit.get_balance(bitcoin)*pyupbit.get_current_price(bitcoin) > 10000:
            upbit.sell_market_order(bitcoin,upbit.get_balance(bitcoin)/4)
            sell_log = time.strftime('%H:%M:%S',time.localtime())+' '+ bitcoin+' ' +close_bong +' '+ '하락장에서 반등하여 25% 판매되었습니다.\n'
            log_panel.insert(tk.END,sell_log)

        #완전 매도 밎 초기화 진행
        if sell_delat1030 < 0 and before_delat1030 > 0 : 
            upbit.sell_market_order(bitcoin, upbit.get_balance(bitcoin))
            buy_count = 0;delay_buy_time = 0
            sell_log = time.strftime('%H:%M:%S',time.localtime())+' '+ bitcoin+' ' +close_bong +' '+ 'SMA10과 SMA30 crossunder 판매되었습니다.\n'
            log_panel.insert(tk.END,sell_log)

        #스탑로스 후 초기화 진행
        '''
        if stop_loss:
            upbit.sell_market_order(bitcoin, upbit.get_balance(bitcoin))
            buy_count = 0;delay_buy_time = 0
            sell_log = time.strftime('%H:%M:%S',time.localtime())+' '+ bitcoin+' ' +close_bong +' '+ '-1% 손절 판매되었습니다.\n'
            log_panel.insert(tk.END,sell_log)
        '''

    print(time.strftime('%H:%M:%S',time.localtime()),'매도', bitcoin, close_bong)

    return  delay_buy_time, buy_count