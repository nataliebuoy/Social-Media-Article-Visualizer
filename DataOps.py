import pandas as pd

dataFrame = pd.read_csv("scimago_categories_then_areas.csv")
dataFrame = dataFrame.drop(columns= ['Code'])
dataFrame = dataFrame.drop(index =[0,1])
dataFrame = dataFrame.reset_index()
dataFrame = dataFrame.drop(columns = ['index'])
print (dataFrame.to_string())
