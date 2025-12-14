import tkinter as tk
import threading
from collections import deque
from config import Config
from utils import safe_api_call

try:
    import matplotlib
    matplotlib.use('TkAgg') #it is Tkinter applications for backend
    from matplotlib.figure import Figure
    from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
    import matplotlib.pyplot as plt
    from matplotlib import style
    mathplotlib_available = True
except ImportError:
    mathplotlib_available = False
    print("Warning: matplotlib not available. Charts will be disabled.")


class CandlestickChart:   
    def __init__(self, parent, is_popup=False):
        self.parent = parent
        self.current_symbol = None
        self.is_active = False
        self.is_popup = is_popup
        self.candles = deque(maxlen=50)
        self.update_thread = None
        
        if not mathplotlib_available:
            self.create_placeholder()
        else:
            self.create_chart()
        
    def create_placeholder(self): #if mathpotlib can't use
        self.frame = tk.Frame(self.parent, bg=Config.color_bg_card)
        tk.Label(
            self.frame,
            text="Candlestick Chart\n(Install matplotlib to enable)",
            font=("Segoe UI", 12),
            bg=Config.color_bg_card,
            fg=Config.color_text_secondary
        ).pack(expand=True)
        
    def create_chart(self): #using mathpotlib
        self.frame = tk.Frame(self.parent, bg=Config.color_bg_card)
        
        style.use('dark_background')
        
        figsize = (14, 8) if self.is_popup else (8, 5) #larger figure
        self.fig = Figure(figsize=figsize, facecolor=Config.color_bg_card)
        
        if not self.is_popup:
            self.ax = self.fig.add_subplot(111)
            self.ax.set_facecolor(Config.color_bg_dark)
            
            self.ax.spines['top'].set_color(Config.color_border)
            self.ax.spines['bottom'].set_color(Config.color_border)
            self.ax.spines['left'].set_color(Config.color_border)
            self.ax.spines['right'].set_color(Config.color_border)
            self.ax.tick_params(colors=Config.color_text_secondary)
        
        self.canvas = FigureCanvasTkAgg(self.fig, self.frame)
        self.canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)
        
    def set_symbol(self, symbol):
        if self.current_symbol == symbol:
            return
        self.stop()
        self.current_symbol = symbol
        self.candles.clear()
        self.start()
        
    def start(self):
        if not self.current_symbol or self.is_active or not mathplotlib_available:
            return
        self.is_active = True
        self.update_thread = threading.Thread(target=self.update_loop, daemon=True)
        self.update_thread.start()
        
    def stop(self):
        self.is_active = False
        
    def update_loop(self):
        while self.is_active:
            url = "https://api.binance.com/api/v3/klines"
            params = {
                "symbol": self.current_symbol.upper(),
                "interval": "1h",
                "limit": 50
            }
            
            data = safe_api_call(url, params=params, retries=3, timeout=10) #call with retry logic
            
            if data:
                try:
                    self.candles.clear()
                    for candle in data:
                        self.candles.append({
                            'time': candle[0],
                            'open': float(candle[1]),
                            'high': float(candle[2]),
                            'low': float(candle[3]),
                            'close': float(candle[4]),
                            'volume': float(candle[5])
                        })
                    self.parent.after(0, self.draw_chart)
                except (KeyError, ValueError, IndexError) as e:
                    print(f"Error parsing candle data: {e}")
            else:
                print(f"Failed to fetch candles for {self.current_symbol}")
                
    def draw_chart(self):
        if not self.is_active or not mathplotlib_available:
            return
        
        if len(self.candles) == 0:
            return
        
        if self.is_popup: #sub plot for pop up
            self.fig.clear()
            gs = self.fig.add_gridspec(2, 1, height_ratios=[3, 1], hspace=0.05)
            ax_candle = self.fig.add_subplot(gs[0])
            ax_volume = self.fig.add_subplot(gs[1], sharex=ax_candle)
        else:
            self.ax.clear()
            ax_candle = self.ax
        
        for i, candle in enumerate(self.candles):
            color = Config.color_positve_num if candle['close'] >= candle['open'] else Config.color_negative_num
            
            body_height = abs(candle['close'] - candle['open'])
            body_bottom = min(candle['open'], candle['close'])
            
            ax_candle.add_patch(plt.Rectangle(
                (i - 0.4, body_bottom),
                0.8,
                body_height if body_height > 0 else candle['close'] * 0.0001,  
                facecolor=color,
                edgecolor=color,
                linewidth=1
            ))
            
            
            ax_candle.plot([i, i], [candle['low'], candle['high']], color=color, linewidth=1.5)
        
        ax_candle.set_xlim(-0.5, len(self.candles) - 0.5)
        ax_candle.set_facecolor(Config.color_bg_dark)
        ax_candle.grid(True, alpha=0.15, color=Config.color_text_secondary, linestyle='--', linewidth=0.5)
        ax_candle.tick_params(colors=Config.color_text_secondary, labelsize=9 if self.is_popup else 8)
        

        for spine in ax_candle.spines.values():
            spine.set_color(Config.color_border)
            spine.set_linewidth(1)
        

        symbol_info = Config.cryptos_all_name_symbol.get(self.current_symbol.upper(), {})
        if self.is_popup:
            title_text = f"{self.current_symbol} 1H Candlestick (Ticking Last Candle)"
            ax_candle.set_title(title_text, color=Config.color_text_primary, fontsize=13, pad=15, fontweight='bold')
        else:
            title_text = f"{symbol_info.get('symbol', self.current_symbol)} 1H Candlestick"
            ax_candle.set_title(title_text, color=Config.color_text_primary, fontsize=11, pad=10)
        
    
        ax_candle.set_ylabel('Price', color=Config.color_text_secondary, fontsize=10 if self.is_popup else 9)
        
        if self.is_popup: # handle volume in x-axis
            ax_candle.tick_params(labelbottom=False) #remove
            
            volumes = [c['volume'] for c in self.candles]
            colors = [Config.color_positve_num if c['close'] >= c['open'] else Config.color_negative_num for c in self.candles]
            
            ax_volume.bar(range(len(volumes)), volumes, color=colors, alpha=0.5, width=0.8, edgecolor='none')
            
            ax_volume.set_facecolor(Config.color_bg_dark)
            ax_volume.grid(True, alpha=0.15, color=Config.color_text_secondary, linestyle='--', linewidth=0.5, axis='y')
            ax_volume.tick_params(colors=Config.color_text_secondary, labelsize=9)
            ax_volume.set_ylabel('Volume', color=Config.color_text_secondary, fontsize=10)
            ax_volume.set_xlabel('Time', color=Config.color_text_secondary, fontsize=10)
            
            for spine in ax_volume.spines.values():
                spine.set_color(Config.color_border)
                spine.set_linewidth(1)
            
            ax_volume.ticklabel_format(style='scientific', axis='y', scilimits=(0,0))
        else:
            ax_candle.set_xlabel('Time', color=Config.color_text_secondary, fontsize=9)
        
        self.fig.tight_layout()
        self.canvas.draw()


