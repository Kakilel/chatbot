import datetime
import json
import os
import re

from apis.ent.anime import route_anime_query, format_anime_response
from apis.ent.games import route_game_query, format_game_response
from apis.ent.heroes import route_hero_query, format_hero_response
from apis.ent.jokes import route_joke_query, format_joke
from apis.ent.movies import route_movie_query, format_movie_response
from apis.ent.music import route_music_query, format_music_response
from apis.ent.news import route_news_query, format_news_response
from apis.ent.suggest import route_activity_query, format_activity
from apis.ent.trivia import route_trivia_query, format_trivia
from apis.health.fitness import route_exercise_query, format_exercise
from apis.health.food import route_food_query, format_meal_plan
from apis.health.quotes import route_quote_query, format_quote_response
from apis.utility.bible import route_bible_query, format_bible_response
from apis.utility.color import route_color_query, format_color_response
from apis.utility.convert import route_unit_query, format_unit_conversion
from apis.utility.days import route_calendar_query, format_holiday_data
from apis.utility.dictionary import route_define_query
from apis.utility.timezone import route_time_query, format_time_info
from apis.utility.translate import route_translation_query, format_detect_result
from apis.utility.travel import route_tourist_query, format_place_list
from apis.utility.weather import route_weather_query, format_weather_data
from apis.utility.wikipedia import route_wikipedia_query, format_wikipedia_result
from jarvis import handle_jarvis_command

today_str = datetime.date.today().isoformat()
LOG_FILE = f"chat_log_{today_str}.json"

day_log = []
if os.path.exists(LOG_FILE):
    with open(LOG_FILE, 'r', encoding='utf-8') as f:
        try:
            day_log = json.load(f)
        except json.JSONDecodeError:
            print("Warning: chat log file is corrupted. Starting fresh.")
else:
    with open(LOG_FILE, 'w', encoding='utf-8') as f:
        json.dump([], f)

def save_log():
    with open(LOG_FILE, 'w', encoding='utf-8') as f:
        json.dump(day_log, f, indent=4, ensure_ascii=False)

def get_sessions():
    return [{'name': s.get('name', s['session_id'])} for s in day_log]

def start_session(name):
    session_id = datetime.datetime.now().isoformat(timespec='seconds')
    new_session = {
        'session_id': session_id,
        'name': name,
        'created_at': datetime.datetime.now().isoformat(),
        'messages': []
    }
    day_log.append(new_session)
    save_log()
    return new_session

def get_session_by_name(name):
    for session in day_log:
        if session.get('name') == name:
            return session
    return None

def delete_session_by_name(name):
    global day_log
    day_log = [s for s in day_log if s.get('name') != name]
    save_log()

def gemini_chat(session, user_message):
    try:
        response = session["chat"].send_message(user_message)
        return response.text.strip() if hasattr(response, "text") else "No response from Gemini."
    except Exception as e:
        return f"Gemini Error: {str(e)}"

