import pandas as pd
import math

from src.params.api_params import *


class APIRequest:

    def __init__(self):

        self.data_gw2_url = DATA_GW2_URL
        self.fields = FIELDS
        self.filters = FILTERS
        self.set_query_url(self.fields, self.filters)


    def set_query_url(self, fields, filters):
        """
        basic url building
        """
        field_string =f"fields={','.join(fields)}" 
        filter_string = f"filter={','.join(filters)}"

        self.query_url = f"{self.data_gw2_url}?{field_string}&{filter_string}"

    
    def get_fields(self):
        return self.fields
    

    def set_fields(self, new_fields):
        """
        update fields
        """
        self.fields = new_fields
        self.set_query_url(self, self.fields, self.filters)

    def get_filters(self):
        return self.filters
    

    def set_filters(self, new_filters):
        """
        Update filters
        """
        self.filters = new_filters
        self.set_query_url(self, self.fields, self.filters)

    
    def get_query_url(self):
        return self.query_url


    def read_data(self):
        """
        load data from query with fields and filters
        """
        data = pd.read_csv(self.query_url).fillna(0)

        return data
    

    def value_gold(self, value):

        str_value = str(int(value))

        gold = str_value[:-4] if str_value[:-4] != '' else '00'
        gold = gold if len(gold) >= 2 else f"0{gold}" 
        silver = str_value[-4:-2] if str_value[-4:-2] != '' else '00'
        copper = str_value[-2:]

        gold_value = f"{gold}G {silver}S {copper}C"

        return gold_value


    def calculate_roi(self, sell_price, buy_price):

        if buy_price != 0:
            roi = round((sell_price * 0.85 - buy_price) / buy_price, 4)
        else:
            roi = 0
    
        return roi


    def transform_data(self, data):


        data_transformed = data.copy()
        data_transformed['daily'] = data_transformed['1d_sell_sold'].apply(
            lambda x: math.floor(x * 0.05)
        )
        data_transformed['1d_sell_sold_avg'] = data_transformed['7d_sell_sold'].apply(
            lambda x: math.floor(x / 7) 
        )
        data_transformed['1d_lower_than_7d_avg'] = (data_transformed['1d_sell_sold'] < data_transformed['1d_sell_sold_avg'])

        data_transformed['1d_sell_sold_mod'] = data_transformed.apply(
            lambda row: min(row['1d_sell_sold'], row['1d_sell_sold_avg']),
            axis=1
        )
        data_transformed['daily_mod'] = data_transformed['1d_sell_sold_mod'].apply(
            lambda x: math.floor(x * 0.05)
        )

        data_transformed['profit'] = round(data_transformed['sell_price'] * 0.85 - data_transformed['buy_price'])
        data_transformed['total_profit'] = round(data_transformed['profit'] * data_transformed['daily_mod'])
        data_transformed['total_profit_gold'] = data_transformed['total_profit'].apply(
            lambda x: self.value_gold(x)
        )
        data_transformed['ROI'] = data_transformed.apply(
            lambda row: self.calculate_roi(row['sell_price'], row['buy_price']),
            axis=1
        )

        return data_transformed


    def filter_data(self, data):

        data_transformed = data.copy()

        # el 1day sold menor que una septima parte de 7d sold
        data_filtered = data_transformed[data_transformed['1d_lower_than_7d_avg'] == True]

        # daily_mod > 0
        data_filtered = data_filtered[data_filtered['daily_mod'] > DAILY_MIN]
        # ROI > 10 y < 100
        data_filtered = data_filtered[data_filtered['ROI'] > ROI_MIN]
        data_filtered = data_filtered[data_filtered['ROI'] < ROI_MAX]

        # profit > 10 platas (1000)
        data_filtered = data_filtered[data_filtered['profit'] >= PROFIT_MIN]

        # ordenacion
        data_filtered = data_filtered.sort_values('ROI', ascending=False)

        return data_filtered


