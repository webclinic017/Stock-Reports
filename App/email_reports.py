import requests
import pickle
import datetime
from config import *
from alpaca_functions import *
import alpaca_trade_api as tradeapi
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

api = tradeapi.REST(API_KEY, SECRET_KEY, BASE_URL)

def sendEmail(to_address, subject, msg):

    message = MIMEMultipart()
    
    message['Subject'] = subject
    message['From'] = FROM_ADDRESS
    message['To'] = ", ".join(to_address)
    
    content = MIMEText(msg)
    message.attach(content)
    
    mail = smtplib.SMTP('smtp.gmail.com', 587)
    mail.ehlo()
    mail.starttls()
    mail.login(FROM_ADDRESS, EMAIL_PW)
    mail.sendmail(FROM_ADDRESS,to_address, message.as_string())
    
    mail.close()

# I want to work with pickle file for learning and txt file for readability
stocks = []


# Grab stocks from watchlist in case new stocks were added there
watchlist = api.get_watchlist('10c71436-8e6b-4d08-9b43-030cbe3ae6c2').assets

for i in range(0, len(watchlist)):
    symbol = watchlist[i]['symbol']
    stocks.append(symbol)
    
    
# Grab current positions in case new stocks were bought
current_positions = api.list_positions()

for i in range(0, len(current_positions) - 1):
    symbol = vars(current_positions[i])['_raw']['symbol']
    stocks.append(symbol)
    
    
# Grab initial stocks from given list if it exists
try:
    [stocks.append(line.rstrip()) for line in open("stocks.txt", "r")]
except (OSError, IOError) as e:
    with open('stocks.txt', 'w') as f:
        for stock in stocks:
            f.write("%s\n" % stocks) 
    [stocks.append(line.rstrip()) for line in open("stocks.txt", "r")]
        
        
# Grab stocks from updated pickle file if it exists
try:
    pickle_stocks = pickle.load(open("stocks_list.pickle", "rb"))
except (OSError, IOError) as e:
    pickle.dump(stocks, open("stocks_list.pickle", "wb"))
    pickle_stocks = pickle.load(open("stocks_list.pickle", "rb"))    

    
stocks = list(set(stocks + pickle_stocks))
stocks.sort()
    
# Store in pickle file and txt file
with open('stocks_list', 'wb') as fp:
    pickle.dump(stocks, fp)

with open('stocks.txt', 'w') as f:
    for stock in stocks:
        f.write("%s\n" % stock)

stocks_string = "\n".join(stocks)

sendEmail('jjmorr13@yahoo.com', 'Stock List', msg = stocks_string)