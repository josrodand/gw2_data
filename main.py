import numpy as np
import pandas as pd
import math

import matplotlib.pyplot as plt
import seaborn as sns

from src.params.api_params import *
from src.data_gathering import APIRequest

if __name__ == "__main__":
    api_request = APIRequest()

    data = api_request.read_data()
    data_transformed = api_request.transform_data(data)
    data_filtered = api_request.filter_data(data_transformed)

    data_filtered.to_excel("data.xlsx", index=False)