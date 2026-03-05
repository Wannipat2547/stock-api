from fastapi import FastAPI
from pydantic import BaseModel # นำเข้า BaseModel มาช่วยรับข้อมูล
import yfinance as yf
import matplotlib.pyplot as plt
import pandas as pd
import base64
from io import BytesIO

app = FastAPI()

# สร้างคลาสสำหรับรับค่า Body
class StockRequest(BaseModel):
    symbol: str

@app.get("/")
def home():
    return {"status": "Stock API running"}

@app.post("/analyze")
def analyze_stock(data: StockRequest): # เปลี่ยนมารับข้อมูลผ่านคลาสนี้

    symbol = data.symbol # เรียกใช้ผ่าน .symbol

    df = yf.Ticker(symbol).history(period="6mo")

    df["MA30"] = df["Close"].rolling(30).mean()

    plt.figure(figsize=(10,5))
    plt.plot(df["Close"], label="Price")
    plt.plot(df["MA30"], label="MA30")
    plt.legend()

    buffer = BytesIO()
    plt.savefig(buffer, format="png")
    buffer.seek(0)

    image_base64 = base64.b64encode(buffer.read()).decode()

    plt.close() # 🔴 สำคัญมาก! เคลียร์กราฟทิ้ง ป้องกันเซิร์ฟเวอร์เมมโมรี่เต็ม

    return {
        "symbol": symbol,
        "chart": image_base64
    }
