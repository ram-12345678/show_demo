from flask import Flask, render_template, jsonify
import yfinance as yf
import pandas as pd
import plotly.graph_objs as go
import plotly.utils
import json

app = Flask(__name__)

# Define the ticker symbol for DLF (listed on NSE)
ticker_symbol = 'DLF.NS'

@app.route('/')
def index():
    # Fetch the stock data
    ticker = yf.Ticker(ticker_symbol)
    stock_data = ticker.history(period="1d", interval="1m")

    # Ensure data is not empty
    if not stock_data.empty:
        # Extract relevant data for visualization and table
        stock_data.reset_index(inplace=True)
        stock_data['Datetime'] = stock_data['Datetime'].dt.strftime('%Y-%m-%d %H:%M:%S')
        
        # Create plotly figure
        fig = go.Figure()
        fig.add_trace(go.Scatter(x=stock_data['Datetime'], y=stock_data['Close'], mode='lines', name='Close Price'))
        fig.update_layout(title=f'Real-time Stock Data for {ticker_symbol}', xaxis_title='Time', yaxis_title='Price (INR)')

        # Convert plotly figure to JSON
        graphJSON = json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)

        # Prepare data for table display
        table_data = stock_data[['Datetime', 'Open', 'High', 'Low', 'Close', 'Volume']].tail(10).to_dict('records')

        return render_template('index.html', table_data=table_data, graphJSON=graphJSON)
    else:
        return render_template('index.html', table_data=[], graphJSON={})

if __name__ == '__main__':
    app.run(debug=True)
