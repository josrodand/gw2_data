DATA_GW2_URL = 'https://api.datawars2.ie/gw2/v1/items/csv'


FIELDS = [
    'id', 
    'name',
    'name_es',
    'type',
    'rarity',
    'buy_quantity',
    'buy_price',
    'sell_quantity',
    'sell_price',
    '7d_buy_sold',
    '7d_sell_sold',
    '1d_buy_sold',
    '1d_sell_sold',
    'lastUpdate'
]

FILTERS = [
    ''
]


ROI_MIN = 0.1
ROI_MAX = 1
DAILY_MIN = 0
PROFIT_MIN = 1000



COLUMNS_SELECTED = [
    'id', 
    'name', 
    'type', 
    'rarity', 
    'buy_quantity', 
    'buy_price',
    'sell_quantity', 
    'sell_price', 
    '7d_buy_sold', 
    '7d_sell_sold',
    '1d_buy_sold', 
    '1d_sell_sold', 
    'lastUpdate', 
    # 'daily',
    # '1d_sell_sold_avg', 
    # '1d_lower_than_7d_avg', 
    # '1d_sell_sold_mod', 
    'daily_mod',
    'profit', 
    'total_profit', 
    'ROI'
]