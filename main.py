import os
import random
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

# နာမည်ကြီး အသင်းများ (လက်ရှိရာသီ ခြေစွမ်းထက်မြက်သော အသင်းများ)
TOP_TEAMS = [
    "Arsenal", "Manchester City", "Liverpool", "Real Madrid", "Barcelona", 
    "Bayern Munich", "Inter", "AC Milan", "Juventus", "PSG", "Benfica", "Sporting CP",
    "Napoli", "Atletico Madrid", "Bayer Leverkusen", "Borussia Dortmund"
]

def smart_ai_prediction(home_team, away_team):
    """အသင်းများ၏ အနေအထားကို လေ့လာပြီး လက်တွေ့ဆန်သော ရလဒ်နှင့် နိုင်ခြေများကို တွက်ချက်ခြင်း"""
    is_home_top = any(t.lower() in home_team.lower() for t in TOP_TEAMS)
    is_away_top = any(t.lower() in away_team.lower() for t in TOP_TEAMS)
    
    # Random seed ကို အသင်းနာမည်အပေါ် မူတည်စေခြင်းဖြင့် ပွဲစဉ်တိုင်းအတွက် ရလဒ် သီးသန့်ထွက်စေရန်
    seed_val = sum(ord(c) for c in home_team + away_team)
    random.seed(seed_val)
    
    if is_home_top and not is_away_top:
        scores = ["2 - 0", "3 - 1", "3 - 0", "2 - 1"]
        score = random.choice(scores)
        h_chance, d_chance, a_chance = "68%", "20%", "12%"
        advice = f"{home_team} သည် အိမ်ကွင်းအားသာချက်နှင့်အတူ ဧည့်သည် {away_team} ကို ဖိကစားကာ အနိုင်ယူရန် ရေပန်းစားနေသည်။"
    elif not is_home_top and is_away_top:
        scores = ["0 - 2", "1 - 2", "0 - 3", "1 - 3"]
        score = random.choice(scores)
        h_chance, d_chance, a_chance = "20%", "25%", "55%"
        advice = f"အသင်းကြီးဖြစ်သည့် {away_team} က အဝေးကွင်းဖြစ်သော်လည်း တိုက်စစ်ပိုင်း အသာစီးဖြင့် ရလဒ်ဖော်ဆောင်နိုင်ချေရှိသည်။"
    elif is_home_top and is_away_top:
        scores = ["1 - 1", "2 - 2", "2 - 1", "1 - 2"]
        score = random.choice(scores)
        h_chance, d_chance, a_chance = "40%", "35%", "25%"
        advice = f"ဥရောပထိပ်တန်းအသင်းနှစ်သင်း ထိပ်တိုက်တွေ့ဆုံမှုဖြစ်၍ အကြိတ်အနယ်ရှိပြီး ဂိုးရလဒ် အပြန်အလှန် ထွက်ပေါ်လာနိုင်ပါသည်။"
    else:
        scores = ["1 - 0", "0 - 1", "1 - 1", "0 - 0"]
        score = random.choice(scores)
        h_chance, d_chance, a_chance = "45%", "35%", "20%"
        advice = f"နှစ်သင်း၏ ခြေစွမ်းနီးစပ်သဖြင့် အိမ်ကွင်းဧည့်ကွင်း ရုန်းကန်ရမည့်ပွဲဖြစ်ပြီး အမှားနည်းသူ အနိုင်ရရှိသွားပါမည်။"

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
                            
                            if not home or not away or "Rams" in home or "Bills" in home or "Miami" in home:
                                continue

                            match_date = event.get('dateEvent', '')
                            match_time = event.get('strTime', '15:00:00')
                            if not match_date:
                                continue
                                
                            utc_date = f"{match_date}T{match_time}Z"
                            seen_match_ids.add(event_id)
                            prediction = smart_ai_prediction(home, away)

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
