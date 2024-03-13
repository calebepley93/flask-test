from selenium import webdriver
from selenium.webdriver.common.by import By
import time
import pandas as pd

# Load the spreadsheet
df = pd.read_excel('./EVTracker.xlsx')
matches = df['MATCH']
print(matches)
match_links = []


url = 'https://www.crazyninjaodds.com/site/browse/games.aspx'
driver = webdriver.Chrome()
driver.get(url)

time.sleep(5)

# need to check matches in spreadsheet db
# spreadsheet includes completed matches
# need to check if match is completed
# if match is not completed, I'll need to find where the match on spreadsheet = match on website
# then I'll need to click on the match, navigate to market, and get the CLV