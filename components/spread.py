import tkinter as tk
import websocket
import json
import threading
from config import Config
from .orderbook import OrderBookPopup 

class BidAskSpreadPanel:   
    def __init__(self, parent):
        self.parent = parent
        self.current_symbol = None
        self.is_active = False
        self.ws = None
        self.orderbook_popup = None
        
        self.create_ui()
        
    def create_ui(self):
        self.frame = tk.Frame(self.parent, bg=Config.color_bg_card)
        
        header_frame = tk.Frame(self.frame, bg=Config.color_bg_card)
        header_frame.pack(fill=tk.X, padx=15, pady=(10, 0))
        
        tk.Label(
            header_frame,
            text="Best Bid / Ask & Spread",
            font=("Segoe UI", 10),
            bg=Config.color_bg_card,
            fg=Config.color_text_secondary
        ).pack(side=tk.LEFT, pady=(0, 10))
        
        import sys
        import os
        sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
        from toggle_switch import ToggleSwitch
        
        self.orderbook_switch = ToggleSwitch(
            header_frame,
            width=115,
            height=30,
            bg_on="#3b82f6",
            bg_off="#6b7280",
            text_on="CLOSE",
            text_off="Order book",
            command=self.on_orderbook_toggle
        )
        self.orderbook_switch.pack(side=tk.RIGHT, pady=(0, 10))
        
        bid_frame = tk.Frame(self.frame, bg=Config.color_bg_card)
        bid_frame.pack(fill=tk.BOTH, expand=True, padx=15, pady=(0, 10))
        
        bid_info = tk.Frame(bid_frame, bg=Config.color_bg_card)
        bid_info.pack(fill=tk.X, pady=5)
        
        tk.Label(
            bid_info,
            text="BID (Buy)",
            font=("Segoe UI", 9),
            bg=Config.color_bg_card,
            fg=Config.color_text_secondary,
            width=12,
            anchor="w"
        ).pack(side=tk.LEFT)
        
        self.bid_label = tk.Label(
            bid_info,
            text="87,290.71",
            font=("Segoe UI", 12, "bold"),
            bg=Config.color_bg_card,
            fg=Config.color_positve_num
        )
        self.bid_label.pack(side=tk.LEFT)
        
        ask_info = tk.Frame(bid_frame, bg=Config.color_bg_card)
        ask_info.pack(fill=tk.X, pady=5)
        
        tk.Label(
            ask_info,
            text="ASK (Sell)",
            font=("Segoe UI", 9),
            bg=Config.color_bg_card,
            fg=Config.color_text_secondary,
            width=12,
            anchor="w"
        ).pack(side=tk.LEFT)
        
        self.ask_label = tk.Label(
            ask_info,
            text="87,290.72",
            font=("Segoe UI", 12, "bold"),
            bg=Config.color_bg_card,
            fg=Config.color_negative_num
        )
        self.ask_label.pack(side=tk.LEFT)
        
        spread_info = tk.Frame(bid_frame, bg=Config.color_bg_card)
        spread_info.pack(fill=tk.X, pady=5)
        
        tk.Label(
            spread_info,
            text="Spread",
            font=("Segoe UI", 9),
            bg=Config.color_bg_card,
            fg=Config.color_text_secondary,
            width=12,
            anchor="w"
        ).pack(side=tk.LEFT)
        
        self.spread_label = tk.Label(
            spread_info,
            text="0.0100",
            font=("Segoe UI", 12, "bold"),
            bg=Config.color_bg_card,
            fg=Config.color_text_primary
        )
        self.spread_label.pack(side=tk.LEFT)
        
        volume_container = tk.Frame(self.frame, bg=Config.color_bg_card)
        volume_container.pack(fill=tk.BOTH, expand=True, padx=15, pady=10)
        
        minute_5_frame = tk.Frame(volume_container, bg=Config.color_bg_card)
        minute_5_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=(0, 5))
        
        tk.Label(
            minute_5_frame,
            text="5 Min Volume",
            font=("Segoe UI", 9, "bold"),
            bg=Config.color_bg_card,
            fg=Config.color_text_secondary
        ).pack(anchor="w", pady=(0, 5))
        
        buy_vol_5m = tk.Frame(minute_5_frame, bg=Config.color_bg_card)
        buy_vol_5m.pack(fill=tk.X, pady=2)
        
        tk.Label(
            buy_vol_5m,
            text="Buy:",
            font=("Segoe UI", 8),
            bg=Config.color_bg_card,
            fg=Config.color_positve_num,
            width=5,
            anchor="w"
        ).pack(side=tk.LEFT)
        
        self.buy_vol_label = tk.Label(
            buy_vol_5m,
            text="10.88",
            font=("Segoe UI", 10, "bold"),
            bg=Config.color_bg_card,
            fg=Config.color_text_primary
        )
        self.buy_vol_label.pack(side=tk.LEFT)
        
        sell_vol_5m = tk.Frame(minute_5_frame, bg=Config.color_bg_card)
        sell_vol_5m.pack(fill=tk.X, pady=2)
        
        tk.Label(
            sell_vol_5m,
            text="Sell:",
            font=("Segoe UI", 8),
            bg=Config.color_bg_card,
            fg=Config.color_negative_num,
            width=5,
            anchor="w"
        ).pack(side=tk.LEFT)
        
        self.sell_vol_label = tk.Label(
            sell_vol_5m,
            text="4.55",
            font=("Segoe UI", 10, "bold"),
            bg=Config.color_bg_card,
            fg=Config.color_text_primary
        )
        self.sell_vol_label.pack(side=tk.LEFT)
        
        ratio_vol_5m = tk.Frame(minute_5_frame, bg=Config.color_bg_card)
        ratio_vol_5m.pack(fill=tk.X, pady=2)
        
        tk.Label(
            ratio_vol_5m,
            text="Ratio:",
            font=("Segoe UI", 8),
            bg=Config.color_bg_card,
            fg=Config.color_text_secondary,
            width=5,
            anchor="w"
        ).pack(side=tk.LEFT)
        
        self.ratio_label = tk.Label(
            ratio_vol_5m,
            text="0.705",
            font=("Segoe UI", 10, "bold"),
            bg=Config.color_bg_card,
            fg=Config.color_text_primary
        )
        self.ratio_label.pack(side=tk.LEFT)
        
        #1 hour Volume
        hour_1_frame = tk.Frame(volume_container, bg=Config.color_bg_card)
        hour_1_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=(5, 0))
        
        tk.Label(
            hour_1_frame,
            text="1 Hour Volume",
            font=("Segoe UI", 9, "bold"),
            bg=Config.color_bg_card,
            fg=Config.color_text_secondary
        ).pack(anchor="w", pady=(0, 5))
        
        buy_vol_1h = tk.Frame(hour_1_frame, bg=Config.color_bg_card)
        buy_vol_1h.pack(fill=tk.X, pady=2)
        
        tk.Label(
            buy_vol_1h,
            text="Buy:",
            font=("Segoe UI", 8),
            bg=Config.color_bg_card,
            fg=Config.color_positve_num,
            width=5,
            anchor="w"
        ).pack(side=tk.LEFT)
        
        self.buy_vol_1h_label = tk.Label(
            buy_vol_1h,
            text="125.50",
            font=("Segoe UI", 10, "bold"),
            bg=Config.color_bg_card,
            fg=Config.color_text_primary
        )
        self.buy_vol_1h_label.pack(side=tk.LEFT)
        
        sell_vol_1h = tk.Frame(hour_1_frame, bg=Config.color_bg_card)
        sell_vol_1h.pack(fill=tk.X, pady=2)
        
        tk.Label(
            sell_vol_1h,
            text="Sell:",
            font=("Segoe UI", 8),
            bg=Config.color_bg_card,
            fg=Config.color_negative_num,
            width=5,
            anchor="w"
        ).pack(side=tk.LEFT)
        
        self.sell_vol_1h_label = tk.Label(
            sell_vol_1h,
            text="98.75",
            font=("Segoe UI", 10, "bold"),
            bg=Config.color_bg_card,
            fg=Config.color_text_primary
        )
        self.sell_vol_1h_label.pack(side=tk.LEFT)
        
        ratio_vol_1h = tk.Frame(hour_1_frame, bg=Config.color_bg_card)
        ratio_vol_1h.pack(fill=tk.X, pady=2)
        
        tk.Label(
            ratio_vol_1h,
            text="Ratio:",
            font=("Segoe UI", 8),
            bg=Config.color_bg_card,
            fg=Config.color_text_secondary,
            width=5,
            anchor="w"
        ).pack(side=tk.LEFT)
        
        self.ratio_1h_label = tk.Label(
            ratio_vol_1h,
            text="1.271",
            font=("Segoe UI", 10, "bold"),
            bg=Config.color_bg_card,
            fg=Config.color_text_primary
        )
        self.ratio_1h_label.pack(side=tk.LEFT)
        
    def set_symbol(self, symbol):
        if self.current_symbol == symbol:
            return
        self.stop()
        self.current_symbol = symbol
        self.start()
        
        if self.orderbook_popup and self.orderbook_popup.popup.winfo_exists():
            self.orderbook_popup.order_book.set_symbol(symbol)
        
    def start(self):
        if not self.current_symbol or self.is_active:
            return
        self.is_active = True
        
        ws_url = f"wss://stream.binance.com:9443/ws/{self.current_symbol.lower()}@depth10@100ms"
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
            if data.get('bids') and data.get('asks'):
                bid = float(data['bids'][0][0])
                ask = float(data['asks'][0][0])
                spread = ask - bid
                self.parent.after(0, self.update_display, bid, ask, spread)
        except json.JSONDecodeError:
            print(f"Invalid JSON in spread message")
        except (KeyError, IndexError) as e:
            print(f"Missing data in spread message: {e}")
        except ValueError as e:
            print(f"Invalid number in spread data: {e}")
        except Exception as e:
            print(f"Unexpected error in spread: {e}")
            
    def update_display(self, bid, ask, spread):
        if not self.is_active:
            return
        
        self.bid_label.config(text=f"{bid:,.2f}")
        self.ask_label.config(text=f"{ask:,.2f}")
        self.spread_label.config(text=f"{spread:.4f}")
    
    def on_orderbook_toggle(self, is_on):
        root = self.parent
        while root.master:
            root = root.master
        
        if is_on:
            if not (self.orderbook_popup and self.orderbook_popup.popup.winfo_exists()):
                self.orderbook_popup = OrderBookPopup(root, self.current_symbol)
                self.orderbook_popup.popup.protocol("WM_DELETE_WINDOW", self.on_orderbook_popup_close)
        else:
            if self.orderbook_popup and self.orderbook_popup.popup.winfo_exists():
                self.orderbook_popup.close()
                self.orderbook_popup = None

    def on_orderbook_popup_close(self):
        if self.orderbook_popup:
            self.orderbook_popup.close()
            self.orderbook_popup = None
            self.orderbook_switch.set_state(False)