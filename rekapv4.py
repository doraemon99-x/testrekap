import json

import plotly.graph_objects as go
import requests

url = "https://sirekap-obj-data.kpu.go.id/pemilu/hhcw/ppwp/14.json"
response = requests.get(url)

# Pastikan bahwa permintaan berhasil
if response.status_code == 200:
    data = response.json()
    
    # Ambil data untuk diagram pie
    chart_data = data['chart']
    labels = list(chart_data.keys())
    values = list(chart_data.values())
    
    # Buat diagram pie
    fig = go.Figure(data=[go.Pie(labels=labels, values=values)])
    
    # Tulis diagram sebagai HTML ke file
    fig.write_html("file.html")
else:
    print("Gagal mendapatkan data dari URL.")

