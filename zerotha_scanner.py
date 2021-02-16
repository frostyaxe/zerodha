# -*- coding: utf-8 -*-
"""
Created on Mon Feb  8 08:09:06 2021

@author: PCS
"""

from datetime import datetime
import os
from threading import Thread
import time

from kiteconnect import KiteConnect, KiteTicker
from openpyxl import load_workbook

from login import ZerodhaAccessToken
import pandas as pd
from stream import Stream


#from client import ClientZerodha
def main():
    #print("ddf")
    #zerodha_access_token = []
    
    wb  = load_workbook('zerotha_scanner.xlsx')
    ws1 = wb["zerotha_scanner"]
    data = ws1.values
    # Get the first line in file as a header line
    columns = next(data)[0:]
    # Create a DataFrame based on the second and subsequent lines of data
    df1 = pd.DataFrame(data, columns=columns)
    '''
    ws2 = wb["Sheet2"]
    data = ws2.values
    # Get the first line in file as a header line
    columns = next(data)[0:]
    # Create a DataFrame based on the second and subsequent lines of data
    df2 = pd.DataFrame(data, columns=columns)'''
    #df1=pd.read_excel("zerotha_scanner.xlsx")
    df2=pd.read_csv("zerotha_scanner_credentials.csv")
    print(df1)
    print(df2)
    zerodha =ZerodhaAccessToken(df2.iloc[0,0],df2.iloc[0,1],df2.iloc[0,4],df2.iloc[0,2],df2.iloc[0,3])
    access_token = zerodha.getaccesstoken()
    kite = KiteConnect(api_key=df2.iloc[0,0])

    kite.set_access_token(access_token)
    print(access_token)
    #zerodha_access_token.append(access_token)
    #kite=ClientZerodha(api_key = 6zfi2amoxjco04yo, zerodha_id = RP7365, kite = kite,multiplier = multiplier, api_secret =     p2zkzvivv3y8fveacsb9ciqnu5y71iul, pin = 244280,access_token = access_token, password = chicu24428)
    instruments = kite.instruments()
    #print(instruments)
    symbol=[]
    tracker_token=[0,0,0,0,0,0,0,0,0,0,0,0,0]
    for i in range(df1.shape[0]):
        symbol.append(df1.iloc[i,0])
    print(symbol)
    for instrument in instruments:
        for i in range(df1.shape[0]):
            if instrument['tradingsymbol'] == symbol[i]:
                tracker_token[i] = instrument['instrument_token']
            elif tracker_token[i]==0:
                tracker_token[i]=1
    print(tracker_token)
    tracker_token[:] = (value for value in tracker_token if value != 0)
    print(tracker_token)
    count=0
    for i in tracker_token:
        if i==1:
            print(df1.iloc[count,0] , "tracker token doesnt exist")
        count+=1
    tracker_token[:] = (value for value in tracker_token if value != 1)
    stream_obj = Stream(kite = kite,zerodha_access_token = access_token,tracker_token = tracker_token,instruments = instruments,df1=df1,df2=df2)
    stream_obj.kws.on_ticks = stream_obj.on_ticks
    stream_obj.kws.on_connect = stream_obj.on_connect
    stream_obj.kws.on_close = stream_obj.on_close

    stream_obj.kws.connect(threaded=True)

    computation = Thread(target=stream_obj.computation)
    computation.start()

    computation.join()

if __name__ == "__main__":
    main()
