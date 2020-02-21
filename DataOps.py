import pandas as pd

dataFrame = pd.read_csv("scimago_categories_then_areas.csv")
dataFrame = dataFrame.drop(columns= ['Code'])
dataFrame = dataFrame.drop(index =[0,1])
dataFrame = dataFrame.reset_index()
dataFrame = dataFrame.drop(columns = ['index'])
dataFrame.columns = ['Subcategory', 'Category']
dataFrame = dataFrame[['Category', 'Subcategory']]
prev = dataFrame['Category'][0]
new_dict = {}
sub_category_list = []
count = 0 
for index in dataFrame.index: 
    current=dataFrame['Category'][index]
    if (current == prev):
        sub_category_list.append(dataFrame['Subcategory'][index])
        count +=1
    else:
        new_dict[prev] = sub_category_list
        sub_category_list.clear()
        sub_category_list.append(dataFrame['Subcategory'][index])

    prev = current   
new_dict[prev] = sub_category_list
df = pd.DataFrame(new_dict)
set1 = set(list(dataFrame['Category']))
set2 = set(list(df.columns))
intersection = set1.intersection(set2)
difference = set1.difference(set2)
print (df.columns)