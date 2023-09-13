import tkinter as tk
from tkinter import ttk
import requests

# Function to fetch cryptocurrency symbols
def fetch_crypto_symbols():
    try:
        response = requests.get("https://api.coingecko.com/api/v3/coins/list")
        data = response.json()
        crypto_symbols = [crypto["symbol"].capitalize() for crypto in data]
        crypto_combobox["values"] = crypto_symbols
        crypto_combobox.set("Btc")  # Set BTC as the default cryptocurrency
    except Exception as e:
        pass

# Function to filter and suggest cryptocurrency names
def suggest_crypto(event):
    typed_text = event.widget.get().lower()
    filtered_cryptos = [crypto for crypto in crypto_combobox["values"] if typed_text in crypto.lower()]
    crypto_combobox["values"] = filtered_cryptos
    if filtered_cryptos:
        crypto_combobox.set(filtered_cryptos[0])

# Function to fetch cryptocurrency prices
def fetch_crypto_prices():
    try:
        currency = currency_combobox.get().lower()
        crypto = crypto_combobox.get().lower()
        url = f"https://api.coingecko.com/api/v3/simple/price?ids={crypto}&vs_currencies={currency}"
        response = requests.get(url)
        data = response.json()
        current_price = data[crypto][currency]
        current_price_entry.delete(0, tk.END)
        current_price_entry.insert(0, current_price)
    except Exception as e:
        current_price_entry.delete(0, tk.END)
        current_price_entry.insert(0, "Error fetching price")

# Function to calculate investment data
def calculate_investment():
    try:
        investment = float(investment_entry.get())
        current_price = float(current_price_entry.get())
        selling_price = float(selling_price_entry.get())
        investment_percentage = float(percentage_entry.get())
        exit_rate = float(exit_rate_entry.get())

        profit = investment * (exit_rate / 100) - investment
        profit_label.config(text=f"Profit: ${profit:.2f}")

        data_label.config(text=f"Investment: ${investment:.2f}\n"
                                f"Current Price: ${current_price:.2f}\n"
                                f"Selling Price: ${selling_price:.2f}\n"
                                f"Investment Percentage: {investment_percentage}%\n"
                                f"Exit Rate: {exit_rate}%")

    except ValueError:
        profit_label.config(text="Invalid input")

# Create the main window
window = tk.Tk()
window.title("Cryptocurrency Investment Calculator")
window.geometry("400x400")
window.configure(bg="black")

# Create and configure widgets
currency_label = tk.Label(window, text="Select Currency:", font=("Helvetica", 12), bg="black", fg="white")
crypto_label = tk.Label(window, text="Choose Cryptocurrency:", font=("Helvetica", 12), bg="black", fg="white")
investment_label = tk.Label(window, text="Investment:", font=("Helvetica", 12), bg="black", fg="white")
current_price_label = tk.Label(window, text="Current Price:", font=("Helvetica", 12), bg="black", fg="white")
selling_price_label = tk.Label(window, text="Selling Price:", font=("Helvetica", 12), bg="black", fg="white")
percentage_label = tk.Label(window, text="Investment Percentage:", font=("Helvetica", 12), bg="black", fg="white")
exit_rate_label = tk.Label(window, text="Exit Rate:", font=("Helvetica", 12), bg="black", fg="white")
profit_label = tk.Label(window, text="", font=("Helvetica", 14), fg="green", bg="black")
data_label = tk.Label(window, text="", font=("Helvetica", 12), bg="black", fg="white")

currencies = {
    "USD": "🇺🇸",
    "EUR": "🇪🇺",
    "GBP": "🇬🇧",
    "JPY": "🇯🇵",
    "AUD": "🇦🇺",
}
currency_var = tk.StringVar()
currency_combobox = ttk.Combobox(window, textvariable=currency_var, values=list(currencies.keys()), state="readonly")
currency_combobox.set("USD")

crypto_var = tk.StringVar()
crypto_combobox = ttk.Combobox(window, textvariable=crypto_var, state="readonly")
fetch_crypto_symbols()

investment_entry = tk.Entry(window, font=("Helvetica", 12))
current_price_entry = tk.Entry(window, font=("Helvetica", 12))
selling_price_entry = tk.Entry(window, font=("Helvetica", 12))
percentage_entry = tk.Entry(window, font=("Helvetica", 12))
exit_rate_entry = tk.Entry(window, font=("Helvetica", 12))

calculate_button = tk.Button(window, text="Calculate", command=calculate_investment, font=("Helvetica", 12), bg="green", fg="white")
fetch_price_button = tk.Button(window, text="Fetch Current Price", command=fetch_crypto_prices, font=("Helvetica", 12))

# Place widgets on the window
currency_label.grid(row=0, column=0, padx=10, pady=5, sticky="w")
currency_combobox.grid(row=0, column=1, padx=10, pady=5)
crypto_label.grid(row=1, column=0, padx=10, pady=5, sticky="w")
crypto_combobox.grid(row=1, column=1, padx=10, pady=5)
investment_label.grid(row=2, column=0, padx=10, pady=5, sticky="w")
investment_entry.grid(row=2, column=1, padx=10, pady=5)
fetch_price_button.grid(row=3, column=0, columnspan=2, padx=10, pady=5)
current_price_label.grid(row=4, column=0, padx=10, pady=5, sticky="w")
current_price_entry.grid(row=4, column=1, padx=10, pady=5)
selling_price_label.grid(row=5, column=0, padx=10, pady=5, sticky="w")
selling_price_entry.grid(row=5, column=1, padx=10, pady=5)
percentage_label.grid(row=6, column=0, padx=10, pady=5, sticky="w")
percentage_entry.grid(row=6, column=1, padx=10, pady=5)
exit_rate_label.grid(row=7, column=0, padx=10, pady=5, sticky="w")
exit_rate_entry.grid(row=7, column=1, padx=10, pady=5)
calculate_button.grid(row=8, column=0, columnspan=2, padx=10, pady=10)
profit_label.grid(row=9, column=0, columnspan=2, padx=10, pady=5)
data_label.grid(row=10, column=0, columnspan=2, padx=10, pady=5)

# Start the GUI main loop
window.mainloop()
