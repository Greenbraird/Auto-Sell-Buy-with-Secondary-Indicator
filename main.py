from threading import Thread
import gui
import process

def setting_threads(app):
    sell_buy_first_room = Thread(target=process.sell_buy_process.first_room, args=(app,))
    sell_buy_second_room = Thread(target=process.sell_buy_process.second_room, args=(app,))
    sell_buy_third_room = Thread(target=process.sell_buy_process.third_room, args=(app,))
    sell_buy_fourth_room = Thread(target=process.sell_buy_process.fourth_room, args=(app,))

    sell_buy_special_room = Thread(target=process.sell_buy_process.special_room, args=(app,))

    checking_coin = Thread(target=process.checking_bitcoin, args=(app,))

    sell_buy_first_room.daemon = True
    sell_buy_second_room.daemon = True
    sell_buy_third_room.daemon = True
    sell_buy_fourth_room.daemon = True

    sell_buy_special_room.daemon = True

    checking_coin.daemon = True

    sell_buy_first_room.start()
    sell_buy_second_room.start()
    sell_buy_third_room.start()
    sell_buy_fourth_room.start()

    sell_buy_special_room.start()

    checking_coin.start()

if __name__ == "__main__":
    root = gui.tk.Tk()
    app = gui.App(root)
    setting_threads(app)
    app.root.mainloop()
