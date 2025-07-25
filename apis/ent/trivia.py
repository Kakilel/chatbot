import requests
import html
import random
import time
import re

CATEGORIES = {
    "general": 9,
    "books": 10,
    "film": 11,
    "music": 12,
    "science": 17,
    "sports": 21,
    "history": 23,
    "animals": 27,
}

start_time = None
timeout_seconds = 15

def get_trivia_question(category=None, difficulty='medium', qtype='multiple'):
    global start_time

    category_id = CATEGORIES.get(category.lower()) if category else None
    url = f"https://opentdb.com/api.php?amount=1&type={qtype}"
    if category_id:
        url += f'&category={category_id}'
    if difficulty:
        url += f'&difficulty={difficulty}'

    try:
        response = requests.get(url)
        response.raise_for_status()
        data = response.json()

        if data['response_code'] == 0:
            result = data['results'][0]
            question = html.unescape(result['question'])
            correct = html.unescape(result['correct_answer'])
            incorrect = [html.unescape(ans) for ans in result['incorrect_answers']]
            options = incorrect + [correct]
            random.shuffle(options)

            start_time = time.time()

            return {
                'question': question,
                'options': options,
                'answer': correct,
                'type': result['type']
            }
        else:
            return {"question": "Error fetching trivia", "options": [], "answer": ""}
    except Exception as e:
        return {"question": "Trivia error", "options": [], "answer": str(e)}

def format_trivia(trivia_data):
    q = trivia_data.get("question", "No question")
    options = trivia_data.get("options", [])
    if not options:
        return "Could not load options."

    labels = ['A', 'B', 'C', 'D']
    msg = f" **Trivia Time!**\n\n**Q:** {q}\n"
    for i, opt in enumerate(options):
        msg += f"{labels[i]}. {opt}\n"

    msg += "\n_Reply with A, B, C, or D to answer._"
    return msg



def route_trivia_query(query: str):
    query = query.lower()

    if match := re.search(r"(trivia|quiz|question)", query):
        cat = None
        for c in CATEGORIES:
            if c in query:
                cat = c
                break
        return get_trivia_question(category=cat)

    return None
