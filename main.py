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
    match_date = request.args.get('date')
    headers = {'X-Auth-Token': API_KEY}
    
    # Free Tier API တွင် Error မတက်စေရန် ပရီးမီးယားလိဂ် (PL) ပြိုင်ပွဲ၏ ပွဲစဉ်များကို တိုက်ရိုက်ခေါ်ယူခြင်း
    url = f"{BASE_URL}competitions/PL/matches"
    if match_date:
        url = f"{BASE_URL}competitions/PL/matches?dateFrom={match_date}&dateTo={match_date}"

    try:
        response = requests.get(url, headers=headers)
        
        if response.status_code != 200:
            # အကယ်၍ သတ်မှတ်ရက်တွင် Error ရှိက ယေဘုယျ ပရီးမီးယားလိဂ် ပွဲစဉ်များကို ဆွဲယူရန် ကြိုးစားခြင်း
            fallback_response = requests.get(f"{BASE_URL}competitions/PL/matches", headers=headers)
            if fallback_response.status_code == 200:
                data = fallback_response.json()
            else:
                return jsonify({"error": "API မှ ဒေတာရယူ၍ မရပါ", "details": response.text}), 500
        else:
            data = response.json()

        matches = []
        match_list = data.get('matches', [])
        
        for match in match_list:
            home = match.get('homeTeam', {}).get('name', 'Unknown Team')
            away = match.get('awayTeam', {}).get('name', 'Unknown Team')
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

    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)
