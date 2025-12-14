import tkinter as tk
from tkinter import ttk
import websocket
import json
import threading
from config import Config

class OrderBookPanel:
    def __init__(self, parent):
        self.parent = parent
        self.current_symbol = None
        self.is_active = False
        self.ws = None
        
        self.create_ui()
        
    def create_ui(self):
        self.frame = tk.Frame(self.parent, bg=Config.color_bg_card)
        
        header = tk.Frame(self.frame, bg=Config.color_bg_card)
        header.pack(fill=tk.X, padx=15, pady=10)
        
        tk.Label(
            header,
            text="Order Book Snapshot",
            font=("Segoe UI", 12, "bold"),
            bg=Config.color_bg_card,
            fg=Config.color_text_primary
        ).pack(side=tk.LEFT)
        
        book_frame = tk.Frame(self.frame, bg=Config.color_bg_card)
        book_frame.pack(fill=tk.BOTH, expand=True, padx=15, pady=(0, 15))
        
        asks_header = tk.Frame(book_frame, bg=Config.color_bg_card)
        asks_header.grid(row=0, column=0, sticky="ew", pady=(0, 5))
        
        tk.Label(
            asks_header,
            text="ASKS (Sells - Lowest to Highest Price)",
            font=("Segoe UI", 9, "bold"),
            bg=Config.color_bg_card,
            fg=Config.color_negative_num,
            anchor="w"
        ).pack(fill=tk.X)
        
        asks_cols = tk.Frame(asks_header, bg=Config.color_bg_card)
        asks_cols.pack(fill=tk.X)
        
        tk.Label(
            asks_cols,
            text="Price",
            font=("Segoe UI", 8),
            bg=Config.color_bg_card,
            fg=Config.color_text_secondary,
            width=15,
            anchor="e"
        ).pack(side=tk.LEFT, padx=5)
        
        tk.Label(
            asks_cols,
            text="Amount",
            font=("Segoe UI", 8),
            bg=Config.color_bg_card,
            fg=Config.color_text_secondary,
            width=15,
            anchor="e"
        ).pack(side=tk.LEFT, padx=5)
        
        tk.Label(
            asks_cols,
            text="Total",
            font=("Segoe UI", 8),
            bg=Config.color_bg_card,
            fg=Config.color_text_secondary,
            width=15,
            anchor="e"
        ).pack(side=tk.LEFT, padx=5)
        
        asks_frame = tk.Frame(book_frame, bg=Config.color_bg_card)
        asks_frame.grid(row=1, column=0, sticky="nsew")
        
        self.asks_labels = []
        for i in range(10):
            row_frame = tk.Frame(asks_frame, bg=Config.color_bg_card)
            row_frame.pack(fill=tk.X, pady=1)
            
            price_label = tk.Label(
                row_frame,
                text="---",
                font=("Consolas", 9),
                bg=Config.color_bg_card,
                fg=Config.color_negative_num,
                width=15,
                anchor="e"
            )
            price_label.pack(side=tk.LEFT, padx=5)
            
            amount_label = tk.Label(
                row_frame,
                text="---",
                font=("Consolas", 9),
                bg=Config.color_bg_card,
                fg=Config.color_text_secondary,
                width=15,
                anchor="e"
            )
            amount_label.pack(side=tk.LEFT, padx=5)
            
            total_label = tk.Label(
                row_frame,
                text="---",
                font=("Consolas", 9),
                bg=Config.color_bg_card,
                fg=Config.color_text_secondary,
                width=15,
                anchor="e"
            )
            total_label.pack(side=tk.LEFT, padx=5)
            
            self.asks_labels.append((price_label, amount_label, total_label))
        
        separator = tk.Frame(book_frame, bg=Config.color_border, height=2)
        separator.grid(row=2, column=0, sticky="ew", pady=10)
        
        bids_header = tk.Frame(book_frame, bg=Config.color_bg_card)
        bids_header.grid(row=3, column=0, sticky="ew", pady=(0, 5))
        
        tk.Label(
            bids_header,
            text="BIDS (Buys - Highest to Lowest Price)",
            font=("Segoe UI", 9, "bold"),
            bg=Config.color_bg_card,
            fg=Config.color_positve_num,
            anchor="w"
        ).pack(fill=tk.X)
        
        bids_cols = tk.Frame(bids_header, bg=Config.color_bg_card)
        bids_cols.pack(fill=tk.X)
        
        tk.Label(
            bids_cols,
            text="Price",
            font=("Segoe UI", 8),
            bg=Config.color_bg_card,
            fg=Config.color_text_secondary,
            width=15,
            anchor="e"
        ).pack(side=tk.LEFT, padx=5)
        
        tk.Label(
            bids_cols,
            text="Amount",
            font=("Segoe UI", 8),
            bg=Config.color_bg_card,
            fg=Config.color_text_secondary,
            width=15,
            anchor="e"
        ).pack(side=tk.LEFT, padx=5)
        
        tk.Label(
            bids_cols,
            text="Total",
            font=("Segoe UI", 8),
            bg=Config.color_bg_card,
            fg=Config.color_text_secondary,
            width=15,
            anchor="e"
        ).pack(side=tk.LEFT, padx=5)
        
        bids_frame = tk.Frame(book_frame, bg=Config.color_bg_card)
        bids_frame.grid(row=4, column=0, sticky="nsew")
        
        self.bids_labels = []

        for i in range(10):
            row_frame = tk.Frame(bids_frame, bg=Config.color_bg_card)
            row_frame.pack(fill=tk.X, pady=1)
            
            price_label = tk.Label(
                row_frame,
                text="---",
                font=("Consolas", 9),
                bg=Config.color_bg_card,
                fg=Config.color_positve_num,
                width=15,
                anchor="e"
            )
            price_label.pack(side=tk.LEFT, padx=5)
            
            amount_label = tk.Label(
                row_frame,
                text="---",
                font=("Consolas", 9),
                bg=Config.color_bg_card,
                fg=Config.color_text_secondary,
                width=15,
                anchor="e"
            )
            amount_label.pack(side=tk.LEFT, padx=5)
            
            total_label = tk.Label(
                row_frame,
                text="---",
                font=("Consolas", 9),
                bg=Config.color_bg_card,
                fg=Config.color_text_secondary,
                width=15,
                anchor="e"
            )
            total_label.pack(side=tk.LEFT, padx=5)
            
            self.bids_labels.append((price_label, amount_label, total_label))
            
        book_frame.grid_rowconfigure(1, weight=1)
        book_frame.grid_rowconfigure(4, weight=1)
        book_frame.grid_columnconfigure(0, weight=1)
        
    def set_symbol(self, symbol):
        if self.current_symbol == symbol:
            return
        self.stop()
        self.current_symbol = symbol
        self.start()
        
    def start(self):
        if not self.current_symbol or self.is_active:
            return
        self.is_active = True
        
        symbol_lower = self.current_symbol.lower()
        ws_url = f"wss://stream.binance.com:9443/ws/{symbol_lower}@depth10@100ms"
        
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
            asks = data.get('asks', [])[:10]
            bids = data.get('bids', [])[:10]
            self.parent.after(0, self.update_display, asks, bids)
        except json.JSONDecodeError:
            print(f"Invalid JSON in order book message")
        except KeyError as e:
            print(f"Missing key in order book data: {e}")
        except Exception as e:
            print(f"Unexpected error in order book: {e}")
            
    def update_display(self, asks, bids):
        if not self.is_active:
            return
        
        asks_reversed = list(reversed(asks)) #lowest first
        for i, (price_label, amount_label, total_label) in enumerate(self.asks_labels):
            if i < len(asks_reversed):
                price = float(asks_reversed[i][0])
                amount = float(asks_reversed[i][1])
                total = price * amount
                price_label.config(text=f"{price:,.2f}")
                amount_label.config(text=f"{amount:.6f}")
                total_label.config(text=f"{total:,.2f}")
            else:
                price_label.config(text="---")
                amount_label.config(text="---")
                total_label.config(text="---")
        
        for i, (price_label, amount_label, total_label) in enumerate(self.bids_labels): #highest first
            if i < len(bids):
                price = float(bids[i][0])
                amount = float(bids[i][1])
                total = price * amount
                price_label.config(text=f"{price:,.2f}")
                amount_label.config(text=f"{amount:.6f}")
                total_label.config(text=f"{total:,.2f}")
            else:
                price_label.config(text="---")
                amount_label.config(text="---")
                total_label.config(text="---")


