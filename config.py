class Config:
    # colors to style this dashboard
    color_bg_dark = "#1a1d29"
    color_bg_sidebar = "#0f1116"
    color_bg_card = "#252836"
    color_bg_header = "#2d3142"
    color_bg_row = "#1e2132"
    word_accent_color = "#3b82f6"
    color_positve_num = "#10b981"
    color_negative_num = "#ef4444"
    color_text_primary = "#f1f5f9"
    color_text_secondary = "#94a3b8"
    color_border = "#334155"
    color_hover = "#1e293b"
    
    # All crypto that we want to show
    cryptos_all_name_symbol = {
        "BTCUSDT": {"name": "Bitcoin", "symbol": "BTC"},
        "ETHUSDT": {"name": "Ethereum", "symbol": "ETH"},
        "SOLUSDT": {"name": "Solana", "symbol": "SOL"},
        "BNBUSDT": {"name": "Binance Coin", "symbol": "BNB"},
        "XRPUSDT": {"name": "Ripple", "symbol": "XRP"} #if want to add other bid coin in dashboard put it at here next time
    }