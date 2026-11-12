import pandas as pd
import sys

if len(sys.argv) < 2:
    raise Exception('1 command line argument required: python index.py <csv-path>')

#load csv
path = sys.argv[1]
df = pd.read_csv(path)

#preserve column if its actually body data
df.loc[-1] = df.columns[0]
df.index = df.index + 1
df = df.sort_index()

#create new df
n_col = df[df.columns[0]].str.count(',').max() + 1
n_rows = len(df)
col_list = df.columns[0].split(',')
new_cols = [col_list[i] if i < len(col_list) else 'empty_' + str(i) for i in range(n_col)]
n_data = df[df.columns[0]].str.split(',').loc[1:].reset_index()[df.columns[0]]
ndf = pd.DataFrame(columns=new_cols)

#inset data
for i in n_data.index:
    row = n_data.iloc[i]
    diff = n_col - len(row) 
    row += ['' for j in range(diff)]
    ndf.loc[i] = row

#save
output_path = path.replace('.csv', '_fixed.csv')
ndf.to_csv(output_path)
print('saved to ' + output_path)
