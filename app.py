from flask import Flask, request, jsonify, redirect
import uuid
import requests
from datetime import datetime

app = Flask(__name__)
links = {}

@app.route('/')
def home():
    return 'Aplikasi Tracking URL Flask aktif! 🎯'

@app.route('/generate', methods=['POST'])
def generate_link():
    original_url = request.json['url']
    tracking_id = str(uuid.uuid4())
    tracking_link = request.host_url.rstrip('/') + f"/track/{tracking_id}"
    links[tracking_id] = original_url
    return jsonify({'tracking_link': tracking_link})

@app.route('/track/<tracking_id>')
def track_link(tracking_id):
    original_url = links.get(tracking_id)
    if original_url:
        user_ip = request.headers.get('X-Forwarded-For', request.remote_addr)
        try:
            location = requests.get(f'https://ipinfo.io/{user_ip}/json').json()
            city = location.get('city', 'Unknown')
            region = location.get('region', 'Unknown')
            country = location.get('country', 'Unknown')
            org = location.get('org', 'Unknown')
        except:
            city = region = country = org = 'Unknown'

        waktu = datetime.now()
        print("🔍 Klik Terdeteksi")
        print(f"Waktu    : {waktu}")
        print(f"IP       : {user_ip}")
        print(f"Lokasi   : {city}, {region}, {country}")
        print(f"Provider : {org}")
        print(f"URL      : {original_url}")
        print("---------------")

        return redirect(original_url)
    return "Link not found", 404

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
