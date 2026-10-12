import os
import requests
from flask import Flask, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

# သင့်ရဲ့ API-Football Key ထည့်ရန်
API_KEY = "9c7229c6da02c8846916bfd3d374a5e2" 
HEADERS = {
    'x-apisports-key': API_KEY
}
BASE_URL = "https://v3.football.api-sports.io/"

# အဓိက လိဂ်များ၏ API-Football IDs
LEAGUES = [
    {"id": 39, "name": "English Premier League"},
    {"id": 140, "name": "Spanish La Liga"},
    {"id": 78, "name": "German Bundesliga"},
    {"id": 135, "name": "Italian Serie A"},
    {"id": 61, "name": "French Ligue 1"}
]

def get_standings(league_id, season=2026):
    """လိဂ်အလိုက် လက်ရှိ အမှတ်ပေးဇယားကို ဆွဲထုတ်ခြင်း"""
    try:
        url = f"{BASE_URL}standings?league={league_id}&season={season}"
        response = requests.get(url, headers=HEADERS, timeout=5)
        if response.status_code == 200:
            data = response.json()
            response_data = data.get('response', [])
            if response_data:
                standings = response_data[0]['league']['standings'][0]
                standings_dict = {}
                for item in standings:
                    team_name = item['team']['name']
                    standings_dict[team_name] = {
                        "position": item['rank'],
                        "points": item['points'],
                        "form": item.get('form', 'N/A')
                    }
                return standings_dict
    except Exception as e:
        print(f"Error fetching standings: {e}")
    return {}

def predict_match_with_standings(home_team, away_team, standings):
    """အမှတ်ပေးဇယား အဆင့်နှင့် ဖောင်ကို အခြေခံ၍ AI ခန့်မှန်းခြင်း"""
    home_stats = standings.get(home_team, {})
    away_stats = standings.get(away_team, {})
    
    home_pos = home_stats.get('position', 10)
    away_pos = away_stats.get('position', 10)
    
    # ဇယားအပေါ်ပိုင်းနှင့် အောက်ပိုင်း အခြေအနေအပေါ် မူတည်ပြီး ခန့်မှန်းချက်ထုတ်ခြင်း
    if home_pos < away_pos:
        score = "2 - 1" if home_pos + 3 < away_pos else "1 - 0"
        h_chance, d_chance, a_chance = "65%", "20%", "15%"
        advice = f"{home_team} (အဆင့် {home_pos}) သည် လက်ရှိဇယားရပ်တည်မှုအသာစီးဖြင့် {away_team} (အဆင့် {away_pos}) ကို ဖိကစားနိုင်ချေရှိသည်။"
    elif home_pos > away_pos:
        score = "1 - 2" if away_pos + 3 < home_pos else "0 - 1"
        h_chance, d_chance, a_chance = "20%", "25%", "55%"
        advice = f"ဇယားအဆင့်ပိုမြင့်နေသည့် ဧည့်သည်အသင်း {away_team} က အဝေးကွင်းတွင် ခြေစွမ်းပြနိုင်ချေရှိသည်။"
    else:
        score = "1 - 1"
        h_chance, d_chance, a_chance = "35%", "40%", "25%"
        advice = f"နှစ်သင်းစလုံး အမှတ်ပေးဇယားတွင် အဆင့်တူနီးပါးရှိနေသဖြင့် အကြိတ်အနယ်ရှိမည့်ပွဲ ဖြစ်သည်။"

    return {
        "predicted_score": score,
        "home_win_chance": h_chance,
        "draw_chance": d_chance,
        "away_win_chance": a_chance,
        "ai_advice": advice
    }

@app.route('/api/matches', methods=['GET'])
def get_matches():
    all_matches = []
    
    try:
        for league in LEAGUES:
            league_id = league['id']
            league_name = league['name']
            
            # ၁။ အမှတ်ပေးဇယား ဆွဲထုတ်ခြင်း
            standings = get_standings(league_id, season=2026)
            
            # ၂။ လိဂ်၏ လာမည့်ပွဲစဉ်များကို ဆွဲထုတ်ခြင်း (လက်ရှိ ၂၀၂၆/၂၀၂၇ ရာသီ)
            url = f"{BASE_URL}fixtures?league={league_id}&season=2026&next=10"
            response = requests.get(url, headers=HEADERS, timeout=5)
            
            if response.status_code == 200:
                data = response.json()
                fixtures = data.get('response', [])
                
                for fixture in fixtures:
                    fixture_id = fixture['fixture']['id']
                    utc_date = fixture['fixture']['date']
                    status = fixture['fixture']['status']['short']
                    
                    home = fixture['teams']['home']['name']
                    away = fixture['teams']['away']['name']
                    
                    # တကယ့် ဒေတာများကို အခြေခံ၍ AI ခန့်မှန်းချက်ထုတ်ခြင်း
                    prediction = predict_match_with_standings(home, away, standings)

                    all_matches.append({
                        "id": fixture_id,
                        "utcDate": utc_date,
                        "status": status,
                        "homeTeam": home,
                        "awayTeam": away,
                        "competition": league_name,
                        "prediction": prediction
                    })

        return jsonify(all_matches)

    except Exception as e:
        return jsonify([])

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)
