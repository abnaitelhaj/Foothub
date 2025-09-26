import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import pandas as pd

# Initialize the WebDriver
driver_path = "C:/Users/AMADEUS/Documents/chromedriver-win64/chromedriver.exe"  # Update this path
service = Service(driver_path)
driver = webdriver.Chrome(service=service)

# URL to scrape
url = 'https://fbref.com/en/comps/9/Premier-League-Stats'

# Open the webpage
driver.get(url)

# Wait for the page to load and find the stats table
WebDriverWait(driver, 10).until(
    EC.presence_of_element_located((By.CLASS_NAME, 'stats_table'))
)

# Find the first table (stats table)
table = driver.find_element(By.CLASS_NAME, 'stats_table')

# Extract all links to squad pages
links = [a.get_attribute('href') for a in table.find_elements(By.TAG_NAME, 'a') if '/squads/' in a.get_attribute('href')]

# List to store all teams' data
all_teams = []

# Loop through each team's URL
for team_url in links:
    team_name = team_url.split("/")[-1].replace("-Stats", "")
    driver.get(team_url)

    # Wait for the team page to load and find the stats table
    WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.CLASS_NAME, 'stats_table'))
    )

    # Find the stats table on the team page
    stats_table = driver.find_element(By.CLASS_NAME, 'stats_table')

    # Convert the table to a DataFrame using pandas
    team_data = pd.read_html(stats_table.get_attribute('outerHTML'))[0]
    team_data["Team"] = team_name
    all_teams.append(team_data)

    time.sleep(1)  # Add a small delay to avoid being blocked

# Concatenate all teams' data and save to CSV
stat_df = pd.concat(all_teams, ignore_index=True)
stat_df.to_csv("stats.csv", index=False)

# Close the browser after scraping
driver.quit()

print("CSV file saved as 'stats.csv'")
