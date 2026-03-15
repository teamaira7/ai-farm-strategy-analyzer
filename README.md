# AI Farm Strategy Advisor 🌾🤖

AI Farm Strategy Advisor is an **AI-powered decision support system** that helps farmers evaluate multiple farming strategies under uncertainty.

Agriculture decisions are heavily affected by **rainfall variability, market price fluctuations, and soil conditions**. Instead of providing a single fixed recommendation, this system allows farmers to **simulate different strategies and compare potential outcomes before planting**.

The platform combines **machine learning price prediction** with **Monte Carlo simulations** to estimate possible yield, revenue, and risk levels for different crop strategies.

---

## Problem

Farmers often make crop planning decisions with **limited information and high uncertainty**.  
Unexpected weather changes or sudden price drops can lead to **significant financial losses**.

Current advisory tools usually provide **static recommendations**, which do not account for uncertainty or allow farmers to compare multiple strategies.

There is a need for a system that helps farmers **understand risk and make informed decisions**.

---

## Solution

AI Farm Strategy Advisor enables farmers to:

- Compare multiple crop strategies  
- Predict crop prices using machine learning  
- Simulate outcomes under uncertain conditions  
- Visualize best-case, worst-case, and average scenarios  

Using **Monte Carlo simulations**, the platform generates thousands of possible outcomes and provides insights that help farmers choose **more resilient and profitable strategies**.

---

## Features

- Crop price prediction using ML  
- Farming strategy comparison  
- Monte Carlo simulation for risk analysis  
- Visualization of expected revenue and variability  
- Simple and interactive dashboard  

---

## Tech Stack

- Python  
- Streamlit  
- Pandas / NumPy  
- Scikit-learn  
- Matplotlib / Plotly  

---

## Project Structure

```
AI Farm Strategy Advisor
│
├── app.py                # Streamlit UI
├── simulation.py         # Monte Carlo simulation engine
├── price_prediction.py   # ML model for crop price prediction
├── requirements.txt
├── data/
│   └── crop_prices.csv
└── screenshots/
    └── dashboard.png
```

---

## How It Works

1. Farmer selects crop and strategy parameters  
2. ML model predicts future crop price trends  
3. Monte Carlo simulation generates possible yield and revenue scenarios  
4. Dashboard visualizes outcomes for strategy comparison  

This helps farmers understand **risk vs reward** before making planting decisions.

---

## How to Run the Project

Install dependencies:

```bash
pip install -r requirements.txt
```

Run the Streamlit app:

```bash
streamlit run app.py
```

---

## Impact

This project aims to **empower farmers with data-driven decision tools**.

Potential benefits include:

- Reduced financial risk  
- Better crop planning decisions  
- Increased farm profitability  
- More resilient agricultural practices  

---

## Future Improvements

- Integration with real-time weather data  
- Regional language support for farmers  
- Mobile-friendly deployment  
- Government agriculture dataset integration  

---

## Team

**Team AIRA**

AI-driven solutions for smarter agriculture 🌱
