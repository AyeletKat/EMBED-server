# Hey, here you can use data_mng.merged_df to answer the questions you have and to explore the data.
# To run this, do in the terminal: python data_loader_helper.py

from App.utils.data_manager import DataManager

data_mng = DataManager()

print(data_mng.merged_df.head(1))