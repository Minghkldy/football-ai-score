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
    try:
        headers = {'X-Auth-Token': API_KEY}
        response = requests.get(f"{BASE_URL}matches", headers=headers)
        
        if response.status_code != 200:
            # API Error ဖြစ်ခဲ့လျှင် Dummy Data (နမူနာပွဲစဉ်) ပြန်ပေးရန် (Website မပြိုကျစေရန်)
            dummy_matches = [
                {
                    "id": 1,
                    "utcDate": "2026-10-12T15:00:00Z",
                    "status": "SCHEDULED",
                    "homeTeam": "Arsenal",
                    "awayTeam": "Chelsea",
                    "prediction": predict_match("Arsenal", "Chelsea")
                },
                {
                    "id": 2,
                    "utcDate": "2026-10-12T17:30:00Z",
                    "status": "SCHEDULED",
                    "homeTeam": "Manchester City",
                    "awayTeam": "Liverpool",
                    "prediction": predict_match("Manchester City", "Liverpool")
                }
            ]
            return jsonify(dummy_matches)

        data = response.json()
        matches = []
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
            
        if not matches:
            # ပွဲစဉ် မရှိသေးပါကလည်း နမူနာပြရန်
            matches = [
                {
                    "id": 1,
                    "utcDate": "2026-10-12T15:00:00Z",
                    "status": "SCHEDULED",
                    "homeTeam": "Arsenal",
                    "awayTeam": "Chelsea",
                    "prediction": predict_match("Arsenal", "Chelsea")
                }
            ]

        return jsonify(matches)
    except Exception as e:
        # ဘယ်လို Error တက်တက် Website မှာ စာရင်းပေါ်လာစေရန် Safe Fallback
        return jsonify([
            {
                "id": 1,
                "utcDate": "2026-10-12T15:00:00Z",
                "status": "SCHEDULED",
                "homeTeam": "Manchester United",
                "awayTeam": "Tottenham",
                "prediction": predict_match("Manchester United", "Tottenham")
            }
        ])

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)
