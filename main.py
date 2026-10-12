import os
import requests
from flask import Flask, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

API_KEY = "4e8538ba274a14e60a063277b1bcc2253"
BASE_URL = "https://api.football-data.org/v4/"

def predict_match(home_team, away_team):
    return {
        "predicted_score": "2 - 1",
        "home_win_chance": "55%",
        "draw_chance": "25%",
        "away_win_chance": "20%",
        "ai_advice": f"{home_team} သည် အိမ်ကွင်းတွင် ခြေစွမ်းပိုမို သာလွန်နေပါသည်။"
    }

@app.route('/api/matches', methods=['GET'])
def get_matches():
    headers = {'X-Auth-Token': API_KEY}
    # လက်ရှိ သို့မဟုတ် လာမည့်ပွဲစဉ်များကို ဆွဲထုတ်ခြင်း
    response = requests.get(f"{BASE_URL}matches", headers=headers)
    
    if response.status_code != 200:
        return jsonify({"error": "Data ဆွဲယူ၍ မရပါ", "details": response.text}), 500

    data = response.json()
    matches = []

    # matches ဆိုတဲ့ Key ပါမပါ စစ်ဆေးပြီးမှ loop ပတ်ရန်
    match_list = data.get('matches', [])
    for match in match_list[:5]:
        home = match.get('homeTeam', {}).get('name', 'Home Team')
        away = match.get('awayTeam', {}).get('name', 'Away Team')
        prediction = predict_match(home, away)

        matches.append({
            "id": match.get('id'),
            "utcDate": match.get('utcDate'),
            "status": match.get('status'),
            "homeTeam": home,
            "awayTeam": away,
            "prediction": prediction
        })

    return jsonify(matches)

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)
