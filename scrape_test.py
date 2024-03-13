import requests
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
import time

def send_discord_message(data):
    webhook_url = 'https://discord.com/api/webhooks/1206758308103327835/v1-XHkwhJbEGYAj2ODw7pSycGg3n2EEeFUaN14K9nyUJj9Mx0Fmx5LRNenENpCVk9MrI'
    response = requests.post(webhook_url, json=data)
    if response.status_code == 204:
        print("Message sent successfully.")
    else:
        print(f"Failed to send message. Status code: {response.status_code} | Response: {response.text}")

def my_task():
    print("This is my task")
    driver = webdriver.Chrome()
    driver.set_window_size(1404, 768)  
    driver.get('https://www.crazyninjaodds.com/site/tools/positive-ev.aspx')
    time.sleep(5)  

    driver.add_cookie({"name": "BetaWarningLimits", "value": "Read=1"})
    driver.add_cookie({"name": "BetaFilters", "value": "DevigMethod=0&ProfitStrategy=0&SortBy=1&IsMain2=0"})
    driver.add_cookie({"name": "BetaSettings", "value": "ExcludedSportsbooks=VMk0rwaZLdl4ybG0jjZEzLRs/QIZIvHAW+LV5vh+0iPS/Fxbm3NNSxOpyXPzW088c1XzBddptMpd1TU+qRLLJw=="})

    time.sleep(5) 
    driver.refresh()
    time.sleep(5)
    
    
    all_links = []
    worst_case_percent_boxes = driver.find_elements(By.CSS_SELECTOR, "td.expand")
    for box in worst_case_percent_boxes:

        worst_case_percent_text = box.text.rstrip('%')  
        worst_case_percent = float(worst_case_percent_text)
        print(worst_case_percent)


        if worst_case_percent > 3.0:
            row_data = [worst_case_percent_text + '%']  
            #finding variables in main table
            sportsbook_element = box.find_element(By.XPATH, "./following-sibling::td[10]")  
            sportsbook_name = sportsbook_element.text
            print("Sportsbook Name:", sportsbook_name)  
            target_line_element = box.find_element(By.XPATH, "./following-sibling::td[9]")
            target_line = target_line_element.text
            fv_element = box.find_element(By.XPATH, "./following-sibling::td[11]")
            fv = fv_element.text
            print("FV:", fv)
            sport_elment = box.find_element(By.XPATH, "./following-sibling::td[5]")
            sport = sport_elment.text
            match_element = box.find_element(By.XPATH, "./following-sibling::td[6]")
            match = match_element.text
            market_element = box.find_element(By.XPATH, "./following-sibling::td[7]")
            market = market_element.text
            bet_element = box.find_element(By.XPATH, "./following-sibling::td[8]")
            bet = bet_element.text
            match_date_element = box.find_element(By.XPATH, "./following-sibling::td[3]")
            match_date = match_date_element.text
            link_element = match_element.find_element(By.TAG_NAME, "a")
            href = link_element.get_attribute("href")
            
            excluded_sportsbooks = ["FanDuel", "Sporttrade (NJ)", "Sporttrade (CO)", "BetRivers"]

    # Check if sportsbook_name is not in the excluded list
            if sportsbook_name not in excluded_sportsbooks:
                all_links.append({
                    "href": href,
                    "initial_data": {
                        "worst_case_percent": worst_case_percent_text,
                        "sportsbook_name": sportsbook_name,
                        "target_line": target_line,
                        "fv": fv,
                        "sport": sport,
                        "match": match,
                        "market": market,
                        "bet": bet,
                        "match_date": match_date,
                    }
                })
            #end finding variables in main table


    for link_info in all_links:
        driver.get(link_info["href"])
        time.sleep(5)
        target_play = link_info["initial_data"]["bet"]
        print("Target Play:", target_play)
        play_boxes = driver.find_elements(By.CSS_SELECTOR, "td.expand")
        print("Play Boxes:", play_boxes)
        play_element = None
        for box in play_boxes:
            play_text = box.text
            if play_text == target_play:
                print("Found play:", play_text)
                play_element = box
                break
            
         # Initialize odds variables with None to signify no value or "0" odds
        FD_line = DK_line = CZR_line = MGM_line = ESPN_line = PrizePicks_line = None

        
        if play_element is not None:
    # Extract each column's line and only update the variable if the line is not "0"
            FD_line = play_element.find_element(By.XPATH, "./following-sibling::td[3]").text if play_element.find_element(By.XPATH, "./following-sibling::td[3]").text != "0" else None
            DK_line = play_element.find_element(By.XPATH, "./following-sibling::td[4]").text if play_element.find_element(By.XPATH, "./following-sibling::td[4]").text != "0" else None
            CZR_line = play_element.find_element(By.XPATH, "./following-sibling::td[5]").text if play_element.find_element(By.XPATH, "./following-sibling::td[5]").text != "0" else None
            MGM_line = play_element.find_element(By.XPATH, "./following-sibling::td[6]").text if play_element.find_element(By.XPATH, "./following-sibling::td[6]").text != "0" else None
            ESPN_line = play_element.find_element(By.XPATH, "./following-sibling::td[7]").text if play_element.find_element(By.XPATH, "./following-sibling::td[7]").text != "0" else None
            PrizePicks_line = play_element.find_element(By.XPATH, "./following-sibling::td[12]").text if play_element.find_element(By.XPATH, "./following-sibling::td[12]").text != "0" else None

# Rest of the code to format and update combined_data

        # Construct additional odds formatted string with non-"0" odds
        odds_parts = []
        for name, line in [("Fanduel", FD_line), ("DK", DK_line), ("Caesars", CZR_line), ("MGM", MGM_line), ("ESPN", ESPN_line), ("PrizePicks", PrizePicks_line)]:
            if line:
                odds_parts.append(f"{name}: {line}")
        additional_odds_formatted = "\n".join(odds_parts)
       
        
        # Update combined_data with the formatted additional odds
        combined_data = link_info["initial_data"]
        combined_data.update({
            "additional_market_odds": additional_odds_formatted
        })
        
        print("Additional Odds for Discord:", combined_data['additional_market_odds'])


            
        embeds = [{
        "title": "EV Alert",
        "color": 5814783,
        "fields": [
            {"name": "EV%", "value": f"{combined_data['worst_case_percent']}", "inline": True},
            {"name": "Book", "value": combined_data['sportsbook_name'], "inline": True},
            {"name": "Line", "value": combined_data['target_line'], "inline": True},
            {"name": "FV American Odds", "value": combined_data['fv'], "inline": True},
            {"name": "Sport", "value": combined_data['sport'], "inline": True},
            {"name": "Match Name", "value": combined_data['match'], "inline": True},
            {"name": "Market", "value": combined_data['market'], "inline": False},
            {"name": "Play", "value": combined_data['bet'], "inline": False},
            {"name": "Match Date", "value": combined_data['match_date'], "inline": False},
            # Include additional market odds here
            {"name": "Full Market", "value": combined_data['additional_market_odds'], "inline": False},
        ],
    }]
        data = {"embeds": embeds}
        send_discord_message(data)


    driver.quit()  
    
while True:
    my_task()
    # Wait for 300 seconds (5 minutes) before running the task again
    time.sleep(300)
