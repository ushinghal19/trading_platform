import argparse
from flask import Flask
from apscheduler.schedulers.background import BackgroundScheduler
from trading_signals import update_historical_data, update_current_quote, Data

def parse_arguments():
    parser = argparse.ArgumentParser(description='Trading signals server.')
    parser.add_argument('--tickers', nargs='+', help='List of tickers the server is interested in', default=['AAPL', 'MSFT'])
    parser.add_argument('--port', type=int, help='Network port for the server', default=8000)
    parser.add_argument('--interval', type=str, help='Interval for updating quotes', default='5min')
    return parser.parse_args()

args = parse_arguments()

app = Flask(__name__)
data_storage = Data()  # Initialize your Data storage
scheduler = BackgroundScheduler()
