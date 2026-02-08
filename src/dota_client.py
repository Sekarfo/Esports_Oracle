import requests

def get_team_recent_matches(team_name: str):
    """
    Finds team, fetches matches, and PRE-CALCULATES stats (Winrate, Avg Duration).
    """
    print(f"DEBUG: Searching for team: {team_name}")
    
    # 1. Поиск команды
    try:
        r = requests.get("https://api.opendota.com/api/teams", timeout=10)
        teams_data = r.json()
        
        found_team = None
        target = team_name.lower().strip()
        
        # Умный поиск
        for team in teams_data:
            t_name = team.get('name', '').lower()
            t_tag = team.get('tag', '').lower()
            if t_name == target or t_tag == target:
                found_team = team
                break
        
        if not found_team:
            for team in teams_data:
                if target in team.get('name', '').lower():
                    found_team = team
                    break
        
        if not found_team:
            return {"error": f"Team '{team_name}' not found."}

        team_id = found_team.get('team_id')
        official_name = found_team.get('name')
        
        # 2. Получение матчей
        matches_url = f"https://api.opendota.com/api/teams/{team_id}/matches"
        matches = requests.get(matches_url, timeout=10).json()[:15] # Берем 15

        # 3. МАТЕМАТИКА (Считаем тут, чтобы разгрузить ИИ)
        wins = 0
        total_duration = 0
        valid_games = 0
        clean_matches = []

        for m in matches:
            is_win = m.get("radiant_win") if m.get("radiant") else not m.get("radiant_win")
            duration = m.get("duration", 0) / 60
            
            if is_win: wins += 1
            total_duration += duration
            valid_games += 1
            
            clean_matches.append({
                "win": is_win,
                "duration": round(duration, 1),
                "opposing_team": m.get("opposing_team_name", "?")
            })
            
        # Финальные расчеты
        win_rate = round((wins / valid_games) * 100, 1) if valid_games > 0 else 0
        avg_duration = round(total_duration / valid_games, 1) if valid_games > 0 else 0

        return {
            "team": official_name,
            "stats": {
                "win_rate_last_15": f"{win_rate}%",
                "avg_duration_mins": avg_duration,
                "total_games_analyzed": valid_games
            },
            "recent_matches_log": clean_matches[:5] # Даем ИИ только последние 5 для контекста
        }

    except Exception as e:
        return {"error": str(e)}