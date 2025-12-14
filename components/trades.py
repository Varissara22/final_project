import tkinter as tk
from tkinter import ttk
import websocket
import json
import threading
from datetime import datetime
from collections import deque
from config import Config

class RecentTradesPanel:
    def __init__(self, parent):
        self.parent = parent
        self.current_symbol = None
        self.is_active = False
        self.ws = None
        self.trades = deque(maxlen=20)
        
        self.create_ui()
        
    def create_ui(self):
        self.frame = tk.Frame(self.parent, bg=Config.color_bg_card)
        
        header = tk.Frame(self.frame, bg=Config.color_bg_card)
        header.pack(fill=tk.X, padx=15, pady=10)
        
        tk.Label(
            header,
            text="Recent Trades",
            font=("Segoe UI", 12, "bold"),
            bg=Config.color_bg_card,
            fg=Config.color_text_primary
        ).pack(side=tk.LEFT)
        
        cols_frame = tk.Frame(self.frame, bg=Config.color_bg_card)
        cols_frame.pack(fill=tk.X, padx=15, pady=(0, 5))
        
        tk.Label(
            cols_frame,
            text="Time",
            font=("Segoe UI", 8),
            bg=Config.color_bg_card,
            fg=Config.color_text_secondary,
            width=10,
            anchor="w"
        ).pack(side=tk.LEFT, padx=2)
        
        tk.Label(
            cols_frame,
            text="Price",
            font=("Segoe UI", 8),
            bg=Config.color_bg_card,
            fg=Config.color_text_secondary,
            width=12,
            anchor="e"
        ).pack(side=tk.LEFT, padx=2)
        
        tk.Label(
            cols_frame,
            text="Quantity",
            font=("Segoe UI", 8),
            bg=Config.color_bg_card,
            fg=Config.color_text_secondary,
            width=12,
            anchor="e"
        ).pack(side=tk.LEFT, padx=2)
        
        trades_container = tk.Frame(self.frame, bg=Config.color_bg_card)
        trades_container.pack(fill=tk.BOTH, expand=True, padx=15, pady=(0, 15))
        
        self.trade_labels = []
        for i in range(15):
            row_frame = tk.Frame(trades_container, bg=Config.color_bg_card)
            row_frame.pack(fill=tk.X, pady=1)
            
            time_label = tk.Label(
                row_frame,
                text="--:--:--",
                font=("Consolas", 8),
                bg=Config.color_bg_card,
                fg=Config.color_text_secondary,
                width=10,
                anchor="w"
            )
            time_label.pack(side=tk.LEFT, padx=2)
            
            price_label = tk.Label(
                row_frame,
                text="---",
                font=("Consolas", 9),
                bg=Config.color_bg_card,
                fg=Config.color_text_primary,
                width=12,
                anchor="e"
            )
            price_label.pack(side=tk.LEFT, padx=2)
            
            qty_label = tk.Label(
                row_frame,
                text="---",
                font=("Consolas", 8),
                bg=Config.color_bg_card,
                fg=Config.color_text_secondary,
                width=12,
                anchor="e"
            )
            qty_label.pack(side=tk.LEFT, padx=2)
            
            self.trade_labels.append((time_label, price_label, qty_label))
    
    def set_symbol(self, symbol):
        if self.current_symbol == symbol:
            return
        self.stop()
        self.current_symbol = symbol
        self.trades.clear()
        self.start()
        
    def start(self):
        if not self.current_symbol or self.is_active:
            return
        self.is_active = True
        
        symbol_lower = self.current_symbol.lower()
        ws_url = f"wss://stream.binance.com:9443/ws/{symbol_lower}@trade"
        
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
            trade = {
                'time': datetime.fromtimestamp(data['T'] / 1000).strftime('%H:%M:%S'),
                'price': float(data['p']),
                'quantity': float(data['q']),
                'is_buyer_maker': data['m']
            }
            self.trades.appendleft(trade)
            self.parent.after(0, self.update_display)
        except json.JSONDecodeError:
            print("Invalid JSON in trades message")
        except KeyError as e:
            print(f"Missing key in trades data: {e}")
        except Exception as e:
            print(f"Unexpected error in trades: {e}")
            
    def update_display(self):
        if not self.is_active:
            return
        
        for i, (time_label, price_label, qty_label) in enumerate(self.trade_labels):
            if i < len(self.trades):
                trade = list(self.trades)[i]
                time_label.config(text=trade['time'])
                price_label.config(text=f"{trade['price']:,.2f}")
                qty_label.config(text=f"{trade['quantity']:.6f}")
                
                # Color based on buyer/seller (red = sell, green = buy)
                color = Config.color_negative_num if trade['is_buyer_maker'] else Config.color_positve_num
                price_label.config(fg=color)
            else:
                time_label.config(text="--:--:--")
                price_label.config(text="---")
                qty_label.config(text="---")