# Trading Platform - Take-Home Assessment for OTPP

Hello OTPP Team 👋,

I am truly grateful for this opportunity to participate in the Take-Home Assessment. This project was an exciting challenge that allowed me to showcase my abilities and potential. Although the time was limited, I wanted to demonstrate a breadth of skills and deliver a meaningful piece of work.


# Project 1
With additional time, I would have further refined the project by:
- Employing Version Control best practices with frequent, well-documented commits.
- Conducting comprehensive testing, including writing unit tests for all functions and using mocks to emulate endpoints.
- Observing the system in a live environment during trading hours to validate real-time data integration with Finnhub.

The experience was immensely enjoyable, and I am thrilled to present my work to you.

## Project Structure
The project is structured into two main components: `server` and `client`.

### Server
The server is the backbone of this trading platform. It is built using Flask and runs by default on port `8000`. The server's entry point is `server_main.py`, which initializes the Flask application and the scheduled jobs for data retrieval.

Key server subdirectories and files:

- `data`: Contains the `Data` class, which maintains a DataFrame that tracks all the trading data and signals.

- `/api`: Hosts the interface for external data sources. It includes modules for fetching data from Alphavantage and Finnhub APIs.

- `utils`: Provides utility functions to calculate trading signals, P&L, and other analytics.

### Client
The client directory includes `client_main.py`, which allows users to interact with the server through a command-line interface. It can query the server for the latest price, signals, and generate reports.

## Getting Started

To run the project locally, please follow the steps below:

1. **Clone the Repository**
```sh
git clone [repository_url]
cd trading_platform
```
2. **Install Dependencies**
Ensure you have Python 3 installed and then set up a virtual environment:
  ```sh
  python3 -m venv venv  
  source venv/bin/activate  # On Windows use `venv\Scripts\activate`
  pip install -r requirements.txt
  ```
3. **Start the Server**
Run the server using the following command:
```sh
python3 server/server.py --tickers AAPL MSFT TSLA --port 8000 --interval 60min
```
4. **Interact with the Client**
Open a new terminal window and navigate to the client directory to run client_main.py:
```sh
python3 client/client_main.py --server localhost:8000
```
## Usage
Here are some common comands to interact with the client:
1. *Query Data*: `data YYYY-MM-DDTHH:MM`
2. *Add a Ticker*: `add TSLA`
3. *Delete a Ticker*: `delete TSLA`
4. *Generate a Report*: `report`

### Closing Thoughts
This project is a testament to my passion for fintech and my commitment to delivering high-quality software. I hope it meets your expectations and showcases the potential value I can bring to the OTPP team.
I am open to feedback and looking forward to discussing the project in further detail.


#### DEMO!
https://github.com/ushinghal19/trading_platform/assets/56486015/ada34ca4-109f-452d-ab4f-d01c0432277f

# Project 2: 
See OTPP_Random_Forest.ipynb!

Warm regards,

Utsav Shinghal :)
