import json

import requests

url = "https://sirekap-obj-data.kpu.go.id/pemilu/hhcw/ppwp/14.json"
response = requests.get(url)

# Pastikan bahwa permintaan berhasil
if response.status_code == 200:
    data = response.json()
    
    # Membuat file HTML
    with open('output.html', 'w') as f:
        f.write('<html>\n<body>\n')
        
        # Membuat tabel untuk setiap kunci dalam data
        for key in data.keys():
            f.write('<h1>{}</h1>\n'.format(key))
            f.write('<table border="1">\n')
            
            # Jika nilai adalah dictionary, buat baris dan kolom untuk setiap item
            if isinstance(data[key], dict):
                for sub_key in data[key].keys():
                    f.write('<tr>\n')
                    f.write('<td>{}</td>\n'.format(sub_key))
                    f.write('<td>{}</td>\n'.format(data[key][sub_key]))
                    f.write('</tr>\n')
            
            # Jika nilai bukan dictionary, cukup tulis nilai tersebut
            else:
                f.write('<tr>\n')
                f.write('<td>{}</td>\n'.format(data[key]))
                f.write('</tr>\n')
            
            f.write('</table>\n')
        
        f.write('</body>\n</html>')
else:
    print("Gagal mendapatkan data dari URL.")
