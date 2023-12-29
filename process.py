import pyupbit
import time
import Strategy

class sell_buy_process():
    def first_room(app):
        while True:
            if len(app.restore_coin_list) != 0 : 
                if app.first_room_is_auto == 0:
                    app.first_room_label.config(bg='green')
                    if int(time.strftime('%M', time.localtime())) % int(app.first_room_bong_close_combobox.get()[6:]) == 0: 
                        app.first_room_rsi_close_entry.config(state='readonly')
                        for coin in app.restore_coin_list:
                            app.first_room_bitcoin_dict[coin]['delay_buy_time'], app.first_room_bitcoin_dict[coin]['buy_count'] = Strategy.strategy_sell_RSI_and_EMA(
                                app.upbit,
                                coin,
                                app.first_room_bitcoin_dict[coin]['delay_buy_time'],
                                app.first_room_bong_close_combobox.get(),
                                int(app.first_room_rsi_close_entry.get()),
                                app.first_room_bitcoin_dict[coin]['buy_count'],
                                app.debug_panel
                            )
                    if int(time.strftime('%M', time.localtime())) % int(app.first_room_bong_entry_combobox.get()[6:]) == 0:
                        app.first_room_price_entry.config(state='readonly')
                        app.first_room_count_entry.config(state='readonly')
                        app.first_room_rsi_entry_entry.config(state='readonly')
                        for coin in app.restore_coin_list:
                            app.first_room_bitcoin_dict[coin]['delay_buy_time'], app.first_room_bitcoin_dict[coin]['buy_count'] = Strategy.strategy_buy_RSI_and_EMA(
                                app.upbit,
                                coin,
                                app.first_room_bitcoin_dict[coin]['delay_buy_time'],
                                app.first_room_bong_entry_combobox.get(),
                                int(app.first_room_rsi_entry_entry.get()),
                                app.first_room_bitcoin_dict[coin]['buy_count'],
                                int(app.first_room_price_entry.get()),
                                int(app.first_room_count_entry.get()),
                                int(app.first_room_count_time_combobox.get()),
                                app.debug_panel
                        )
                    
                else:
                    app.first_room_price_entry.config(state='normal')
                    app.first_room_count_entry.config(state='normal')
                    app.first_room_rsi_entry_entry.config(state='normal')
                    app.first_room_rsi_close_entry.config(state='normal')
                    app.first_room_label.config(bg='yellow')
                    
            else:
                app.first_room_label.config(bg='red')
            
            time.sleep(1)

    def second_room(app):
        while True:
            if len(app.restore_coin_list) != 0 : 
                if app.second_room_is_auto == 0:
                    app.second_room_label.config(bg='green')
                    if int(time.strftime('%M', time.localtime())) % int(app.second_room_bong_close_combobox.get()[6:]) == 0: 
                        app.second_room_rsi_close_entry.config(state='readonly')
                        for coin in app.restore_coin_list:
                            app.second_room_bitcoin_dict[coin]['delay_buy_time'], app.second_room_bitcoin_dict[coin]['buy_count'] = Strategy.strategy_sell_RSI_and_EMA(
                                app.upbit,
                                coin,
                                app.second_room_bitcoin_dict[coin]['delay_buy_time'],
                                app.second_room_bong_close_combobox.get(),
                                int(app.second_room_rsi_close_entry.get()),
                                app.second_room_bitcoin_dict[coin]['buy_count'],
                                app.debug_panel
                            )
                    if int(time.strftime('%M', time.localtime())) % int(app.second_room_bong_entry_combobox.get()[6:]) == 0:
                        app.second_room_price_entry.config(state='readonly')
                        app.second_room_count_entry.config(state='readonly')
                        app.second_room_rsi_entry_entry.config(state='readonly')
                        for coin in app.restore_coin_list:
                            app.second_room_bitcoin_dict[coin]['delay_buy_time'], app.second_room_bitcoin_dict[coin]['buy_count'] = Strategy.strategy_buy_RSI_and_EMA(
                                app.upbit,
                                coin,
                                app.second_room_bitcoin_dict[coin]['delay_buy_time'],
                                app.second_room_bong_entry_combobox.get(),
                                int(app.second_room_rsi_entry_entry.get()),
                                app.second_room_bitcoin_dict[coin]['buy_count'],
                                int(app.second_room_price_entry.get()),
                                int(app.second_room_count_entry.get()),
                                int(app.second_room_count_time_combobox.get()),
                                app.debug_panel
                        )
                    
                else:
                    app.second_room_price_entry.config(state='normal')
                    app.second_room_count_entry.config(state='normal')
                    app.second_room_rsi_entry_entry.config(state='normal')
                    app.second_room_rsi_close_entry.config(state='normal')
                    app.second_room_label.config(bg='yellow')
                    
            else:
                app.second_room_label.config(bg='red')
            
            time.sleep(1)

    def third_room(app):
        while True:
            if len(app.restore_coin_list) != 0 : 
                if app.third_room_is_auto == 0:
                    app.third_room_label.config(bg='green')
                    if int(time.strftime('%M', time.localtime())) % int(app.third_room_bong_close_combobox.get()[6:]) == 0: 
                        app.third_room_rsi_close_entry.config(state='readonly')
                        for coin in app.restore_coin_list:
                            app.third_room_bitcoin_dict[coin]['delay_buy_time'], app.third_room_bitcoin_dict[coin]['buy_count'] = Strategy.strategy_sell_RSI_and_EMA(
                                app.upbit,
                                coin,
                                app.third_room_bitcoin_dict[coin]['delay_buy_time'],
                                app.third_room_bong_close_combobox.get(),
                                int(app.third_room_rsi_close_entry.get()),
                                app.third_room_bitcoin_dict[coin]['buy_count'],
                                app.debug_panel
                            )
                    if int(time.strftime('%M', time.localtime())) % int(app.third_room_bong_entry_combobox.get()[6:]) == 0:
                        app.third_room_price_entry.config(state='readonly')
                        app.third_room_count_entry.config(state='readonly')
                        app.third_room_rsi_entry_entry.config(state='readonly')
                        for coin in app.restore_coin_list:
                            app.third_room_bitcoin_dict[coin]['delay_buy_time'], app.third_room_bitcoin_dict[coin]['buy_count'] = Strategy.strategy_buy_RSI_and_EMA(
                                app.upbit,
                                coin,
                                app.third_room_bitcoin_dict[coin]['delay_buy_time'],
                                app.third_room_bong_entry_combobox.get(),
                                int(app.third_room_rsi_entry_entry.get()),
                                app.third_room_bitcoin_dict[coin]['buy_count'],
                                int(app.third_room_price_entry.get()),
                                int(app.third_room_count_entry.get()),
                                int(app.third_room_count_time_combobox.get()),
                                app.debug_panel
                        )
                    
                else:
                    app.third_room_price_entry.config(state='normal')
                    app.third_room_count_entry.config(state='normal')
                    app.third_room_rsi_entry_entry.config(state='normal')
                    app.third_room_rsi_close_entry.config(state='normal')
                    app.third_room_label.config(bg='yellow')
                    
            else:
                app.third_room_label.config(bg='red')
            
            time.sleep(1)
    
    def fourth_room(app):
        while True:
            if len(app.restore_coin_list) != 0 : 
                if app.fourth_room_is_auto == 0:
                    app.fourth_room_label.config(bg='green')
                    if int(time.strftime('%M', time.localtime())) % int(app.fourth_room_bong_close_combobox.get()[6:]) == 0: 
                        app.fourth_room_rsi_close_entry.config(state='readonly')
                        for coin in app.restore_coin_list:
                            app.fourth_room_bitcoin_dict[coin]['delay_buy_time'], app.fourth_room_bitcoin_dict[coin]['buy_count'] = Strategy.strategy_sell_RSI_and_EMA(
                                app.upbit,
                                coin,
                                app.fourth_room_bitcoin_dict[coin]['delay_buy_time'],
                                app.fourth_room_bong_close_combobox.get(),
                                int(app.fourth_room_rsi_close_entry.get()),
                                app.fourth_room_bitcoin_dict[coin]['buy_count'],
                                app.debug_panel
                            )
                    if int(time.strftime('%M', time.localtime())) % int(app.fourth_room_bong_entry_combobox.get()[6:]) == 0:
                        app.fourth_room_price_entry.config(state='readonly')
                        app.fourth_room_count_entry.config(state='readonly')
                        app.fourth_room_rsi_entry_entry.config(state='readonly')
                        for coin in app.restore_coin_list:
                            app.fourth_room_bitcoin_dict[coin]['delay_buy_time'], app.fourth_room_bitcoin_dict[coin]['buy_count'] = Strategy.strategy_buy_RSI_and_EMA(
                                app.upbit,
                                coin,
                                app.fourth_room_bitcoin_dict[coin]['delay_buy_time'],
                                app.fourth_room_bong_entry_combobox.get(),
                                int(app.fourth_room_rsi_entry_entry.get()),
                                app.fourth_room_bitcoin_dict[coin]['buy_count'],
                                int(app.fourth_room_price_entry.get()),
                                int(app.fourth_room_count_entry.get()),
                                int(app.fourth_room_count_time_combobox.get()),
                                app.debug_panel
                        )
                    
                else:
                    app.fourth_room_price_entry.config(state='normal')
                    app.fourth_room_count_entry.config(state='normal')
                    app.fourth_room_rsi_entry_entry.config(state='normal')
                    app.fourth_room_rsi_close_entry.config(state='normal')
                    app.fourth_room_label.config(bg='yellow')
                    
            else:
                app.fourth_room_label.config(bg='red')
            
            time.sleep(1)
    
    def special_room(app):
        while True:
            if len(app.restore_coin_list) != 0 : 
                if app.special_room_is_auto == 0:
                    app.special_room_label.config(bg='green')
                    if int(time.strftime('%M', time.localtime())) % int(app.special_room_bong_close_combobox.get()[6:]) == 0: 
                        app.special_room_rsi_close_entry.config(state='readonly')
                        app.special_room_delay_time, app.special_room_count = Strategy.strategy_sell_RSI_and_EMA(
                            app.upbit,
                            "KRW-SBD",
                            app.special_room_delay_time,
                            app.special_room_bong_close_combobox.get(),
                            int(app.special_room_rsi_close_entry.get()),
                            app.special_room_count,
                            app.debug_panel
                            )
                    if int(time.strftime('%M', time.localtime())) % int(app.special_room_bong_entry_combobox.get()[6:]) == 0:
                        app.special_room_price_entry.config(state='readonly')
                        app.special_room_rsi_entry_entry.config(state='readonly')
                        app.special_room_delay_time, app.special_room_count = Strategy.strategy_buy_RSI_and_EMA(
                            app.upbit,
                            "KRW-SBD",
                            app.special_room_delay_time,
                            app.special_room_bong_entry_combobox.get(),
                            int(app.special_room_rsi_entry_entry.get()),
                            app.special_room_count,
                            int(app.special_room_price_entry.get()),
                            app.special_room_count_entry,
                            app.special_room_count_time_list[app.special_room_count],
                            app.debug_panel
                        )
                    
                else:
                    app.special_room_price_entry.config(state='normal')
                    app.special_room_rsi_entry_entry.config(state='normal')
                    app.special_room_label.config(state='normal')
                    app.special_room_label.config(bg='yellow')
                    
            else:
                app.special_room_label.config(bg='red')
            
            time.sleep(1)

