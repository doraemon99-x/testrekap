import json
import os

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
    
    # Ganti '100025' dengan 'Anis'
    for i, label in enumerate(labels):
        if label == '100025':
            labels[i] = 'H. ANIES RASYID'
        if label == '100026':
            labels[i] = 'H. PRABOWO SUBIANTO'
        if label == '100027':
            labels[i] = 'H. GANJAR PRANOWO'
    
    # Buat diagram pie
    fig = go.Figure(data=[go.Pie(labels=labels, values=values)])
    
    # Simpan diagram sebagai gambar PNG
    if not os.path.exists("images"):
        os.mkdir("images")
    fig.write_image("images/fig1.png")

    # Buat file HTML dan masukkan gambar ke dalamnya
    with open('chart.html', 'w') as f:
        f.write('<html>\n<body>\n')
        f.write('<img src="images/fig1.png" alt="Pie Chart">\n')
        f.write('</body>\n</html>')
else:
    print("Gagal mendapatkan data dari URL.")
