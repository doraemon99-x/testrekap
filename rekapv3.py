import json

import matplotlib.pyplot as plt
import requests

url = "https://sirekap-obj-data.kpu.go.id/pemilu/hhcw/ppwp/14.json"
response = requests.get(url)

# Pastikan bahwa permintaan berhasil
if response.status_code == 200:
    data = response.json()
    
    # Ambil data untuk diagram pie
    chart_data = data['chart']
    labels = list(chart_data.keys())
    sizes = list(chart_data.values())
    
    # Buat diagram pie
    fig1, ax1 = plt.subplots()
    ax1.pie(sizes, labels=labels, autopct='%1.1f%%', startangle=90)
    ax1.axis('equal')  # Equal aspect ratio ensures that pie is drawn as a circle.

    plt.show()
else:
    print("Gagal mendapatkan data dari URL.")
