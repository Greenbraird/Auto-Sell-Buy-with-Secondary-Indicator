import pyupbit
import tkinter as tk
import tkinter.ttk as ttk
import threading
import Strategy
import time


class App:
    def __init__(self, root):
        self.root = root
        self.creat_title_frame()
        self.creat_debuging_panel()
        self.creat_head_frame()
        self.checkboxes = {}
        self.restore_coin_list = []
        self.bitcoinlist = ['KRW-BTC', 'KRW-ETH', 'KRW-NEO', 'KRW-MTL', 'KRW-XRP', 'KRW-ETC', 'KRW-T', 'KRW-AVAX', 'KRW-XEM', 'KRW-STRAX', 
                            'KRW-LSK', 'KRW-SXP', 'KRW-FCT2', 'KRW-ARDR', 'KRW-ARK', 'KRW-STORJ', 'KRW-GRS', 'KRW-ADA', 'KRW-SBD', 'KRW-POWR',
                            'KRW-BTG', 'KRW-HIVE', 'KRW-HPO', 'KRW-AHT', 'KRW-SC', 'KRW-DOGE', 'KRW-STPT', 'KRW-EGLD', 'KRW-ZRX', 'KRW-META', 
                            'KRW-BCH', 'KRW-SOL', 'KRW-AERGO', 'KRW-CVC', 'KRW-IMX', 'KRW-IOTA', 'KRW-HIFI', 'KRW-ONG', 'KRW-GAS', 'KRW-UPP', 
                            'KRW-ELF', 'KRW-KNC', 'KRW-AXS', 'KRW-TT', 'KRW-QKC', 'KRW-BTT', 'KRW-MOC', 'KRW-TFUEL', 'KRW-SAND', 'KRW-ANKR']
        self.except_bitcoin = []
        self.first_room_bitcoin_dict = {}
        self.second_room_bitcoin_dict = {}
        self.third_room_bitcoin_dict = {}
        self.fourth_room_bitcoin_dict = {}

        self.except_coin_delay_tiem_list =[]

        for i in self.bitcoinlist:
            self.first_room_bitcoin_dict[i] = {'delay_buy_time': 0 , 'buy_count':0}
            self.second_room_bitcoin_dict[i] = {'delay_buy_time': 0 , 'buy_count':0}
            self.third_room_bitcoin_dict[i] = {'delay_buy_time': 0 , 'buy_count':0}
            self.fourth_room_bitcoin_dict[i] = {'delay_buy_time': 0 , 'buy_count':0}

        self.open_new_window()

        #백그라운드 스레드 생성
        self.background_thread = threading.Thread(target=self.buy_start_strategy)
        self.background_thread.daemon = True  # 메인 스레드가 종료되면 백그라운드 스레드도 종료되도록 설정

        self.background_thread2 = threading.Thread(target=self.sell_start_strategy)
        self.background_thread2.daemon = True  # 메인 스레드가 종료되면 백그라운드 스레드도 종료되도록 설정
        

        self.background_thread3 = threading.Thread(target=self.checking_bitcoin)
        self.background_thread3.daemon = True

        self.root.mainloop()

    def checking_bitcoin(self):
        while True:
            
            if time.strftime('%M',time.localtime()) == "00" :
                if len(self.except_bitcoin) != 0:
                    count = 0
                    while len(self.except_bitcoin) != count:
                        date = time.strftime("%Y%m%d",time.localtime())

                        #어제 값 
                        close = pyupbit.get_ohlcv(self.except_bitcoin[count], interval="day",to=date)[['close']].tail(1)

                        #오늘 값
                        today = pyupbit.get_ohlcv(self.except_bitcoin[count], interval="day")[['close']].tail(1)
                        delta = round((today.iloc[0,0] - close.iloc[0,0]) / close.iloc[0,0] * 100, 3)
                        if delta < -10:
                            self.bitcoinlist.append(self.except_bitcoin.pop(count))
                            self.except_coin_delay_tiem_list.pop(count)
                        elif self.except_coin_delay_tiem_list[count] <= int(date) :
                            self.bitcoinlist.append(self.except_bitcoin.pop(count))
                            self.except_coin_delay_tiem_list.pop(count)

                        else: count += 1 
                
                if  len(self.bitcoinlist) != 0 :
                    count = 0
                    while len(self.bitcoinlist) != count:
                        date = time.strftime("%Y%m%d",time.localtime())

                        #어제 값 
                        close = pyupbit.get_ohlcv(self.bitcoinlist[count], interval="day",to=date)[['close']].tail(1)

                        #오늘 값
                        today = pyupbit.get_ohlcv(self.bitcoinlist[count], interval="day")[['high']].tail(1)
                        delta = round((today.iloc[0,0] - close.iloc[0,0]) / close.iloc[0,0] * 100, 3)
                        if delta > 10 :
                            log = self.bitcoinlist.pop(count) + "가 " + "장 상승으로 인하여 잠시 거래 중지합니다.\n"
                            self.debug_panel.insert(tk.END,log)
                            self.upbit.sell_market_order(self.bitcoinlist, self.upbit.get_balance(self.bitcoinlist))
                            self.except_bitcoin.append(self.bitcoinlist.pop(count))

                            self.except_coin_delay_tiem_list.append(int(date) + 2)
                        
                        else: count += 1
            time.sleep(30)

    def buy_process_room(self, room_label, is_auto, bong_entry_combobox, price_entry, count_entry, rsi_entry_entry, count_time,bitcoin_dict,log_panel):
        if len(self.restore_coin_list) != 0:
            if is_auto == 0:
                room_label.config(bg='green')
                if int(time.strftime('%M', time.localtime())) % int(bong_entry_combobox.get()[6:]) == 0 or bong_entry_combobox.get()[6:] == '60': #60이런 것 들은 처리를 못함
                    price_entry.config(state='readonly')
                    count_entry.config(state='readonly')
                    rsi_entry_entry.config(state='readonly')
                    for coin in self.restore_coin_list:
                        bitcoin_dict[coin]['delay_buy_time'], bitcoin_dict[coin]['buy_count'] = Strategy.strategy_buy_RSI_and_EMA(
                            self.upbit,
                            coin,
                            bitcoin_dict[coin]['delay_buy_time'],
                            bong_entry_combobox.get(),
                            int(rsi_entry_entry.get()),
                            bitcoin_dict[coin]['buy_count'],
                            int(price_entry.get()),
                            int(count_entry.get()),
                            int(count_time.get()),
                            log_panel,
                    )
            else:
                price_entry.config(state='normal')
                count_entry.config(state='normal')
                rsi_entry_entry.config(state='normal')
                room_label.config(bg='yellow')
        else:
            room_label.config(bg='red')

    def buy_start_strategy(self):
        while True:
            if self.special_room_is_auto == 0:
                self.special_room_label.configure(bg='green')
                if int(time.strftime('%M', time.localtime())) % int(self.special_room_bong_entry_combobox.get()[6:]) == 0:
                    self.special_room_rsi_entry_entry.config(state='readonly')
                    self.special_room_price_entry.config(state='readonly')

                    self.special_room_delay_time, self.special_room_count = Strategy.strategy_buy_RSI_and_EMA (
                        self.upbit,
                        "KRW-SBD",
                        self.special_room_delay_time,
                        self.special_room_bong_entry_combobox.get(),
                        int(self.special_room_rsi_entry_entry.get()),
                        self.special_room_count,
                        int(self.special_room_price_entry.get())/4,
                        self.special_room_count_entry,
                        self.special_room_count_time_list[self.special_room_count],
                        self.debug_panel
                    )
            else:
                self.special_room_rsi_close_entry.config(state='normal')
                self.special_room_label.configure(bg='yellow')

            self.buy_process_room(self.fourth_room_label, self.fourth_room_is_auto, self.fourth_room_bong_entry_combobox,
                               self.fourth_room_price_entry, self.fourth_room_count_entry,self.fourth_room_rsi_entry_entry,
                                self.fourth_room_count_time_combobox, self.fourth_room_bitcoin_dict,self.debug_panel)
            
            self.buy_process_room(self.second_room_label, self.second_room_is_auto, self.second_room_bong_entry_combobox,
                               self.second_room_price_entry, self.second_room_count_entry, self.second_room_rsi_entry_entry,
                                self.second_room_count_time_combobox, self.second_room_bitcoin_dict,self.debug_panel)


            self.buy_process_room(self.third_room_label, self.third_room_is_auto, self.third_room_bong_entry_combobox,
                               self.third_room_price_entry, self.third_room_count_entry, self.third_room_rsi_entry_entry,
                                self.third_room_count_time_combobox, self.third_room_bitcoin_dict,self.debug_panel)
            
            self.buy_process_room(self.first_room_label, self.first_room_is_auto, self.first_room_bong_entry_combobox,
                                self.first_room_price_entry, self.first_room_count_entry, self.first_room_rsi_entry_entry,
                                self.first_room_count_time_combobox, self.first_room_bitcoin_dict,self.debug_panel)
            
            time.sleep(1)

    def sell_process_room(self,room_label,is_auto,bong_close_combobox,rsi_close_entry,bitcoin_dict,log_panel):
         if len(self.restore_coin_list) != 0:
            if is_auto == 0:
                room_label.config(bg='green')
                if int(time.strftime('%M', time.localtime())) % int(bong_close_combobox.get()[6:]) == 0 or bong_close_combobox.get()[6:] == '60': 
                    rsi_close_entry.config(state='readonly')
                    for coin in self.restore_coin_list:
                        bitcoin_dict[coin]['delay_buy_time'], bitcoin_dict[coin]['buy_count'] = Strategy.strategy_sell_RSI_and_EMA(
                            self.upbit,
                            coin,
                            bitcoin_dict[coin]['delay_buy_time'],
                            bong_close_combobox.get(),
                            int(rsi_close_entry.get()),
                            bitcoin_dict[coin]['buy_count'],
                            log_panel
                    )
            else:
                rsi_close_entry.config(state='normal')
                room_label.config(bg='yellow')
    
    def sell_start_strategy(self):
        while True:
            self.sell_process_room(self.first_room_label, self.first_room_is_auto, self.first_room_bong_close_combobox,
                                self.first_room_rsi_close_entry, self.first_room_bitcoin_dict,self.debug_panel)

            self.sell_process_room(self.second_room_label, self.second_room_is_auto, self.second_room_bong_close_combobox,
                                self.second_room_rsi_close_entry, self.second_room_bitcoin_dict,self.debug_panel)

            self.sell_process_room(self.third_room_label, self.third_room_is_auto, self.third_room_bong_close_combobox,
                                self.third_room_rsi_close_entry, self.third_room_bitcoin_dict,self.debug_panel)

            self.sell_process_room(self.fourth_room_label, self.fourth_room_is_auto, self.fourth_room_bong_close_combobox,
                                self.fourth_room_rsi_close_entry, self.fourth_room_bitcoin_dict,self.debug_panel)
            
            if self.special_room_is_auto == 0:
                self.special_room_label.configure(bg='green')
                if int(time.strftime('%M', time.localtime())) % int(self.special_room_bong_close_combobox.get()[6:]) == 0:
                    self.special_room_rsi_close_entry.config(state='readonly')
                    self.special_room_delay_time, self.special_room_count = Strategy.strategy_sell_RSI_and_EMA (
                        self.upbit,
                        "KRW-SBD",
                        self.special_room_delay_time,
                        self.special_room_bong_close_combobox.get(),
                        int(self.special_room_rsi_close_entry.get()),
                        self.special_room_count,
                        self.debug_panel
                    )
            else:
                self.special_room_rsi_close_entry.config(state='normal')
                self.special_room_label.configure(bg='yellow')

            time.sleep(1)

    #restore coin list가 실질적으로 돌아가는 코인들을 모아둔 list임
    def get_checked_boxes(self):
        
        self.restore_coin_list = []
        for box in self.checkboxes:
                if box.var.get() == 1:
                        self.restore_coin_list.append(self.checkboxes[box])
        
        self.new_window.destroy()
        log = str(self.restore_coin_list) + " 총 " + str(len(self.restore_coin_list)) + "개를 선택하셨습니다.\n"
        self.debug_panel.insert(tk.END,log)
        
        print(self.restore_coin_list)    # debug

    def open_new_window(self):
        self.new_window = tk.Toplevel(self.root)
        self.new_window.title('coin창')
    
        Cbcolumn = 0
        Cbrow = 8
        Chkcount = 0
        self.checkboxes = {}
        for Checkbox in range(len(self.bitcoinlist)):
                name = self.bitcoinlist[Checkbox]
                current_var = tk.IntVar()
                current_box = tk.Checkbutton(self.new_window, text=name, variable=current_var)
                current_box.var = current_var
                current_box.grid(row=Cbrow, column=Cbcolumn)
                
                self.checkboxes[current_box] = name 
                if Cbcolumn == 4:
                        Cbcolumn = 0
                        Cbrow += 1
                else:
                        Cbcolumn += 1
                        Chkcount += 1

                if self.checkboxes[current_box] in self.restore_coin_list:
                     current_box.select()
        
        print_cbox_button = tk.Button(self.new_window, text='적용', command=self.get_checked_boxes)
        print_cbox_button.grid(row=20, column=0, columnspan=5)

    def login(self):
        self.upbit = pyupbit.Upbit(self.access_entry.get(), self.secret_entry.get())
        self.balance_label.config(text = self.upbit.get_balance("KRW"))
        
        log = time.strftime('%H:%M:%S',time.localtime()) + ' ' + '로그인이 완료 되었습니다.\n'
        self.debug_panel.insert(tk.END,log)
        self.creat_body_frame()

        self.background_thread.start()
        self.background_thread2.start()
        self.background_thread3.start()

    def creat_title_frame(self):

        titleF = tk.Frame(self.root, relief='solid', bd=2)
        titleF.pack(fill='x', padx=2, pady=2)
        
        p_name_label = tk.Label(titleF, text="Auto Upbit Sell Buy").pack(fill='x', padx=2, pady=2,side='left')
        coin_list_btn = tk.Button(titleF, text="Coin List", command=self.open_new_window).pack(fill='x', padx=2, pady=2,side='right')

    def creat_debuging_panel(self):
        
        debug_panelF = tk.Frame(self.root, relief='solid',bd=2)
        debug_panelF.pack(fill='x', padx=2,pady=2)

        debug_panel_scrollbar = tk.Scrollbar(debug_panelF)
        debug_panel_scrollbar.pack(side="right", fill="y")

        self.debug_panel = tk.Text(debug_panelF,height=15)
        self.debug_panel.pack(fill='x', padx=2,pady=2)

        debug_panel_scrollbar["command"] = self.debug_panel.yview
        
    
    def creat_head_frame(self):
        headF = tk.Frame(self.root, relief='solid', bd=2)
        headF.pack(fill="x", padx=2, pady=2)

        access_label = tk.Label(headF, text="access:")
        access_label.pack(fill='x', padx=2, pady=2, side="left")
        self.access_entry = tk.Entry(headF, width=25)
        self.access_entry.pack(fill='x', padx=2, pady=2, side="left")

        secret_label = tk.Label(headF, text="secret:")
        secret_label.pack(fill='x', padx=2, pady=2, side="left")
        self.secret_entry = tk.Entry(headF, width=25)
        self.secret_entry.pack(fill='x', padx=2, pady=2, side="left")

        self.balance_label = tk.Label(headF, text='0')
        self.balance_label.pack(fill='x', padx=2, pady=2, side="right")
        get_balance_btn = tk.Button(headF, text='로그인', command=self.login)
        get_balance_btn.pack(fill='x', padx=2, pady=2, side="right")


    def creat_body_frame(self):
        bodyF = tk.Frame(self.root, bd=2)
        bodyF.pack(fill='x', padx=2, pady=2)
        
        close_bong_combobox_valuse = ['minute3','minute5','minute10','minute15','minute30','minute60']
        #--------------------------------
        #----------first frame-----------
        #--------------------------------

        first_roomF = tk.Frame(bodyF, relief='solid', bd=2)
        first_roomF.pack(fill='x', padx=2, pady=2)

        self.first_room_label = tk.Label(first_roomF, text = "1번방",bg = 'red')
        self.first_room_label.pack(fill='x', padx=2, pady=2, side= 'left')


        first_room_bong_entry_lable = tk.Label(first_roomF, text = "매수 분봉").pack(fill='x', padx=2, pady=2, side='left')
        min_bong_combobox_values = ['minute1','minute3','minute5']
        self.first_room_bong_entry_combobox = ttk.Combobox(first_roomF,width=10,values=min_bong_combobox_values,state='readonly')
        self.first_room_bong_entry_combobox.pack(fill='x', padx=2, pady=2, side='left')
        self.first_room_bong_entry_combobox.current(1)

        first_room_bong_close_lable = tk.Label(first_roomF, text = "매도 분봉").pack(fill='x', padx=2, pady=2, side='left')
        self.first_room_bong_close_combobox = ttk.Combobox(first_roomF,width=10,values=close_bong_combobox_valuse,state='readonly')
        self.first_room_bong_close_combobox.pack(fill='x', padx=2, pady=2, side='left')
        self.first_room_bong_close_combobox.current(1)
        
        first_room_price_label = tk.Label(first_roomF, text = "매수 가격").pack(fill='x', padx=2, pady=2, side='left')
        self.first_room_price_entry = tk.Entry(first_roomF, width=7)
        self.first_room_price_entry.pack(fill='x', padx=2, pady=2, side='left')
        
        first_room_rsi_entry_label = tk.Label(first_roomF, text = "매수 RSI").pack(fill='x', padx=2, pady=2, side= 'left')
        self.first_room_rsi_entry_entry = tk.Entry(first_roomF, width=2)
        self.first_room_rsi_entry_entry.pack(fill='x', padx=2, pady=2 , side= 'left')

        first_room_rsi_close_label = tk.Label(first_roomF, text = "매도 RSI").pack(fill='x', padx=2, pady=2, side= 'left')
        self.first_room_rsi_close_entry = tk.Entry(first_roomF, width=2)
        self.first_room_rsi_close_entry.pack(fill='x', padx=2, pady=2 , side= 'left')

        first_room_count_label = tk.Label(first_roomF, text = "횟수").pack(fill='x', padx=2, pady=2, side= 'left')
        self.first_room_count_entry = tk.Entry(first_roomF, width=1)
        self.first_room_count_entry.pack(fill='x', padx=2, pady=2 , side= 'left')

        first_room_count_time_label = tk.Label(first_roomF, text='딜레이 시간').pack(fill='x', padx=2, pady=2, side= 'left')
        first_room_count_time_list = [40,50,60,70,80]
        self.first_room_count_time_combobox = ttk.Combobox(first_roomF, width=3,values=first_room_count_time_list,state='readonly')
        self.first_room_count_time_combobox.pack(fill='x', padx=2, pady=2, side='left')
        self.first_room_count_time_combobox.current(0)

        
        def first_room_check():
            self.first_room_is_auto = first_is_auto.get()

        first_is_auto = tk.IntVar()

        autobutton = tk.Radiobutton(first_roomF, text="시작", value=0, variable=first_is_auto, command=first_room_check)
        autobutton.pack(fill='x', padx=2, pady=2, side= 'left')

        nonautobutton = tk.Radiobutton(first_roomF, text="중지", value=1, variable=first_is_auto, command=first_room_check)
        nonautobutton.pack(fill='x', padx=2, pady=2, side= 'left')
        nonautobutton.invoke()


        #--------------------------------
        #----------second frame----------
        #--------------------------------
        second_roomF = tk.Frame(bodyF, relief='solid', bd=2)
        second_roomF.pack(fill='x', padx=2, pady=2)

        self.second_room_label = tk.Label(second_roomF, text = "2번방",bg = 'red')
        self.second_room_label.pack(fill='x', padx=2, pady=2, side= 'left')


        second_room_bong_entry_lable = tk.Label(second_roomF, text = "매수 분봉").pack(fill='x', padx=2, pady=2, side='left')
        min_bong_combobox_values = ['minute3','minute5','minute10','minute15']
        self.second_room_bong_entry_combobox = ttk.Combobox(second_roomF,width=10,values=min_bong_combobox_values,state='readonly')
        self.second_room_bong_entry_combobox.pack(fill='x', padx=2, pady=2, side='left')
        self.second_room_bong_entry_combobox.current(0)

        second_room_bong_close_lable = tk.Label(second_roomF, text = "매도 분봉").pack(fill='x', padx=2, pady=2, side='left')
        self.second_room_bong_close_combobox = ttk.Combobox(second_roomF,width=10,values=close_bong_combobox_valuse,state='readonly')
        self.second_room_bong_close_combobox.pack(fill='x', padx=2, pady=2, side='left')
        self.second_room_bong_close_combobox.current(1)
        
        second_room_price_label = tk.Label(second_roomF, text = "매수 가격").pack(fill='x', padx=2, pady=2, side='left')
        self.second_room_price_entry = tk.Entry(second_roomF, width=7)
        self.second_room_price_entry.pack(fill='x', padx=2, pady=2, side='left')
        
        second_room_rsi_entry_label = tk.Label(second_roomF, text = "매수 RSI").pack(fill='x', padx=2, pady=2, side= 'left')
        self.second_room_rsi_entry_entry = tk.Entry(second_roomF, width=2)
        self.second_room_rsi_entry_entry.pack(fill='x', padx=2, pady=2 , side= 'left')

        second_room_rsi_close_label = tk.Label(second_roomF, text = "매도 RSI").pack(fill='x', padx=2, pady=2, side= 'left')
        self.second_room_rsi_close_entry = tk.Entry(second_roomF, width=2)
        self.second_room_rsi_close_entry.pack(fill='x', padx=2, pady=2 , side= 'left')

        second_room_count_label = tk.Label(second_roomF, text = "횟수").pack(fill='x', padx=2, pady=2, side= 'left')
        self.second_room_count_entry = tk.Entry(second_roomF, width=1)
        self.second_room_count_entry.pack(fill='x', padx=2, pady=2 , side= 'left')

        second_room_count_time_label = tk.Label(second_roomF, text='딜레이 시간').pack(fill='x', padx=2, pady=2, side= 'left')
        second_room_count_time_list = [60,80,100,120,150]
        self.second_room_count_time_combobox = ttk.Combobox(second_roomF, width=3,values=second_room_count_time_list,state='readonly')
        self.second_room_count_time_combobox.pack(fill='x', padx=2, pady=2, side='left')
        self.second_room_count_time_combobox.current(0)

        
        def second_room_check():
            self.second_room_is_auto = second_is_auto.get()

        second_is_auto = tk.IntVar()

        autobutton = tk.Radiobutton(second_roomF, text="시작", value=0, variable=second_is_auto, command=second_room_check)
        autobutton.pack(fill='x', padx=2, pady=2, side= 'left')

        nonautobutton = tk.Radiobutton(second_roomF, text="중지", value=1, variable=second_is_auto, command=second_room_check)
        nonautobutton.pack(fill='x', padx=2, pady=2, side= 'left')
        nonautobutton.invoke()


        #--------------------------------
        #----------third frame-----------
        #--------------------------------
        third_roomF = tk.Frame(bodyF, relief='solid', bd=2)
        third_roomF.pack(fill='x', padx=2, pady=2)

        self.third_room_label = tk.Label(third_roomF, text = "3번방",bg = 'red')
        self.third_room_label.pack(fill='x', padx=2, pady=2, side= 'left')

        third_room_bong_entry_lable = tk.Label(third_roomF, text = "매수 분봉").pack(fill='x', padx=2, pady=2, side='left')
        min_bong_combobox_values = ['minute5','minute10','minute15','minute30','minute60']
        self.third_room_bong_entry_combobox = ttk.Combobox(third_roomF,width=10,values=min_bong_combobox_values,state='readonly')
        self.third_room_bong_entry_combobox.pack(fill='x', padx=2, pady=2, side='left')
        self.third_room_bong_entry_combobox.current(0)

        third_room_bong_close_lable = tk.Label(third_roomF, text = "매도 분봉").pack(fill='x', padx=2, pady=2, side='left')
        self.third_room_bong_close_combobox = ttk.Combobox(third_roomF,width=10,values=close_bong_combobox_valuse,state='readonly')
        self.third_room_bong_close_combobox.pack(fill='x', padx=2, pady=2, side='left')
        self.third_room_bong_close_combobox.current(0)
        
        third_room_price_label = tk.Label(third_roomF, text = "매수 가격").pack(fill='x', padx=2, pady=2, side='left')
        self.third_room_price_entry = tk.Entry(third_roomF, width=7)
        self.third_room_price_entry.pack(fill='x', padx=2, pady=2, side='left')
        
        third_room_rsi_entry_label = tk.Label(third_roomF, text = "매수 RSI").pack(fill='x', padx=2, pady=2, side= 'left')
        self.third_room_rsi_entry_entry = tk.Entry(third_roomF, width=2)
        self.third_room_rsi_entry_entry.pack(fill='x', padx=2, pady=2 , side= 'left')

        third_room_rsi_close_label = tk.Label(third_roomF, text = "매도 RSI").pack(fill='x', padx=2, pady=2, side= 'left')
        self.third_room_rsi_close_entry = tk.Entry(third_roomF, width=2)
        self.third_room_rsi_close_entry.pack(fill='x', padx=2, pady=2 , side= 'left')

        third_room_count_label = tk.Label(third_roomF, text = "횟수").pack(fill='x', padx=2, pady=2, side= 'left')
        self.third_room_count_entry = tk.Entry(third_roomF, width=1)
        self.third_room_count_entry.pack(fill='x', padx=2, pady=2 , side= 'left')

        third_room_count_time_label = tk.Label(third_roomF, text='딜레이 시간').pack(fill='x', padx=2, pady=2, side= 'left')
        third_room_count_time_list = [60,120,180,240]
        self.third_room_count_time_combobox = ttk.Combobox(third_roomF, width=3,values=third_room_count_time_list,state='readonly')
        self.third_room_count_time_combobox.pack(fill='x', padx=2, pady=2, side='left')
        self.third_room_count_time_combobox.current(0)

        
        def third_room_check():
            self.third_room_is_auto = third_is_auto.get()

        third_is_auto = tk.IntVar()

        autobutton = tk.Radiobutton(third_roomF, text="시작", value=0, variable=third_is_auto, command=third_room_check)
        autobutton.pack(fill='x', padx=2, pady=2, side= 'left')

        nonautobutton = tk.Radiobutton(third_roomF, text="중지", value=1, variable=third_is_auto, command=third_room_check)
        nonautobutton.pack(fill='x', padx=2, pady=2, side= 'left')
        nonautobutton.invoke()

        #--------------------------------
        #----------fourth----------------
        #--------------------------------
        
        fourth_roomF = tk.Frame(bodyF, relief='solid', bd=2)
        fourth_roomF.pack(fill='x', padx=2, pady=2)

        self.fourth_room_label = tk.Label(fourth_roomF, text = "4번방",bg = 'red')
        self.fourth_room_label.pack(fill='x', padx=2, pady=2, side= 'left')


        fourth_room_bong_entry_lable = tk.Label(fourth_roomF, text = "매수 분봉").pack(fill='x', padx=2, pady=2, side='left')
        min_bong_combobox_values = ['minute30', 'minute60']
        self.fourth_room_bong_entry_combobox = ttk.Combobox(fourth_roomF,width=10,values=min_bong_combobox_values,state='readonly')
        self.fourth_room_bong_entry_combobox.pack(fill='x', padx=2, pady=2, side='left')
        self.fourth_room_bong_entry_combobox.current(0)

        fourth_room_bong_close_lable = tk.Label(fourth_roomF, text = "매도 분봉").pack(fill='x', padx=2, pady=2, side='left')
        self.fourth_room_bong_close_combobox = ttk.Combobox(fourth_roomF,width=10,values=close_bong_combobox_valuse,state='readonly')
        self.fourth_room_bong_close_combobox.pack(fill='x', padx=2, pady=2, side='left')
        self.fourth_room_bong_close_combobox.current(0)


        fourth_room_price_label = tk.Label(fourth_roomF, text = "매수 가격").pack(fill='x', padx=2, pady=2, side='left')
        self.fourth_room_price_entry = tk.Entry(fourth_roomF, width=7)
        self.fourth_room_price_entry.pack(fill='x', padx=2, pady=2, side='left')
        
        fourth_room_rsi_entry_label = tk.Label(fourth_roomF, text = "매수 RSI").pack(fill='x', padx=2, pady=2, side= 'left')
        self.fourth_room_rsi_entry_entry = tk.Entry(fourth_roomF, width=2)
        self.fourth_room_rsi_entry_entry.pack(fill='x', padx=2, pady=2 , side= 'left')

        fourth_room_rsi_close_label = tk.Label(fourth_roomF, text = "매도 RSI").pack(fill='x', padx=2, pady=2, side= 'left')
        self.fourth_room_rsi_close_entry = tk.Entry(fourth_roomF, width=2)
        self.fourth_room_rsi_close_entry.pack(fill='x', padx=2, pady=2 , side= 'left')

        fourth_room_count_label = tk.Label(fourth_roomF, text = "횟수").pack(fill='x', padx=2, pady=2, side= 'left')
        self.fourth_room_count_entry = tk.Entry(fourth_roomF, width=1)
        self.fourth_room_count_entry.pack(fill='x', padx=2, pady=2 , side= 'left')

        fourth_room_count_time_label = tk.Label(fourth_roomF, text='딜레이 시간').pack(fill='x', padx=2, pady=2, side= 'left')
        fourth_room_count_time_list = [60,120,180,240]
        self.fourth_room_count_time_combobox = ttk.Combobox(fourth_roomF, width=3,values=fourth_room_count_time_list,state='readonly')
        self.fourth_room_count_time_combobox.pack(fill='x', padx=2, pady=2, side='left')
        self.fourth_room_count_time_combobox.current(0)

        
        def fourth_room_check():
            self.fourth_room_is_auto = fourth_is_auto.get()

        fourth_is_auto = tk.IntVar()

        autobutton = tk.Radiobutton(fourth_roomF, text="시작", value=0, variable=fourth_is_auto, command=fourth_room_check)
        autobutton.pack(fill='x', padx=2, pady=2, side= 'left')

        nonautobutton = tk.Radiobutton(fourth_roomF, text="중지", value=1, variable=fourth_is_auto, command=fourth_room_check)
        nonautobutton.pack(fill='x', padx=2, pady=2, side= 'left')
        nonautobutton.invoke()

        bodyF = tk.Frame(self.root, bd=2)
        bodyF.pack(fill='x', padx=2, pady=2)

        #--------------------------------
        #----------Special frame---------
        #--------------------------------

        special_roomF = tk.Frame(bodyF, relief='solid', bd=2)
        special_roomF.pack(fill='x', padx=2, pady=2)

        self.special_room_label = tk.Label(special_roomF, text = "SBD방",bg = 'red')
        self.special_room_label.pack(fill='x', padx=2, pady=2, side= 'left')


        special_room_bong_entry_lable = tk.Label(special_roomF, text = "매수 분봉").pack(fill='x', padx=2, pady=2, side='left')
        min_bong_combobox_values = ['minute1','minute3','minute5','minute10']
        self.special_room_bong_entry_combobox = ttk.Combobox(special_roomF,width=10,values=min_bong_combobox_values,state='readonly')
        self.special_room_bong_entry_combobox.pack(fill='x', padx=2, pady=2, side='left')
        self.special_room_bong_entry_combobox.current(1)

        special_room_bong_close_lable = tk.Label(special_roomF, text = "매도 분봉").pack(fill='x', padx=2, pady=2, side='left')
        self.special_room_bong_close_combobox = ttk.Combobox(special_roomF,width=10,values=close_bong_combobox_valuse,state='readonly')
        self.special_room_bong_close_combobox.pack(fill='x', padx=2, pady=2, side='left')
        self.special_room_bong_close_combobox.current(1)
        
        special_room_price_label = tk.Label(special_roomF, text = "매수 가격").pack(fill='x', padx=2, pady=2, side='left')
        self.special_room_price_entry = tk.Entry(special_roomF, width=7)
        self.special_room_price_entry.pack(fill='x', padx=2, pady=2, side='left')
        
        special_room_rsi_entry_label = tk.Label(special_roomF, text = "매수 RSI").pack(fill='x', padx=2, pady=2, side= 'left')
        self.special_room_rsi_entry_entry = tk.Entry(special_roomF, width=2)
        self.special_room_rsi_entry_entry.pack(fill='x', padx=2, pady=2 , side= 'left')

        special_room_rsi_close_label = tk.Label(special_roomF, text = "매도 RSI").pack(fill='x', padx=2, pady=2, side= 'left')
        self.special_room_rsi_close_entry = tk.Entry(special_roomF, width=2)
        self.special_room_rsi_close_entry.pack(fill='x', padx=2, pady=2 , side= 'left')

        special_room_count_label = tk.Label(special_roomF, text = "횟수").pack(fill='x', padx=2, pady=2, side= 'left')
        special_room_count_entry = tk.Label(special_roomF, text = "4")
        special_room_count_entry.pack(fill='x', padx=2, pady=2, side= 'left')
        self.special_room_count_entry = int(special_room_count_entry['text'])

        self.special_room_count_time_list = [10,20,30,50]

        self.special_room_count = 0
        self.special_room_delay_time = 0

        def special_room_check():
            self.special_room_is_auto = special_is_auto.get()

        special_is_auto = tk.IntVar()

        autobutton = tk.Radiobutton(special_roomF, text="시작", value=0, variable=special_is_auto, command=special_room_check)
        autobutton.pack(fill='x', padx=2, pady=2, side= 'left')

        nonautobutton = tk.Radiobutton(special_roomF, text="중지", value=1, variable=special_is_auto, command=special_room_check)
        nonautobutton.pack(fill='x', padx=2, pady=2, side= 'left')
        nonautobutton.invoke()
       
if __name__ == "__main__":
    root = tk.Tk()
    app = App(root)
    
    