import time

import pandas as pd
import requests
from bs4 import BeautifulSoup

user_list = pd.read_csv("user_list.csv", header=None)[0].tolist()

user_url = user_list[0]
question_list = []

for page in range(1, 100):
    response = requests.get(user_url + f"?tab=answers&sort=votes&page={page}")
    soup = BeautifulSoup(response.text, "html.parser")
    question_blocks = soup.find_all("div", {"class": "s-post-summary--content"})
    for question_block in question_blocks:
        question_list.append(
            "https://poker.stackexchange.com" + question_block.find("a")["href"]
        )
    # если на странице нет вопросов, то выходим из цикла
    if len(question_blocks) == 0:
        break
    # чтобы не забанили, ждем 1 секунду
    time.sleep(1)

pd.DataFrame(question_list).to_csv("question_list.csv", index=False, header=False)