class ChartPopup:  
    def __init__(self, parent, symbol):
        self.parent = parent
        self.symbol = symbol
        
        self.popup = tk.Toplevel(parent)
        self.popup.title(f"{symbol} - Full Candlestick Chart")
        self.popup.geometry("1400x800")
        self.popup.configure(bg=Config.color_bg_dark)
        
        header = tk.Frame(self.popup, bg=Config.color_bg_card, height=60)
        header.pack(fill=tk.X)
        header.pack_propagate(False)
        
        symbol_info = Config.cryptos_all_name_symbol.get(symbol, {})
        tk.Label(
            header,
            text=f"{symbol_info.get('name', symbol)} ({symbol_info.get('symbol', symbol)}) - Full Chart View",
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
        
        chart_frame = tk.Frame(self.popup, bg=Config.color_bg_card, highlightthickness=1, highlightbackground=Config.color_border)
        chart_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=(10, 20))
        
        self.chart = CandlestickChart(chart_frame, is_popup=True)
        self.chart.frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        self.chart.set_symbol(symbol)
        
        self.popup.update_idletasks()
        x = (self.popup.winfo_screenwidth() // 2) - (self.popup.winfo_width() // 2)
        y = (self.popup.winfo_screenheight() // 2) - (self.popup.winfo_height() // 2)
        self.popup.geometry(f"+{x}+{y}")
        
        self.popup.protocol('close_window_manager', self.close)
        
    def close(self):
        self.chart.stop()
        self.popup.destroy()