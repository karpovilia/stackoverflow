import pandas as pd
import requests
from bs4 import BeautifulSoup

url = "https://poker.stackexchange.com/users"
user_list = []
response = requests.get(url)
soup = BeautifulSoup(response.text, "html.parser")
user_blocks = soup.find_all("div", {"class": "user-details"})
for user_block in user_blocks:
    user_list.append("https://poker.stackexchange.com" + user_block.find("a")["href"])
pd.DataFrame(user_list).to_csv("user_list.csv", index=False, header=False)
