import pandas as pd

df = pd.read_json('anvisa/result.json')

df.to_excel('result.xlsx', index=False)

print('arquivo gerado')
