import requests
import random

api_key = '3fed5ae3acmshb6f4ce20fd17af9p1857a5jsn2ec77070065e'
api_host = 'exercisedb.p.rapidapi.com'

headers ={
    'X-RapidAPI-Key' : api_key,
    'X-RapidAPI-Host': api_host
}

base_url = 'https://exercisedb.p.rapidapi.com'


def get_random_exercise():
    try:
        response = requests.get(f'{base_url}/exercises',headers=headers)
        data = response.json()
        exercise = random.choice(data)
        return format_exercise(exercise)
    except Exception as e:
        return f'Failed to fetch exercise:{str(e)}'

def search_exercise_by_name(query):
    try:
        response = requests.get(f'{base_url}/exercises',headers=headers)
        data = response.json()
        matches =  [ex for ex in data if query.lower() in ex['name'].lower()]
        if not matches:
            return f'No exercises found for "{query}" '
        return '\n\n'.join(format_exercise(ex) for ex in matches[:5])
    except Exception as e:
        return f"Couldn't find exercises : {str(e)}"


def get_exercises_by_body_part(body_part):
    try:
        url = f"{base_url}/exercises/bodyPart/{body_part.lower()}"
        response = requests.get(url, headers=headers)
        data = response.json()
        if not data:
            return f'No exercises found for {body_part}'
        return '\n\n'.join(format_exercise(ex)for ex in random.sample(data,min(3,len(data))))
    except Exception as e:
        return f'Failed to fetch bodypart exercises:{str(e)}'


def get_exercises_by_equipment(equipment):
    try:
        url = f"{base_url}/exercises/equipment/{equipment.lower()}"
        response = requests.get(url, headers=headers)
        data = response.json()
        if not data:
            return f"No exercises found for equipment: {equipment}"
        return '\n\n'.join(format_exercise(ex) for ex in random.sample(data, min(3, len(data))))
    except Exception as e:
        return f"Failed to fetch equipment exercises: {str(e)}"


def format_exercise(exercise):
    return(
        f"Excercise:{exercise['name'].title()}\n"
        f"Target Muscle:{exercise['target']}\n"
        f"Body Part:{exercise['bodyPart']}\n"
        f"Equipment:{exercise['equipment']}\n"
    )

print(get_exercises_by_equipment("dumbbell"))