class OrderBookPopup:
    def __init__(self, parent, symbol):
        self.parent = parent
        self.symbol = symbol
        
        self.popup = tk.Toplevel(parent)
        self.popup.title(f"{symbol} - Order Book")
        self.popup.geometry("600x800")
        self.popup.configure(bg=Config.color_bg_dark)
        
        header = tk.Frame(self.popup, bg=Config.color_bg_card, height=60)
        header.pack(fill=tk.X)
        header.pack_propagate(False)
        
        symbol_info = Config.cryptos_all_name_symbol.get(symbol, {})
        tk.Label(
            header,
            text=f"{symbol_info.get('name', symbol)} ({symbol_info.get('symbol', symbol)}) - Order Book",
            font=("Segoe UI", 14, "bold"),
            bg=Config.color_bg_card,
            fg=Config.color_text_primary
        ).pack(side=tk.LEFT, padx=20, pady=15)
        
        close_btn = tk.Button(
            header,
            text="X Close",
            command=self.close,
            font=("Segoe UI", 10),
            bg=Config.color_negative_num,
            fg=Config.color_text_primary,
            activebackground="#dc2626",
            activeforeground=Config.color_text_primary,
            relief="flat",
            cursor="hand2",
            padx=15,
            pady=5
        )
        close_btn.pack(side=tk.RIGHT, padx=20)
        
        book_frame = tk.Frame(self.popup, bg=Config.color_bg_card, highlightthickness=1, highlightbackground=Config.color_border)
        book_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=(10, 20))
        
        self.order_book = OrderBookPanel(book_frame)
        self.order_book.frame.pack(fill=tk.BOTH, expand=True)
        self.order_book.set_symbol(symbol)
        
        self.popup.update_idletasks()
        x = (self.popup.winfo_screenwidth() // 2) - (self.popup.winfo_width() // 2)
        y = (self.popup.winfo_screenheight() // 2) - (self.popup.winfo_height() // 2)
        self.popup.geometry(f"+{x}+{y}")
        
        self.popup.protocol('close_window_manager', self.close)
        
    def close(self):
        self.order_book.stop()
        self.popup.destroy()