import pandas as pd
import requests

# URL JSON Anda
url = 'https://sirekap-obj-data.kpu.go.id/pemilu/hhcw/ppwp.json'

# Mengambil data JSON dari URL
response = requests.get(url)
data = response.json()

# Mengambil data 'chart' dari data JSON
chart_data = data['chart']

# Mengubah data 'chart' menjadi DataFrame pandas
df = pd.DataFrame([chart_data])

# Menyimpan DataFrame sebagai file CSV
df.to_csv('spreadsheet.csv', index=False)
