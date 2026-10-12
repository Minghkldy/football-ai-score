import os
import requests
from flask import Flask, jsonify, request
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
    # Frontend ကနေ ပို့လိုက်တဲ့ နေ့ရက် (Date) ကို ဖမ်းယူခြင်း (မပါလာရင် ယနေ့ရက်စွဲကို ယူမည်)
    match_date = request.args.get('date')
    
    headers = {'X-Auth-Token': API_KEY}
    
    # Football-Data.org API တွင် သတ်မှတ်ထားသော နေ့ရက်အလိုက် ပွဲစဉ်တောင်းဆိုခြင်း
    url = f"{BASE_URL}matches"
    if match_date:
        url = f"{BASE_URL}matches?dateFrom={match_date}&dateTo={match_date}"

    response = requests.get(url, headers=headers)
    
    if response.status_code != 200:
        return jsonify({"error": "Data ဆွဲယူ၍ မရပါ"}), 500

    data = response.json()
    matches = []
    match_list = data.get('matches', [])
    
    for match in match_list:
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
