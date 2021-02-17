from queue import Queue
import time

from kiteconnect import KiteConnect, KiteTicker


#from orders import *
class Stream:
    '''class for the websocket in which all the callback functions are present'''

    def __init__(self, kite, zerodha_access_token, tracker_token, instruments, df1, df2):
        # kite ticker initialization
        self.kws = KiteTicker(df2.iloc[0,0], zerodha_access_token)
        self.kite = kite
        # self.kite.set_access_token(self.access_token)
        self.zerodha_access_token = zerodha_access_token
        self.tracker_token = tracker_token
        self.df1 = df1
        self.df2 = df2
        self.instruments = instruments
        self.ticks_queue = Queue()
        self.exit = 0

    def on_ticks(self, ws, ticks):
        self.ticks_queue.put(ticks)

    def on_connect(self, ws, response):
        # Callback on successful connect.
        
        ws.subscribe(self.tracker_token)
        ws.set_mode(ws.MODE_FULL, self.tracker_token)
    
    def on_reconnect(self, ws, attempt_count):
        print("Reconnecting the websocket: {}".format(attempt_count))
    

    def on_close(self, ws, code, reason):
        # On connection close stop the main loop
        # Reconnection will not happen after executing `ws.stop()`
        ws.stop()
        print('socket closed')

    def computation(self):
        t=[]
        for k in range(len(self.tracker_token)):
            t.append(k)
        while not self.exit:
            # print(self.ticks_queue.get())
            # self.exit=1

            c = self.ticks_queue.get()
            #print(c)
            d = []
            e = []
            
            f = len(c)
            
                
            for i in range(f):
                d.append(c[i]['last_price'])
                e.append(c[i]['instrument_token'])
            #print(d, e)
            #print(t)
            for j in range(f):
                if j in t:
                    try:

                        if(self.df1.iloc[j, 1] == "Greater then or equal to"):
                            if d[e.index(self.tracker_token[j])] >= self.df1.iloc[j, 2]:
                                print(self.df1.iloc[j, 0], d[e.index(self.tracker_token[j])],
                                      "condition is fulfiled")
                                t.remove(j)
                        elif(self.df1.iloc[j, 1] == "Greater then"):
                            if d[e.index(self.tracker_token[j])] > self.df1.iloc[j, 2]:
                                print(self.df1.iloc[j, 0],
                                      "condition is fulfiled")
                                t.remove(j)
                        elif(self.df1.iloc[j, 1] == "Less then or equal to"):
                            if d[e.index(self.tracker_token[j])] <= self.df1.iloc[j, 2]:
                                print(self.df1.iloc[j, 0],
                                      "condition is fulfiled")
                                t.remove(j)
                        elif(self.df1.iloc[j, 1] == "Less then"):
                            if d[e.index(self.tracker_token[j])] < self.df1.iloc[j, 2]:
                                print(self.df1.iloc[j, 0],
                                      "condition is fulfiled")
                                t.remove(j)
                        elif(self.df1.iloc[j, 1] == "Equal to"):
                            if d[e.index(self.tracker_token[j])] == self.df1.iloc[j, 2]:
                                return self.df1.iloc[j, 0] + "condition is fulfiled"
                                t.remove(j)
                        print(t)
                    except:
                        return self.df1.iloc[j, 0] + " tracker token doesnt exist"
                if len(t) == 0:
                    self.exit=1
            # print(c,d,e)

            # def buy_call_option():

            # self.exit = 1 '''
