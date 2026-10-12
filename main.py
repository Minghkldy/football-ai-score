import os
import requests
from flask import Flask, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

# TheSportsDB API (English Premier League အတွက် Free Endpoint - ID: 4328)
LEAGUE_URL = "https://www.thesportsdb.com/api/v1/json/3/eventsnextleague.php?id=4328"

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
        response = requests.get(LEAGUE_URL)
        
        if response.status_code != 200:
            return jsonify({"error": "Data ဆွဲယူ၍ မရပါ"}), 500

        data = response.json()
        events = data.get('events', [])
        matches = []

        if not events:
            # ပွဲစဉ် မရှိသေးပါက နမူနာပြရန်
            return jsonify([
                {
                    "id": 1,
                    "utcDate": "2026-10-12T15:00:00Z",
                    "status": "SCHEDULED",
                    "homeTeam": "Arsenal",
                    "awayTeam": "Chelsea",
                    "prediction": predict_match("Arsenal", "Chelsea")
                }
            ])

        for event in events:
            home = event.get('strHomeTeam', 'Home Team')
            away = event.get('strAwayTeam', 'Away Team')
            match_date = event.get('dateEvent', '2026-10-12')
            match_time = event.get('strTime', '15:00:00')
            utc_date = f"{match_date}T{match_time}Z"
            
            prediction = predict_match(home, away)

            matches.append({
                "id": event.get('idEvent'),
                "utcDate": utc_date,
                "status": event.get('strStatus') or "SCHEDULED",
                "homeTeam": home,
                "awayTeam": away,
                "prediction": prediction
            })

        return jsonify(matches)

    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)
