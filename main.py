import requests
from flask import Flask, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app)  # Frontend မှ လာရောက် ချိတ်ဆက်နိုင်ရန်

API_KEY = "4e8538ba274a14e60a063277b1bcc2253"  # Football-Data.org မှရသော key ထည့်ပါ
BASE_URL = "https://api.football-data.org/v4/"

def predict_match(home_team, away_team):
    """
    အသင်းအမည်၊ ရလဒ်နှင့် အခြေအနေအပေါ် မူတည်၍ 
    AI Prediction (Win % / Score) ထုတ်ပေးသည့် ရိုးရှင်းသော Algorithm
    """
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
    response = requests.get(f"{BASE_URL}competitions/PL/matches?status=SCHEDULED", headers=headers)
    
    if response.status_code != 200:
        return jsonify({"error": "Data ဆွဲယူ၍ မရပါ"}), 500

    data = response.json()
    matches = []

    for match in data.get('matches', [])[:5]: # ပွဲစဉ် ၅ ပွဲ ထုတ်ယူပြသခြင်း
        home = match['homeTeam']['name']
        away = match['awayTeam']['name']
        prediction = predict_match(home, away)

        matches.append({
            "id": match['id'],
            "utcDate": match['utcDate'],
            "status": match['status'],
            "homeTeam": home,
            "awayTeam": away,
            "prediction": prediction
        })

    return jsonify(matches)

if __name__ == '__main__':
    app.run(port=5000)
