import os
import requests
from flask import Flask, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

# ချန်ပီယံလိဂ်၊ ယူရိုပါလိဂ်၊ ကာရာဘောင်းဖလားနှင့် အခြားလိဂ်များပါ ထည့်သွင်းထားသော TheSportsDB ID များ
LEAGUES = [
    {"id": "4328", "name": "English Premier League"},
    {"id": "4335", "name": "Spanish La Liga"},
    {"id": "4331", "name": "German Bundesliga"},
    {"id": "4332", "name": "Italian Serie A"},
    {"id": "4334", "name": "French Ligue 1"},
    {"id": "4344", "name": "Portuguese Primeira Liga"},
    {"id": "4351", "name": "Brazilian Serie A"},
    {"id": "4346", "name": "Dutch Eredivisie"},
    {"id": "4330", "name": "Scottish Premiership"},
    {"id": "4480", "name": "UEFA Champions League"},
    {"id": "4697", "name": "UEFA Europa League"},
    {"id": "4391", "name": "Carabao Cup (League Cup)"}
]

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
    all_matches = []
    
    try:
        for league in LEAGUES:
            url = f"https://www.thesportsdb.com/api/v1/json/3/eventsnextleague.php?id={league['id']}"
            try:
                response = requests.get(url, timeout=5)
                if response.status_code == 200:
                    data = response.json()
                    events = data.get('events', [])
                    
                    if events:
                        for event in events:
                            home = event.get('strHomeTeam', 'Home Team')
                            away = event.get('strAwayTeam', 'Away Team')
                            match_date = event.get('dateEvent', '2026-10-12')
                            match_time = event.get('strTime', '15:00:00')
                            utc_date = f"{match_date}T{match_time}Z"
                            
                            prediction = predict_match(home, away)

                            all_matches.append({
                                "id": event.get('idEvent'),
                                "utcDate": utc_date,
                                "status": event.get('strStatus') or "SCHEDULED",
                                "homeTeam": home,
                                "awayTeam": away,
                                "competition": league['name'],
                                "prediction": prediction
                            })
            except requests.exceptions.RequestException:
                continue

        # အကယ်၍ API မှ ဒေတာ လုံးဝ မရခဲ့ပါက Website မပြိုကျစေရန် နမူနာပွဲစဉ်ပြရန်
        if not all_matches:
            all_matches = [
                {
                    "id": 1,
                    "utcDate": "2026-10-12T18:30:00Z",
                    "status": "SCHEDULED",
                    "homeTeam": "Arsenal",
                    "awayTeam": "Chelsea",
                    "competition": "English Premier League",
                    "prediction": predict_match("Arsenal", "Chelsea")
                }
            ]

        return jsonify(all_matches)

    except Exception as e:
        return jsonify([])

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)
