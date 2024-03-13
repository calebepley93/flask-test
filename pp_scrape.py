import requests
import math
import time
from datetime import datetime
import pytz
import uuid

def convert_utc_to_central(utc_str):
    # Parse the UTC datetime string to a datetime object
    utc_time = datetime.strptime(utc_str, '%Y-%m-%dT%H:%M:%S.%fZ')
    # Set the timezone to UTC
    utc_time = utc_time.replace(tzinfo=pytz.utc)
    # Convert to Central Time
    central_time = utc_time.astimezone(pytz.timezone('US/Central'))
    # Format the datetime string based on whether it's today or another day
    now = datetime.now(pytz.timezone('US/Central'))
    if central_time.date() == now.date():
        return central_time.strftime('Today at %I:%M %p Central')
    else:
        return central_time.strftime('%A at %I:%M %p Central')

def my_task():
    print("This is my task")
    url = 'https://www.propprofessor.com/api/trpc/sportsbook.getAllMarkets?batch=1&input=%7B%220%22%3A%7B%22json%22%3A%7B%22isLive%22%3Afalse%7D%7D%7D'

    # Cookies extracted from the browser
    cookies = {
        '__Host-next-auth.csrf-token': '0a3386183704fd0546205f6b9ce55068a1c1247e778fb8160adbfb1679525e35%7C260a6dc99ebac6761d8a446abc354903b733ed1ff7a885ec7fe18cdfac15256f',
        '__Secure-next-auth.callback-url': 'https%3A%2F%2Fwww.propprofessor.com',
        '__Secure-next-auth.session-token': 'e9d772f6-d63e-40ef-ab1e-45d8f7143c58'
    }
        

    # Make the request with the session token
    response = requests.get(url, cookies=cookies)

    def calculate_implied_probability(odds):
        if odds < 0:
            implied_probability = abs(odds) / (abs(odds) + 100)
        else:  # For positive odds and odds equal to 0, this else block will now only handle positive odds.
            implied_probability = 100 / (odds + 100)
        return implied_probability * 100

    def convert_to_american_odds(fv_prob):
        converted_prob = fv_prob * 100
        if converted_prob > 50:
            american_odds = (converted_prob / (100 - converted_prob)) * -100
        else:
            american_odds = ((100 - converted_prob) / converted_prob) * 100
        return american_odds

    def get_EV(fv_prob, target_odds):
        if target_odds > 0:
            amount_to_win = target_odds
            amount_to_lose = 100
        else:
            amount_to_win = 100
            amount_to_lose = abs(target_odds)
        ev = (fv_prob * amount_to_win) - (amount_to_lose * (1 - fv_prob))
        return ev

    webhook_url = 'https://discord.com/api/webhooks/1206758308103327835/v1-XHkwhJbEGYAj2ODw7pSycGg3n2EEeFUaN14K9nyUJj9Mx0Fmx5LRNenENpCVk9MrI'

    # Check the response
    if response.status_code == 200:
        data = response.json()
        print(data)
        markets = data[0]['result']['data']['json'] 
        for market in markets:
            print(f"Market ID: {market['id']}")  # Print market ID for reference
            total_implied_probability = 0
            implied_probability_count = 0
            target_odds = market['odds']
            start_time_formatted = convert_utc_to_central(market.get('start', ''))
            print(f"Start Time: {start_time_formatted}")
            print(target_odds)
            for key in market:
                if key in ['FanDuel', 'DraftKings', 'BetMGM', 'Caesars', 'BetOnline', 'Bovada', 'ESPN', 'odds']:
                    odds = market[key]
                    print(f"Odds for {key}: {odds}")
                    if odds == 0:
                        continue
                    implied_probability = calculate_implied_probability(odds)
                    total_implied_probability += implied_probability
                    implied_probability_count += 1
                    #can use elifs to find other relevant variables
            if implied_probability_count > 0:
                average_implied_probability_main = total_implied_probability / implied_probability_count
                print(f"Average Implied Probability for Market ID {market['id']}: {average_implied_probability_main}%")
            
            # Initialize variables for subMarket calculations
            sub_total_implied_probability = 0
            sub_implied_probability_count = 0

            if 'subMarkets' in market:
                subMarkets = market['subMarkets']
                for subMarket in subMarkets:
                    for key in subMarket:
                        if key in ['FanDuel', 'DraftKings', 'BetMGM', 'Caesars', 'BetOnline', 'Bovada', 'ESPN']:
                            odds = subMarket[key]
                            if odds == 0:
                                continue
                            implied_probability = calculate_implied_probability(odds)
                            sub_total_implied_probability += implied_probability
                            sub_implied_probability_count += 1
                    if sub_implied_probability_count > 0:
                        average_implied_probability_sub = sub_total_implied_probability / sub_implied_probability_count
                        print(f"Average Implied Probability for SubMarket ID {subMarket['id']}: {average_implied_probability_sub}%")

            # Calculate the vig only if we have both main and subMarket average implied probabilities
            if implied_probability_count > 0 and sub_implied_probability_count > 0:
                false_implied_probability = average_implied_probability_main + average_implied_probability_sub
                vig = (average_implied_probability_main + average_implied_probability_sub) - 100
                print(f"Vig for Market ID {market['id']}: {vig}%")
                fv_prob = average_implied_probability_main / false_implied_probability
                print(f"Fair Value Probability for Market ID {market['id']}: {fv_prob}%")
                fv_american_odds = convert_to_american_odds(fv_prob)
                print(fv_american_odds)
                EV_num = get_EV(fv_prob, target_odds)
                print(f"EV for Market ID {market['id']}: {EV_num}")
                if EV_num > 4:
                    EV_num_rounded_down = math.floor(EV_num * 10) / 10.0
                    fv_american_odds_rounded_down = math.floor(fv_american_odds * 10) / 10.0
                    print(fv_american_odds_rounded_down)
                    
                    unique_id = uuid.uuid4()
                    
                    odds_info_list = []
                    for key in ['FanDuel', 'DraftKings', 'BetMGM', 'Caesars', 'BetOnline', 'Bovada', 'ESPN']:
                        if key in market and market[key] != 0:  # Checking if the sportsbook is in the market and has valid odds
                            odds_info_list.append(f"{key}: {market[key]}")
                    odds_info_string = "\n".join(odds_info_list)
                    
                    link_to_process_play = f"http://yourflaskapp.com/process_play/{unique_id}"
                    
                    data = {
            "embeds": [
                {
                    "title": "EV Alert",
                    "color": 5814783,  # You can change this to any color you prefer
                    "fields": [
                        {"name": "EV%", "value": str(EV_num_rounded_down) + "%", "inline": True},  # Ensure this is a string
                        {"name": "Book", "value": f"{market.get('site', 'N/A')}", "inline": True},
                        {"name": "Line", "value": f"{market.get('odds', 'N/A')}", "inline": True}, 
                        {"name": "FV American Odds", "value": f"{fv_american_odds_rounded_down}", "inline": True},
                        {"name": "Sport", "value": f"{market.get('league', 'N/A')}", "inline": True},
                        {"name": "Match Name", "value": f"{market.get('match', 'N/A')}", "inline": True},
                        {"name": "Market", "value": f"{market.get('marketName', 'N/A')}", "inline": False},
                        {"name": "Play", "value": f"{market.get('name', 'N/A')}", "inline": False},
                        {"name": "Rest of Market", "value": odds_info_string, "inline": True},
                        {"name": "Start Time", "value": start_time_formatted, "inline": True},
                        {"name": "Process Play", "value": f"[Click Here]({link_to_process_play})", "inline": False} 
                    ]
                }
            ]
        }
                    print(data)
                    response = requests.post(webhook_url, json=data)
                    if response.status_code == 204:
                        print("Message sent successfully.")
                    else:
                        print(f"Failed to send message. Status code: {response.status_code} | Response: {response.text}")


        
    else:
        print("Failed to fetch data:", response.status_code)

while True:
    my_task()
    # Wait for 300 seconds (5 minutes) before running the task again
    time.sleep(300)
