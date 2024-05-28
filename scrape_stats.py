import curses
import pandas as pd
import requests
import time

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

def scrape_nba_stats(years, season_types):
    df = pd.DataFrame()

    for year in years:
        for season_type in season_types:
            r = get_nba_stats(season=year, season_type=season_type)

            temp_df = pd.DataFrame(r['resultSet']['rowSet'], columns=r['resultSet']['headers'])
            temp_df.insert(0, 'Year', year)
            temp_df.insert(1, 'Season Type', season_type)
            
            df = pd.concat([df, temp_df], axis=0)
        
            lag = 2
            
            print(f'Finished scraping data for the {year} {season_type}')
            print(f'Waiting {lag} seconds')
            
            time.sleep(lag)

    # df.to_csv('nba_stats.csv', index=False)

    return df

def update_menu(stdscr, choices, current_choice):
    stdscr.clear()
    stdscr.addstr(0, 0, "Select a choice:")

    current_row = 2

    for i, choice in enumerate(choices):
        if i == current_choice:
            stdscr.addstr(current_row, 0, f'{i + 1}. {choice}', curses.A_REVERSE)
        else:
            stdscr.addstr(current_row, 0, f'{i + 1}. {choice}')
        current_row += 1

    stdscr.refresh()

def display_menu(stdscr, choices):
    choice = 0
    
    update_menu(stdscr, choices, 0)

    while True:
        key = stdscr.getch()

        if key == curses.KEY_UP:
            choice = (choice - 1) % len(choices)
        elif key == curses.KEY_DOWN:
            choice = (choice + 1) % len(choices)
        elif key == 10: # Enter key
            return choices[choice]

        update_menu(stdscr, choices, choice)

def menu(stdscr, years, season_types):
    curses.curs_set(0)

    chosen_year = display_menu(stdscr, years)
    chosen_season_type = display_menu(stdscr, season_types)

    return chosen_year, chosen_season_type

def filter_and_sort_data(df, year, season_type, stat_category):
    filtered_df = df[(df['Year'] == year) & (df['Season Type'] == season_type)]

    sorted_df = filtered_df.sort_values(by=stat_category, ascending=False).head(10)

    return sorted_df

def main():
    years = [f'{year}-{(year + 1)%100:02}' for year in range(2015, 2018)]
    season_types = ['Regular Season', 'Playoffs']

    df = scrape_nba_stats(years, season_types)

    year, season_type = curses.wrapper(menu, years, season_types)

    sorted_df = filter_and_sort_data(df, year, season_type, 'PTS')

    print(sorted_df)

if __name__ == '__main__':
    main()
