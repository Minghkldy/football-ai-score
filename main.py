import os
import requests
from flask import Flask, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

# TheSportsDB တွင် ရရှိနိုင်သော ကမ္ဘာတစ်ဝှမ်းမှ လိဂ်များနှင့် ဖလားပြိုင်ပွဲများ အားလုံး
LEAGUES = [
    {"id": "4328", "name": "English Premier League"},
    {"id": "4335", "name": "Spanish La Liga"},
    {"id": "4331", "name": "German Bundesliga"},
    {"id": "4332", "name": "Italian Serie A"},
    {"id": "4334", "name": "French Ligue 1"},
    {"id": "4344", "name": "Portuguese Primeira Liga"},
    {"id": "4351", "name": "Brazilian Serie A"},
    {"id": "4330", "name": "Scottish Premiership"},
    {"id": "4346", "name": "Dutch Eredivisie"},
    {"id": "4480", "name": "UEFA Champions League"},
    {"id": "4697", "name": "UEFA Europa League"},
    {"id": "4356", "name": "Australian A-League"},
    {"id": "4340", "name": "Greek Super League"},
    {"id": "4337", "name": "Mexican Liga MX"},
    {"id": "4359", "name": "Chinese Super League"},
    {"id": "4354", "name": "Argentine Primera División"},
    {"id": "4363", "name": "Polish Ekstraklasa"},
    {"id": "4358", "name": "Turkish Super Lig"},
    {"id": "4339", "name": "Belgian Pro League"},
    {"id": "4353", "name": "Danish Superliga"},
    {"id": "4361", "name": "Swiss Super League"},
    {"id": "4362", "name": "Swedish Allsvenskan"},
    {"id": "4355", "name": "Japanese J1 League"},
    {"id": "4422", "name": "Copa Libertadores"}
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
    seen_match_ids = set()
    
    try:
        for league in LEAGUES:
            url = f"https://www.thesportsdb.com/api/v1/json/3/eventsnextleague.php?id={league['id']}"
            try:
                response = requests.get(url, timeout=4)
                if response.status_code == 200:
                    data = response.json()
                    events = data.get('events', [])
                    
                    if events:
                        for event in events:
                            event_id = event.get('idEvent')
                            if not event_id or event_id in seen_match_ids:
                                continue
                                
                            home = event.get('strHomeTeam', '')
                            away = event.get('strAwayTeam', '')
                            
                            # အမှိုက်အချက်အလက်များ သို့မဟုတ် အခြားအားကစားနည်းများ ပါမလာစေရန် စစ်ထုတ်ခြင်း
                            if not home or not away or "Rams" in home or "Bills" in home or "Miami" in home:
                                continue

                            match_date = event.get('dateEvent', '')
                            match_time = event.get('strTime', '15:00:00')
                            if not match_date:
                                continue
                                
                            utc_date = f"{match_date}T{match_time}Z"
                            seen_match_ids.add(event_id)
                            prediction = predict_match(home, away)

                            all_matches.append({
                                "id": event_id,
                                "utcDate": utc_date,
                                "status": event.get('strStatus') or "SCHEDULED",
                                "homeTeam": home,
                                "awayTeam": away,
                                "competition": league['name'],
                                "prediction": prediction
                            })
            except requests.exceptions.RequestException:
                continue

        return jsonify(all_matches)

    except Exception as e:
        return jsonify([])

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)
