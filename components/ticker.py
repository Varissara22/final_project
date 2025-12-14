import tkinter as tk
import websocket
import json
import threading
from config import Config

class PriceTickerCard:
    #box of price on top of dashboard
    def __init__(self, parent, symbol, display_name):
        self.parent = parent
        self.symbol = symbol.lower()
        self.display_name = display_name
        self.is_active = False
        self.ws = None
        
        self.create_ui()
        
    def create_ui(self): #symbol, price, changed percentage at here
        self.frame = tk.Frame(
            self.parent,
            bg=Config.color_bg_card,
            relief="flat",
            highlightthickness=1,
            highlightbackground=Config.color_border
        )
        
        tk.Label(
            self.frame,
            text=self.display_name,
            font=("Segoe UI", 10, "bold"),
            bg=Config.color_bg_card,
            fg=Config.color_text_primary
        ).pack(anchor="w", padx=10, pady=(8, 2))
        
        self.price_label = tk.Label(
            self.frame,
            text="$--,---",
            font=("Segoe UI", 16, "bold"),
            bg=Config.color_bg_card,
            fg=Config.color_text_primary
        )
        self.price_label.pack(anchor="w", padx=10)
        
        self.change_label = tk.Label(
            self.frame,
            text="--",
            font=("Segoe UI", 9),
            bg=Config.color_bg_card,
            fg=Config.color_text_secondary
        )
        self.change_label.pack(anchor="w", padx=10, pady=(0, 8))
        
    def start(self): #websocket
        if self.is_active:
            return
        self.is_active = True
        
        ws_url = f"wss://stream.binance.com:9443/ws/{self.symbol}@ticker"
        self.ws = websocket.WebSocketApp(
            ws_url,
            on_message=self.on_message,
            on_error=lambda ws, e: None,
            on_close=lambda ws, s, m: None
        )
        threading.Thread(target=self.ws.run_forever, daemon=True).start()
        
    def stop(self):
        self.is_active = False
        if self.ws:
            self.ws.close()
            self.ws = None
      
    def on_message(self, ws, message): 
        if not self.is_active:
            return
        try:
            data = json.loads(message)
            price = float(data['c'])
            percent = float(data['P'])
            self.parent.after(0, self.update_display, price, percent)
        except json.JSONDecodeError:
            print(f"Invalid JSON in ticker message")
        except KeyError as e:
            print(f"Missing key in ticker data: {e}")
        except ValueError as e:
            print(f"Invalid number in ticker data: {e}")
        except Exception as e:
            print(f"Unexpected error in ticker: {e}")
            
    def update_display(self, price, percent):
        if not self.is_active:
            return
        
        color = Config.color_positve_num if percent >= 0 else Config.color_negative_num
        self.price_label.config(text=f"${price:,.2f}")
        
        arrow = "▲" if percent >= 0 else "▼"
        self.change_label.config(
            text=f"{arrow} {abs(percent):.2f}%",
            fg=color
        )