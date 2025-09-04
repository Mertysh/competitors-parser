from collections import defaultdict
from os.path import isfile
from os import remove
from io import BytesIO
from datetime import datetime, timedelta

from pandas import DataFrame, read_excel, concat, ExcelWriter, NA
import numpy as np    



def table():
    if isfile(f'./data/table.xlsx') == True:
            table_df = read_excel(f'./data/table.xlsx')

            output = BytesIO()
            writer = ExcelWriter(output, engine='xlsxwriter')
            table_df.to_excel(writer, index=False)

            writer.close()
            file = output.getvalue()

            return file
    