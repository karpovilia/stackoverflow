import pandas as pd
import requests
from bs4 import BeautifulSoup

# Чтение списка вопросов из файла CSV
question_list = pd.read_csv("question_list.csv", header=None)[0].tolist()

# Создание пустой таблицы для хранения данных
results = []

for question_url in question_list[:5]:
    response = requests.get(question_url)
    soup = BeautifulSoup(response.text, "html.parser")

    # Извлечение данных из вопроса
#    question_title = soup.find("a", {"class": "postcell"}).text
#    print("Question:", question_title)

    # Извлечение ответов на вопрос
    answer_cells = soup.find_all("div", {"class": "post-layout"})
    i = 0
    for answer_cell in answer_cells:
        try:
            answer_text = answer_cell.find("div", {"class": "js-post-body"}).text.strip()
            last_author = answer_cell.find_all("div", {"class": "user-details"})[-1]
            author_name = last_author.find("a").text
            reputation = last_author.find("span", {"class": "reputation-score"}).text
            likes = answer_cell.find("div", {"class": "js-vote-count"}).text
            print("Answer:", answer_text)
            print("Author:", author_name)
            print("Reputation:", reputation)
            print("Likes:", likes)

            # Добавление данных в таблицу
            is_question = True if i == 0 else False
            results.append((question_url, i, is_question, answer_text, author_name, reputation, likes))
            i += 1
            #result_table = result_table.append({'Author': author_name, 'Reputation': reputation, 'Likes': likes, 'Answer': answer_text}, ignore_index=True)
        except Exception as e:
            pass

# Вывод итоговой таблицы
pd.DataFrame(results).to_csv("answers.csv", index=False, header=False)
