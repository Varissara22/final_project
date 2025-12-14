import sys
sys.dont_write_bytecode = True

import tkinter as tk
from tkinter import ttk
from config import Config
from utils import save_preferences, load_preferences
from components import (
    PriceTickerCard,
    CandlestickChart,
    RecentTradesPanel,
    BidAskSpreadPanel,
    ChartPopup,
)

class FinalIntegratedDashboard: 
    def __init__(self, root):
        self.root = root

        prefs = load_preferences()
        if prefs:
            self.current_symbol = prefs.get('selected_crypto', "BTCUSDT")
            geometry = prefs.get('window_geometry', "1400x900")
        else:
            self.current_symbol = "BTCUSDT"
            geometry = "1400x900"
        
        self.root.title(f"Real-Time Binance Dashboard - {self.current_symbol}")
        self.root.geometry(geometry)
        self.root.minsize(1200, 800)
        self.root.configure(bg=Config.color_bg_dark)
        
        self.chart_popup = None  
        
        self.create_ui()
        
        self.update_dropdown_selection()
        
    def create_ui(self):
        top_bar = tk.Frame(self.root, bg=Config.color_bg_card, height=70)
        top_bar.pack(fill=tk.X)
        top_bar.pack_propagate(False)
        
        logo_frame = tk.Frame(top_bar, bg=Config.color_bg_card)
        logo_frame.pack(side=tk.LEFT, padx=20)
        
        tk.Label(
            logo_frame,
            text="📊",
            font=("Segoe UI", 24),
            bg=Config.color_bg_card
        ).pack(side=tk.LEFT, padx=(0, 10))
        
        title_frame = tk.Frame(logo_frame, bg=Config.color_bg_card)
        title_frame.pack(side=tk.LEFT)
        
        self.title_label = tk.Label(
            title_frame,
            text=f"{self.current_symbol} Dashboard",
            font=("Segoe UI", 16, "bold"),
            bg=Config.color_bg_card,
            fg=Config.color_text_primary
        )
        self.title_label.pack(anchor="w")
        
        selector_frame = tk.Frame(top_bar, bg=Config.color_bg_card)
        selector_frame.pack(side=tk.RIGHT, padx=20)
        
        tk.Label(
            selector_frame,
            text="Select Crypto:",
            font=("Segoe UI", 10),
            bg=Config.color_bg_card,
            fg=Config.color_text_secondary
        ).pack(side=tk.LEFT, padx=(0, 10))
        
        style = ttk.Style()
        style.theme_use('default')
        style.configure(
            'Custom.TCombobox',
            fieldbackground=Config.color_bg_dark,
            background=Config.word_accent_color,
            foreground=Config.color_text_primary,
            arrowcolor=Config.color_text_primary
        )
        
        crypto_names = [f"{info['name']} ({info['symbol']})" for info in Config.cryptos_all_name_symbol.values()]
        
        info = Config.cryptos_all_name_symbol[self.current_symbol]
        default_display = f"{info['name']} ({info['symbol']})"
        self.crypto_var = tk.StringVar(value=default_display)
        
        self.crypto_selector = ttk.Combobox(
            selector_frame,
            textvariable=self.crypto_var,
            values=crypto_names,
            state="readonly",
            width=20,
            font=("Segoe UI", 10),
            style='Custom.TCombobox'
        )
        self.crypto_selector.pack(side=tk.LEFT)
        self.crypto_selector.bind('<<ComboboxSelected>>', self.on_crypto_change)
        
        ticker_bar = tk.Frame(self.root, bg=Config.color_bg_dark, height=110)
        ticker_bar.pack(fill=tk.X, padx=10, pady=(10, 0))
        ticker_bar.pack_propagate(False)
        
        self.ticker_cards = {}
        symbols = ["BTCUSDT", "ETHUSDT", "SOLUSDT", "BNBUSDT", "XRPUSDT"]
        
        for i, symbol in enumerate(symbols):
            info = Config.cryptos_all_name_symbol[symbol]
            card = PriceTickerCard(ticker_bar, symbol, f"{info['symbol']}/USDT")
            card.frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=5)
            card.start()
            self.ticker_cards[symbol] = card
        
        main_container = tk.Frame(self.root, bg=Config.color_bg_dark)
        main_container.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        left_side = tk.Frame(main_container, bg=Config.color_bg_dark)
        left_side.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=(0, 5))
        
        chart_container = tk.Frame(left_side, bg=Config.color_bg_card, highlightthickness=1, highlightbackground=Config.color_border)
        chart_container.pack(fill=tk.BOTH, expand=True)
        
        chart_header = tk.Frame(chart_container, bg=Config.color_bg_card)
        chart_header.pack(fill=tk.X, padx=10, pady=8)
        
        tk.Label(
            chart_header,
            text="Price Chart",
            font=("Segoe UI", 11, "bold"),
            bg=Config.color_bg_card,
            fg=Config.color_text_primary
        ).pack(side=tk.LEFT)
        
        import sys
        import os
        sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
        from toggle_switch import ToggleSwitch

        self.full_chart_switch = ToggleSwitch(
            chart_header,
            width=110,
            height=32,
            bg_on="#3b82f6",
            bg_off="#6b7280",
            text_on="CLOSE",
            text_off="Full Chart",
            command=self.on_chart_toggle
        )
        self.full_chart_switch.pack(side=tk.RIGHT, padx=5)
        
        chart_frame = tk.Frame(chart_container, bg=Config.color_bg_card)
        chart_frame.pack(fill=tk.BOTH, expand=True)
        
        self.chart = CandlestickChart(chart_frame, is_popup=False)
        self.chart.frame.pack(fill=tk.BOTH, expand=True)
        self.chart.set_symbol(self.current_symbol)
        
        right_side = tk.Frame(main_container, bg=Config.color_bg_dark, width=550)
        right_side.pack(side=tk.LEFT, fill=tk.BOTH, padx=(5, 0))
        right_side.pack_propagate(False)
        
        spread_frame = tk.Frame(right_side, bg=Config.color_bg_card, highlightthickness=1, highlightbackground=Config.color_border, height=310)
        spread_frame.pack(fill=tk.X, expand=False, pady=(0, 10))
        spread_frame.pack_propagate(False)
        
        self.spread_panel = BidAskSpreadPanel(spread_frame)
        self.spread_panel.frame.pack(fill=tk.BOTH, expand=True)
        self.spread_panel.set_symbol(self.current_symbol)
        
        trades_frame = tk.Frame(right_side, bg=Config.color_bg_card, highlightthickness=1, highlightbackground=Config.color_border)
        trades_frame.pack(fill=tk.BOTH, expand=True)
        
        self.trades_panel = RecentTradesPanel(trades_frame)
        self.trades_panel.frame.pack(fill=tk.BOTH, expand=True)
        self.trades_panel.set_symbol(self.current_symbol)
    
    def update_dropdown_selection(self):
        if self.current_symbol in Config.cryptos_all_name_symbol:
            info = Config.cryptos_all_name_symbol[self.current_symbol]
            display_name = f"{info['name']} ({info['symbol']})"
            self.crypto_var.set(display_name)
    
    def on_chart_toggle(self, is_on):
        if is_on:
            if not (self.chart_popup and self.chart_popup.popup.winfo_exists()):
                self.chart_popup = ChartPopup(self.root, self.current_symbol)
                self.chart_popup.popup.protocol("WM_DELETE_WINDOW", self.on_chart_popup_close)
        else:
            if self.chart_popup and self.chart_popup.popup.winfo_exists():
                self.chart_popup.close()
                self.chart_popup = None
    
    def on_chart_popup_close(self):
        if self.chart_popup:
            self.chart_popup.close()
            self.chart_popup = None
            self.full_chart_switch.set_state(False)
        
    def on_crypto_change(self, event): 
        selected = self.crypto_var.get()
        
        for symbol, info in Config.cryptos_all_name_symbol.items():
            if f"{info['name']} ({info['symbol']})" == selected:
                self.current_symbol = symbol
                break
        
        info = Config.cryptos_all_name_symbol[self.current_symbol]
        self.title_label.config(text=f"{self.current_symbol} Dashboard")
        self.root.title(f"Real-Time Binance Dashboard - {self.current_symbol}")
        
        self.chart.set_symbol(self.current_symbol)
        self.spread_panel.set_symbol(self.current_symbol)
        self.trades_panel.set_symbol(self.current_symbol)
        
        if self.chart_popup and self.chart_popup.popup.winfo_exists():
            self.chart_popup.chart.set_symbol(self.current_symbol)
        
    def on_closing(self):
        print("Closing dashboard")
        
        geometry = self.root.geometry()
        save_preferences(self.current_symbol, geometry)
        
        if self.chart_popup and self.chart_popup.popup.winfo_exists():
            self.chart_popup.close()
        
        for card in self.ticker_cards.values():
            card.stop()
        
        self.chart.stop()
        self.spread_panel.stop()
        self.trades_panel.stop()
        
        self.root.destroy()

    
def main():
    root = tk.Tk()
    app = FinalIntegratedDashboard(root)
    root.protocol("WM_DELETE_WINDOW", app.on_closing)
    
    try:
        root.mainloop()
    except KeyboardInterrupt:
        print("\nShutting down")
        app.on_closing()


if __name__ == "__main__":
    main()