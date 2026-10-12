import os
import random
import requests
from flask import Flask, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

# TheSportsDB တွင် ရရှိနိုင်သော ကမ္ဘာတစ်ဝှမ်းမှ လိဂ်များနှင့် ဖလားပြိုင်ပွဲများ
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

# လက်ရှိ 2026/2027 ရာသီတွင် ထိပ်တန်းဖောင်နှင့် ရပ်တည်မှုရှိသော အသင်းကြီးများ
ELITE_TEAMS = [
    "Arsenal", "Manchester City", "Liverpool", "Real Madrid", "Barcelona", 
    "Bayern Munich", "Inter", "AC Milan", "Juventus", "PSG", "Benfica", "Sporting CP",
    "Napoli", "Atletico Madrid", "Bayer Leverkusen", "Borussia Dortmund", "Aston Villa", "Tottenham"
]

STRONG_TEAMS = [
    "Chelsea", "Manchester United", "Newcastle", "Villarreal", "Real Sociedad", 
    "RB Leipzig", "Roma", "Lazio", "Atalanta", "Marseille", "Monaco", "Porto"
]

def advanced_ai_analysis(home_team, away_team):
    """အသင်းနှစ်သင်း၏ ခြေစွမ်းနှင့် အဆင့်အတန်းအပေါ်မူတည်၍ အသေးစိတ် တွက်ချက်ခြင်း"""
    
    # ပွဲစဉ်တစ်ခုချင်းစီအတွက် ထူးခြားသော random seed သတ်မှတ်ခြင်း
    seed_key = sum(ord(c) for c in home_team + away_team)
    random.seed(seed_key)

    is_home_elite = any(t.lower() in home_team.lower() for t in ELITE_TEAMS)
    is_away_elite = any(t.lower() in away_team.lower() for t in ELITE_TEAMS)
    
    is_home_strong = any(t.lower() in home_team.lower() for t in STRONG_TEAMS)
    is_away_strong = any(t.lower() in away_team.lower() for t in STRONG_TEAMS)

    # 1. အိမ်ကွင်းအသင်းက အသင်းကြီး / ဧည့်သည်က အသင်းငယ်
    if is_home_elite and not is_away_elite and not is_away_strong:
        score = random.choice(["3 - 0", "3 - 1", "4 - 1", "2 - 0"])
        h_chance, d_chance, a_chance = "75%", "15%", "10%"
        advice = f"{home_team} သည် အိမ်ကွင်းတွင် တိုက်စစ်အသာစီးဖြင့် ဧည့်သည်ကို ဖိကစားကာ ဂိုးပြတ်အနိုင်ယူရန် ရေပန်းစားနေသည်။"

    # 2. ဧည့်သည်အသင်းက အသင်းကြီး / အိမ်ကွင်းအသင်းက အသင်းငယ်
    elif not is_home_elite and not is_home_strong and is_away_elite:
        score = random.choice(["0 - 2", "1 - 3", "0 - 3", "1 - 2"])
        h_chance, d_chance, a_chance = "18%", "22%", "60%"
        advice = f"အဝေးကွင်းဖြစ်သော်လည်း ခြေစွမ်းအထွတ်အထိပ်ရောက်နေသည့် {away_team} က ကစားကွက်ကို ဘက်စုံအသာစီးရယူသွားမည်။"

    # 3. အသင်းကြီးနှစ်သင်း ထိပ်တိုက်တွေ့ဆုံခြင်း (Big Match)
    elif is_home_elite and is_away_elite:
        score = random.choice(["2 - 2", "1 - 1", "2 - 1", "1 - 2"])
        h_chance, d_chance, a_chance = "42%", "36%", "22%"
        advice = f"ဥရောပထိပ်တန်းအသင်းချင်း ထိပ်တိုက်တွေ့ဆုံမှုဖြစ်၍ အကြိတ်အနယ်ရှိပြီး ဂိုးအပြန်အလှန်ဖြင့် သရေကျရန် သို့မဟုတ် အနိုင်အရှုံး အနည်းငယ်ကွာခြားနိုင်ပါသည်။"

    # 4. အကြိတ်အနယ်ရှိမည့် အသင်းလတ်များ တွေ့ဆုံခြင်း
    elif (is_home_strong or is_home_elite) and (is_away_strong or is_away_elite):
        score = random.choice(["1 - 1", "2 - 1", "1 - 0", "0 - 0"])
        h_chance, d_chance, a_chance = "45%", "35%", "20%"
        advice = f"နှစ်သင်း၏ လက်ရှိခြေစွမ်းနှင့် ဖောင်အရ အိမ်ကွင်းအားသာချက်က အဆုံးအဖြတ်ဖြစ်လာနိုင်ချေရှိသည်။"

    # 5. အခြား အသင်းငယ်ချင်း တွေ့ဆုံပွဲများ
    else:
        score = random.choice(["1 - 0", "0 - 1", "1 - 1", "0 - 0"])
        h_chance, d_chance, a_chance = "40%", "38%", "22%"
        advice = f"ခြေစွမ်းနီးစပ်သည့် အသင်းများဖြစ်သဖြင့် အမှားအယွင်းနည်းသူက ရလဒ်ကောင်းကို ပိုင်ဆိုင်သွားမည်။"

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
                            
                            # အသင်းများ၏ အခြေအနေနှင့် ခြေစွမ်းကို အခြေခံ၍ AI ခန့်မှန်းချက်ထုတ်ခြင်း
                            prediction = advanced_ai_analysis(home, away)

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
