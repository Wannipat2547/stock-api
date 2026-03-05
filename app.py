from fastapi import FastAPI
import yfinance as yf
import pandas as pd
import matplotlib.pyplot as plt

app = FastAPI()

@app.get("/")
def home():
    return {"message": "Stock API running"}

@app.get("/analyze/{ticker}")
def analyze_stock(ticker: str):

    df = yf.Ticker(ticker).history(period="6mo")

    df["MA30"] = df["Close"].rolling(30).mean()

    plt.figure(figsize=(10,5))
    plt.plot(df.index, df["Close"], label="Price")
    plt.plot(df.index, df["MA30"], label="MA30")

    plt.legend()
    plt.title(f"{ticker} Price with MA30")

    file = f"{ticker}.png"

    plt.savefig(file)

    return {
        "ticker": ticker,
        "chart": file
    }
