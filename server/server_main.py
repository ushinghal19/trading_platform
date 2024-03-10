import argparse
from flask import Flask, jsonify, Response
from apscheduler.schedulers.background import BackgroundScheduler
from data import Data

# Function to parse command line arguments
def parse_arguments():
    parser = argparse.ArgumentParser(description='Trading signals server.')
    parser.add_argument('--tickers', nargs='+', help='List of tickers the server is interested in',
                        default=['AAPL', 'MSFT'])
    parser.add_argument('--port', type=int, help='Network port for the server', default=8000)
    parser.add_argument('--interval', type=str,
                        help='Interval for updating quotes. Options are: 1min, 5min, 15min, 30min, 60min',
                        default='5min')
    return parser.parse_args()



# Function to initialize historical data from Alphavantage
def initialize_data():
    for ticker in args.tickers:
        data_storage.update_historical_data(ticker, args.interval)


# Function to periodically update data from Finnhub
def scheduled_update():
    for ticker in args.tickers:
        data_storage.update_current_quote(ticker, args.interval)


# Initialize Flask app, Data, and parse arguments
args = parse_arguments()
app = Flask(__name__)
data_storage = Data()
initialize_data()
scheduler = BackgroundScheduler()
scheduler.add_job(scheduled_update, 'interval', minutes=int(args.interval[:-3]))
scheduler.start()

# Route to get data for a specific datetime
@app.route('/data/<datetime>', methods=['GET'])
def get_data_for_datetime(datetime):
    data = data_storage.get_data_for_datetime(datetime)
    # Convert the pandas Series to a dictionary
    data_dict = data.to_dict()

    # Reformat dictionary:
    result = ""
    for key in data_dict['ticker']:
        result += f"{data_dict['ticker'][key]} {data_dict['price'][key]} {data_dict['signal'][key]}\n"

    return result


# Route to add a ticker
@app.route('/add_ticker/<ticker>', methods=['POST'])
def add_ticker(ticker):
    args.tickers.append(ticker)
    data_storage.update_historical_data(ticker, args.interval)
    return jsonify({'status': 'success', 'message': f'{ticker} successfully added! :)'})


# Route to delete a ticker
@app.route('/delete_ticker/<ticker>', methods=['DELETE'])
def delete_ticker(ticker):
    if ticker in args.tickers:
        args.tickers.remove(ticker)
        # You will also need to handle the removal of this ticker's data from your Data class
        data_storage.remove_ticker_data(ticker)
        return jsonify({'status': 'success', 'message': f'{ticker} successfully deleted! :)'})
    else:
        return jsonify({'status': 'failure', 'message': f'{ticker} not found in the list.'})


# Route to generate and download a report
@app.route('/report', methods=['GET'])
def download_report():
    # Create a response object with the CSV string as the file content
    response = Response(
        data_storage.get_dataframe().to_csv(),
        mimetype='text/csv',
        headers={"Content-disposition": "attachment; filename=report.csv"}
    )

    return response


# Run the Flask app
if __name__ == '__main__':
    app.run(debug=True, port=args.port)
