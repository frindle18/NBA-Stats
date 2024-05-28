import requests

def get_nba_stats(season, stat_mode='Totals', season_type='Regular Season', stat_category='PTS'):
    base_url = 'https://stats.nba.com/stats/leagueLeaders'

    headers = {
        'Accept': '*/*',
        'Accept-Encoding': 'gzip, deflate, br, zstd',
        'Accept-Language': 'en-US,en;q=0.6',
        'Connection': 'keep-alive',
        'Host': 'stats.nba.com',
        'Origin': 'https://www.nba.com',
        'Referer': 'https://www.nba.com/',
        'Sec-Fetch-Dest': 'empty',
        'Sec-Fetch-Mode': 'cors',
        'Sec-Fetch-Site': 'same-site',
        'Sec-GPC': '1',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/125.0.0.0 Safari/537.36'
    }

    params = {
        'LeagueID': '00',
        'PerMode': stat_mode,
        'Scope': 'S',
        'Season': season,
        'SeasonType': season_type,
        'StatCategory': stat_category
    }

    response = requests.get(base_url, params=params, headers=headers)

    return response.json()

print(get_nba_stats('2021-22'))
