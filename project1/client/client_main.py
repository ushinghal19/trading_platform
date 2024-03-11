import argparse
import requests


def parse_arguments():
    """ Parses arguments from user. """
    parser = argparse.ArgumentParser(description='Client for querying the trading signals server.')
    parser.add_argument('--server', type=str, help='Server IP and port in the format ip:port', default='127.0.0.1:8000')
    return parser.parse_args()


def get_latest_data(server, datetime):
    """ Makes a request to the server for latest data"""
    response = requests.get(f'http://{server}/data/{datetime}')
    if response.ok:
        print(response.text)
    else:
        print("Failed to retrieve data.")


def add_ticker(server, ticker):
    """ Sends a command to add a new ticker"""
    response = requests.post(f'http://{server}/add_ticker/{ticker}')
    if response.ok:
        print(response.json())
    else:
        print("Failed to add ticker.")


def delete_ticker(server, ticker):
    """ Sends a command to delete a ticker """
    response = requests.delete(f'http://{server}/delete_ticker/{ticker}')
    if response.ok:
        print(response.json())
    else:
        print("Failed to delete ticker.")


def download_report(server):
    """ Requests the server to generate and download a report"""
    response = requests.get(f'http://{server}/report')
    if response.ok:
        with open('report.csv', 'wb') as file:
            file.write(response.content)
        print("Report downloaded successfully.")
    else:
        print("Failed to download report.")


if __name__ == '__main__':
    args = parse_arguments()

    # Main loop for the client to accept commands
    while True:
        try:
            user_input = input('Enter command: ').strip().split()
            command = user_input[0].lower()

            if command == 'data' and len(user_input) == 2:
                get_latest_data(args.server, user_input[1])
            elif command == 'add' and len(user_input) == 2:
                add_ticker(args.server, user_input[1])
            elif command == 'delete' and len(user_input) == 2:
                delete_ticker(args.server, user_input[1])
            elif command == 'report':
                download_report(args.server)
            elif command == 'exit':
                break
            else:
                print('Invalid command or incorrect number of arguments.')
        except KeyboardInterrupt:
            break
        except Exception as e:
            print(f"An error occurred: {e}")