def checking_bitcoin(app):
        while True:
            if time.strftime('%M',time.localtime()) == "00" :
                if len(app.except_bitcoin) != 0:
                    count = 0
                    while len(app.except_bitcoin) != count:
                        date = time.strftime("%Y%m%d",time.localtime())

                        #어제 값 
                        close = pyupbit.get_ohlcv(app.except_bitcoin[count], interval="day",to=date)[['close']].tail(1)

                        #오늘 값
                        today = pyupbit.get_ohlcv(app.except_bitcoin[count], interval="day")[['close']].tail(1)
                        delta = round((today.iloc[0,0] - close.iloc[0,0]) / close.iloc[0,0] * 100, 3)
                        if delta < -10:
                            app.bitcoinlist.append(app.except_bitcoin.pop(count))
                            app.except_coin_delay_tiem_list.pop(count)
                        elif app.except_coin_delay_tiem_list[count] <= int(date) :
                            app.bitcoinlist.append(app.except_bitcoin.pop(count))
                            app.except_coin_delay_tiem_list.pop(count)

                        else: count += 1 
                
                if  len(app.bitcoinlist) != 0 :
                    count = 0
                    while len(app.bitcoinlist) != count:
                        date = time.strftime("%Y%m%d",time.localtime())

                        #어제 값 
                        close = pyupbit.get_ohlcv(app.bitcoinlist[count], interval="day",to=date)[['close']].tail(1)

                        #오늘 값
                        today = pyupbit.get_ohlcv(app.bitcoinlist[count], interval="day")[['high']].tail(1)
                        delta = round((today.iloc[0,0] - close.iloc[0,0]) / close.iloc[0,0] * 100, 3)
                        if delta > 10 :
                            app.upbit.sell_market_order(app.bitcoinlist, app.upbit.get_balance(app.bitcoinlist))
                            app.except_bitcoin.append(app.bitcoinlist.pop(count))

                            app.except_coin_delay_tiem_list.append(int(date) + 2)
                        
                        else: count += 1
            time.sleep(30)