def route_all_apis(session, user_message):
    bot_reply = None
    text = user_message.lower().strip()


    jarvis_response = handle_jarvis_command(user_message)
    if jarvis_response is not None:
        session.setdefault("messages", []).append({
            'timestamp': datetime.datetime.now().isoformat(),
            'user_message': user_message,
            'bot_response': jarvis_response
        })
        for i, s in enumerate(day_log):
            if s['session_id'] == session['session_id']:
                day_log[i] = session
                break
        save_log()
        return jarvis_response



    if session.get("pending_trivia"):
        answer_text = text.upper()
        if answer_text in ['A', 'B', 'C', 'D']:
            idx = ord(answer_text) - 65
            options = session["pending_trivia"]["options"]
            correct = session["pending_trivia"]["answer"]
            if idx < len(options):
                user_choice = options[idx]
                bot_reply = "Correct!" if user_choice == correct else f"Incorrect. The correct answer was: **{correct}**"
                session.pop("pending_trivia", None)

    if not bot_reply and re.search(r"\b(bible|verse|scripture|psalm|corinthians|john|genesis|revelation|timothy|in swahili)\b", text):
        bible_data = route_bible_query(user_message)
        if bible_data:
            bot_reply = format_bible_response(bible_data)

    if not bot_reply and re.search(r"\b(translate|what language|in swahili|in spanish|in french|in chinese)\b", text):
        translate_data = route_translation_query(user_message)
        if translate_data:
            bot_reply = format_detect_result(translate_data)

    if not bot_reply and re.search(r"\b(hex|rgb|hsl|color code|shade|palette|gradient)\b", text):
        color_data = route_color_query(user_message)
        if color_data:
            bot_reply = format_color_response(color_data)

    if not bot_reply and re.search(r"\b(convert|conversion|how many|inches|feet|km|kg|ml|fahrenheit|celsius|°c|°f)\b", text):
        convert_data = route_unit_query(user_message)
        if convert_data:
            bot_reply = format_unit_conversion(convert_data)

    if not bot_reply and re.search(r"\b(current time|timezone|what time|time in)\b", text):
        time_data = route_time_query(user_message)
        if time_data:
            bot_reply = format_time_info(time_data)

    if not bot_reply and re.search(r"\b(define|definition|meaning of|what does .* mean)\b", text):
        dictionary_data = route_define_query(user_message)
        if dictionary_data:
            bot_reply = dictionary_data

    if not bot_reply and re.search(r"\b(calendar|holiday|holidays|celebrated|public holiday|which day)\b", text):
        days_data = route_calendar_query(user_message)
        if days_data:
            bot_reply = format_holiday_data(days_data)

    if not bot_reply and re.search(r"\b(weather|temperature|forecast|climate)\b", text):
        weather_data = route_weather_query(user_message)
        if weather_data:
            bot_reply = format_weather_data(weather_data)

    if not bot_reply and re.search(r"\b(exercise|workout|burn calories|training plan)\b", text):
        fitness_data = route_exercise_query(user_message)
        if fitness_data:
            bot_reply = format_exercise(fitness_data)

    if not bot_reply and re.search(r"\b(food|meal plan|what to eat|healthy food|diet)\b", text):
        food_data = route_food_query(user_message)
        if food_data:
            bot_reply = format_meal_plan(food_data)

    if not bot_reply and re.search(r"\b(quote|inspire|inspiration|motivational|motivate me)\b", text):
        quote_data = route_quote_query(user_message)
        if quote_data:
            bot_reply = format_quote_response(quote_data)

    if not bot_reply and re.search(r"\b(superhero|marvel|dc|batman|spiderman|ironman|hero info)\b", text):
        hero_data = route_hero_query(user_message)
        if hero_data:
            bot_reply = format_hero_response(hero_data)

    if not bot_reply and re.search(r"\b(bored|what can i do|suggest something|fun activity)\b", text):
        activity_data = route_activity_query(user_message)
        if activity_data:
            bot_reply = format_activity(activity_data)

    if not bot_reply and re.search(r"\b(trivia|quiz|ask me a question|test me)\b", text):
        trivia_data = route_trivia_query(user_message)
        if trivia_data:
            bot_reply = format_trivia(trivia_data)
            session["pending_trivia"] = {
                "answer": trivia_data.get("correct_answer"),
                "options": trivia_data.get("options")
            }

    if not bot_reply and re.search(r"\b(news|headlines|breaking news|current events)\b", text):
        news_data = route_news_query(user_message)
        if news_data:
            bot_reply = format_news_response(news_data)

    if not bot_reply and re.search(r"\b(music|song|lyrics|track|band|artist|sang)\b", text):
        music_data = route_music_query(user_message)
        if music_data:
            bot_reply = format_music_response(music_data)

    if not bot_reply and re.search(r"\b(movie|film|actor|cast|tv show|trending movie)\b", text):
        movie_data = route_movie_query(user_message)
        if movie_data:
            bot_reply = format_movie_response(movie_data)

    if not bot_reply and re.search(r"\b(joke|make me laugh|pun|funny)\b", text):
        jokes_data = route_joke_query(user_message)
        if jokes_data:
            bot_reply = format_joke(jokes_data)

    if not bot_reply and re.search(r"\b(game|gamer|ps5|xbox|steam|nintendo|game release)\b", text):
        game_data = route_game_query(user_message)
        if game_data:
            bot_reply = format_game_response(game_data)

    if not bot_reply and re.search(r"\b(anime|manga|one piece|naruto|japan animation)\b", text):
        anime_data = route_anime_query(user_message)
        if anime_data:
            bot_reply = format_anime_response(anime_data)

    if not bot_reply and re.search(r"\b(who is|what is|when was|where is|tell me about|explain|history of)\b", text):
        wiki_data = route_wikipedia_query(user_message)
        if wiki_data and "error" not in wiki_data:
            bot_reply = format_wikipedia_result(wiki_data)

    if not bot_reply:
        bot_reply = gemini_chat(session, user_message)
    
    if not bot_reply:
        bot_reply = "I'm not sure how to help with that."


    session.setdefault("messages", []).append({
        'timestamp': datetime.datetime.now().isoformat(),
        'user_message': user_message,
        'bot_response': bot_reply
    })
    for i, s in enumerate(day_log):
        if s['session_id'] == session['session_id']:
            day_log[i] = session
            break
    save_log()
    return bot_reply
