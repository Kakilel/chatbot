import requests
import random
import os
import json
import re

api_key = '3fed5ae3acmshb6f4ce20fd17af9p1857a5jsn2ec77070065e'
api_host = 'exercisedb.p.rapidapi.com'
headers = {
    'X-RapidAPI-Key': api_key,
    'X-RapidAPI-Host': api_host
}
base_url = 'https://exercisedb.p.rapidapi.com'


def get_random_exercise():
    try:
        response = requests.get(f'{base_url}/exercises', headers=headers)
        data = response.json()
        exercise = random.choice(data)
        return format_exercise(exercise)
    except Exception as e:
        return f'Failed to fetch exercise: {str(e)}'

def search_exercise_by_name(query):
    try:
        response = requests.get(f'{base_url}/exercises', headers=headers)
        data = response.json()
        matches = [ex for ex in data if query.lower() in ex['name'].lower()]
        if not matches:
            return f'No exercises found for "{query}".'
        return '\n\n'.join(format_exercise(ex) for ex in matches[:5])
    except Exception as e:
        return f"Couldn't find exercises: {str(e)}"

def get_exercises_by_body_part(body_part):
    try:
        url = f"{base_url}/exercises/bodyPart/{body_part.lower()}"
        response = requests.get(url, headers=headers)
        data = response.json()
        if not data:
            return f'No exercises found for {body_part}.'
        return '\n\n'.join(format_exercise(ex) for ex in random.sample(data, min(3, len(data))))
    except Exception as e:
        return f'Failed to fetch body part exercises: {str(e)}'

def get_exercises_by_equipment(equipment):
    try:
        url = f"{base_url}/exercises/equipment/{equipment.lower()}"
        response = requests.get(url, headers=headers)
        data = response.json()
        if not data:
            return f"No exercises found for equipment: {equipment}."
        return '\n\n'.join(format_exercise(ex) for ex in random.sample(data, min(3, len(data))))
    except Exception as e:
        return f"Failed to fetch equipment exercises: {str(e)}"


def format_exercise(exercise):
    return (
        f"**Exercise**: {exercise['name'].title()}\n"
        f"Target Muscle: {exercise['target']}\n"
        f"Body Part: {exercise['bodyPart']}\n"
        f"Equipment: {exercise['equipment']}"
    )


def training_values(exercise, body_part=None):
    default_training = {
        'chest': (4, 10, 90),
        'back': (4, 10, 90),
        'legs': (4, 12, 90),
        'shoulders': (3, 12, 60),
        'arms': (3, 12, 60),
        'core': (3, 20, 30),
        'cardio': (1, "15 min", 0)
    }
    sets, reps, rest = default_training.get(body_part.lower(), (3, 10, 60))
    return {
        'name': exercise,
        'sets': sets,
        'reps': reps,
        'rest': rest
    }

schedule_file = 'workout_schedule.json'
DAYS = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']

WARM_UPS = [
    "Jumping Jacks - 2 min", "Arm Circles - 1 min", "Leg Swings - 1 min",
    "Bodyweight Squats - 2 sets of 15", "Lunges with Twist - 1 min"
]

COOLDOWNS = [
    "Child's Pose - 1 min", "Hamstring Stretch - 1 min each side",
    "Quad Stretch - 1 min each side", "Shoulder Stretch - 1 min", "Neck Rolls - 1 min"
]

CARDIO_FINISHERS = [
    "High Knees - 30 sec x 3", "Burpees - 3 sets of 10",
    "Mountain Climbers - 45 sec x 2", "Shadow Boxing - 1 min"
]

def load_schedule():
    if os.path.exists(schedule_file):
        with open(schedule_file, 'r', encoding='utf-8') as f:
            return json.load(f)
    return {day: [] for day in DAYS}

def save_schedule(schedule):
    with open(schedule_file, 'w', encoding='utf-8') as f:
        json.dump(schedule, f, indent=2)

def add_exercise_to_day(day, exercise, body_part='general'):
    day = day.capitalize()
    schedule = load_schedule()
    if day not in schedule:
        return f'Invalid day: {day}'
    structured_ex = training_values(exercise, body_part)
    schedule[day].append(structured_ex)
    save_schedule(schedule)
    return f"Added '{exercise}' to {day}'s workout."

def get_schedule():
    schedule = load_schedule()
    response = ['Weekly Workout Plan']
    for day in DAYS:
        exercises = schedule.get(day, [])
        if exercises:
            response.append(f'**{day}**:')
            for ex in exercises:
                response.append(
                    f"- {ex['name']}: {ex['sets']} sets x {ex['reps']} reps (rest {ex['rest']}s)"
                )
        else:
            response.append(f'**{day}**: (Rest)')
    return '\n'.join(response)

def generate_schedule_by_bodyparts(bodyparts: dict):
    if isinstance(bodyparts, list):
        bodyparts = {day: part for day, part in zip(DAYS, bodyparts)}
    schedule = {day: [] for day in DAYS}
    for day, part in bodyparts.items():
        try:
            url = f'{base_url}/exercises/bodyPart/{part.lower()}'
            response = requests.get(url, headers=headers)
            data = response.json()
            exercises = random.sample(data, min(3, len(data)))

            day_plan = []
            warmup = random.sample(WARM_UPS, 2)
            day_plan += [{'name': w, 'sets': 1, 'reps': '-', 'rest': 30} for w in warmup]

            day_plan += [training_values(ex['name'], body_part=part) for ex in exercises]

            if part.lower() in ['legs', 'core', 'full body']:
                cardio = random.choice(CARDIO_FINISHERS)
                day_plan.append({'name': cardio, 'sets': 1, 'reps': '-', 'rest': 0})

            cooldown = random.sample(COOLDOWNS, 2)
            day_plan += [{'name': c, 'sets': 1, 'reps': '-', 'rest': 15} for c in cooldown]

            schedule[day] = day_plan

        except Exception as e:
            schedule[day] = [{'name': f'(Error fetching exercises: {str(e)})', 'sets': 0, 'reps': '-', 'rest': 0}]
    save_schedule(schedule)
    return 'Weekly schedule generated successfully!'

def clear_schedule():
    save_schedule({day: [] for day in DAYS})
    return 'Workout schedule cleared.'


def route_exercise_query(query: str):
    query = query.lower()

    if match := re.search(r"add (.+) to (\w+)", query):
        return add_exercise_to_day(match.group(2), match.group(1))

    if re.search(r"(show|my|current) (schedule|workout|plan)", query):
        return get_schedule()

    if match := re.search(r"generate schedule (.+)", query):
        parts = [p.strip() for p in match.group(1).split(',')]
        return generate_schedule_by_bodyparts(parts)

    if re.search(r"(random|suggest) (workout|exercise)", query):
        return get_random_exercise()

    if match := re.search(r"(workout|exercise)s? (for|targeting) (.+)", query):
        return get_exercises_by_body_part(match.group(3))

    if match := re.search(r"(workout|exercise)s? (using|with) (.+)", query):
        return get_exercises_by_equipment(match.group(3))

    if match := re.search(r"(exercise|workout) (.+)", query):
        return search_exercise_by_name(match.group(2))

    return search_exercise_by_name(query)
