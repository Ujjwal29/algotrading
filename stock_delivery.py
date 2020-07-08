from nsetools import Nse
from pprint import pprint
import pandas as pd
from tqdm import tqdm

nse=Nse()

stocks = list(nse.get_stock_codes().keys())

unwanted_stocks = ['SYMBOL', '3PLAND', 'ANKITMETAL', 'BURNPUR', 'CHROMATIC', 'CREATIVEYE', 'DCMFINSERV', 'EASTSILK', 'EUROMULTI', 'EUROTEXIND', 
                   'EXCEL', 'GAYAHWS', 'GISOLUTION', 'GLOBOFFS', 'HBSL', 'INTEGRA', 'KALYANI', 'KAUSHALYA', 'MOHOTAIND', 'MOHITIND', 'MUKANDENGG', 
                   'NAGREEKCAP', 'NAGREEKCAP', 'NATNLSTEEL', 'NIRAJISPAT', 'NORBTEAEXP', 'NTL', 'OMKARCHEM', 'PAEL', 'PRADIP', 'PREMIER', 'RADAAN', 
                   'SABEVENTS', 'SHYAMTEL', 'SOMATEX', 'TECHIN', 'TFL', 'TGBHOTELS', 'VIVIDHA', 'YESBANK', 'ZICOM' ]

stocks = [stock for stock in stocks if stock not in unwanted_stocks]


price=[]
company=[]
symbol=[]

for stock in tqdm(stocks[:10]):
    q = nse.get_quote(stock)
    if(q['deliveryToTradedQuantity'] is not None):
        if((q['deliveryToTradedQuantity']>90)):
            company.append(q['companyName'])
            price.append(q['lastPrice'])
            symbol.append(q['symbol'])
            

data = {'Symbol':symbol, 'Company Name':company, 'Price':price}
df = pd.DataFrame.from_dict(data)
df.to_csv('Stocks_with_delivery_greater_than_90.csv', index=False)