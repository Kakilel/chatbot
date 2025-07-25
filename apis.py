import datetime
import json
import os
import re

from gemini import send_to_session as gemini_chat
from .apis.ent.anime import route_anime_query, format_anime_response 
from .apis.ent.games import  route_game_query,format_game_response
from .apis.ent.heroes import route_hero_query,format_hero_response
from .apis.ent.jokes import route_joke_query,format_joke
from .apis.ent.movies import route_movie_query,format_movie_response
from .apis.ent.music import route_music_query,format_music_response
from .apis.ent.news import route_news_query,format_news_response
from .apis.ent.suggest import route_activity_query,format_activity
from .apis.ent.trivia import route_trivia_query,format_trivia
from .apis.health.fitness import route_exercise_query,format_exercise
from .apis.health.food import route_food_query,format_meal_plan
from .apis.health.quotes import route_quote_query,format_quote_response
from .apis.utility.bible import route_bible_query,format_bible_response
from .apis.utility.color import route_color_query,format_color_response
from .apis.utility.convert import route_unit_query,format_unit_conversion
from .apis.utility.days import route_calendar_query,format_holiday_data
from .apis.utility.dictionary import route_define_query
from .apis.utility.timezone import route_time_query,format_time_info
from .apis.utility.translate import route_translation_query,format_detect_result
from .apis.utility.travel import route_tourist_query,format_place_list
from .apis.utility.weather import route_weather_query,format_weather_data
from.apis.utility.wikipedia import route_wikipedia_query,format_wikipedia_result



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

def send_to_session(session, user_message):
    bot_reply=None

    if session.get("pending_trivia"):
            answer_text = user_message.strip().upper()
            if answer_text in ['A', 'B', 'C', 'D']:
                idx = ord(answer_text) - 65
                options = session["pending_trivia"]["options"]
                correct = session["pending_trivia"]["answer"]
                if idx < len(options):
                    user_choice = options[idx]
                    if user_choice == correct:
                        bot_reply = "✅ Correct!"
                    else:
                        bot_reply = f"❌ Incorrect. The correct answer was: **{correct}**"
                    session.pop("pending_trivia", None)
    if not bot_reply:
        bible_data = route_bible_query(user_message)
        if bible_data:
            try:
                bot_reply = format_bible_response(bible_data)
            except Exception as e:
                bot_reply = f"Bible API Error:{str(e)}"

    if not bot_reply:
        color_data = route_color_query(user_message)
        if color_data:
            try:
                bot_reply = format_color_response(color_data)
            except Exception as e:
                bot_reply = f"Color API Error:{str(e)}"


    if not bot_reply:
        convert_data = route_unit_query(convert_data)
        if convert_data:
            try:
                bot_reply = format_unit_conversion(convert_data)
            except Exception as e:
                bot_reply = f"Convert API Error:{str(e)}"


    if not bot_reply:
        days_data = route_calendar_query(user_message)
        if days_data:
            try:
                bot_reply = format_holiday_data(days_data)
            except Exception as e:
                bot_reply = f"Days API Error:{str(e)}"


    if not bot_reply:
        dictionary_data =  route_define_query(user_message)
        if dictionary_data:
            try:
                bot_reply = dictionary_data
            except Exception as e:
                bot_reply = f"Word API Error :{str(e)}"


    if not bot_reply:
        time_data =  route_time_query(user_message)
        if time_data:
            try:
                bot_reply = format_time_info(time_data)
            except Exception as e:
                bot_reply = f"Time API Error:{str(e)}"


    if not bot_reply:
        translate_data = route_translation_query(user_message)
        if translate_data:
            try:
                bot_reply = format_detect_result(translate_data)
            except Exception as e:
                bot_reply = f"Translate API Error:{str(e)}"


    if not bot_reply:
        travel_data = route_tourist_query(user_message)
        if travel_data:
            try:
                bot_reply = format_place_list(travel_data)
            except Exception as e:
                bot_reply = f"Travel API Error:{str(e)}"


    if not bot_reply:
        weather_data = route_weather_query(user_message)
        if weather_data:
            try:
                bot_reply = format_weather_data(weather_data)
            except Exception as e:
                bot_reply = f"Weather API Error:{str(e)}"

        
    if not bot_reply:
        fitness_data = route_exercise_query(user_message)
        if fitness_data:
            try:
                bot_reply = format_exercise(fitness_data)
            except Exception as e:
                bot_reply = f"Fitness API Error:{str(e)}"

    if not bot_reply:
        food_data = route_food_query(user_message)
        if food_data:
            try:
                bot_reply = format_meal_plan(food_data)
            except Exception as e:
                bot_reply = f"Food API Error:{str(e)}"
        
    if not bot_reply:
        quote_data=route_quote_query(user_message)
        if quote_data:
            try:
                bot_reply = format_quote_response(quote_data)
            except Exception as e:
                bot_reply = f"Quote API Error:{str(e)}"    


    if not bot_reply:    
        hero_data = route_hero_query(user_message)
        if hero_data:
            try:
                bot_reply = format_hero_response(hero_data)
            except Exception as e:
                bot_reply = f"Superhero API Error:{str(e)}"
        
    if not bot_reply:
        activity_data = route_activity_query(user_message)
        if activity_data:
            try:
                bot_reply = format_activity(activity_data)
            except Exception as e:
                bot_reply = f"Activity API Error:{str(e)}"

    if not bot_reply:
        trivia_data = route_trivia_query(user_message)
        if trivia_data:
            try:
                bot_reply = format_trivia(trivia_data)
            except Exception as e:
                bot_reply = f"Trivia API Error:{str(e)}"    
    
    if not bot_reply:
        news_data = route_news_query(user_message)
        if news_data:
            try:
                bot_reply = format_news_response(news_data)
            except Exception as e:
                bot_reply = f"News API Error:{str(e)}"


    if not bot_reply:           
        music_data = route_music_query(user_message)
        if music_data:
            try:
                bot_reply = format_music_response(music_data)
            except Exception as e:
                bot_reply = f"Music API Error:{str(e)}"

    if not bot_reply:
        movie_data = route_movie_query(user_message)
        if movie_data:
            try:
                bot_reply = format_movie_response(movie_data)
            except Exception as e:
                bot_reply = f"Movies API Error:{str(e)}"    

    if not bot_reply:
        jokes_data = route_joke_query(user_message)
        if jokes_data:
            try:
                bot_reply = format_joke(jokes_data)
            except Exception as e:
                bot_reply =f"Jokes API Error:{str(e)}"

    if not bot_reply:
        game_data = route_game_query(user_message)
        if game_data:
            try:
                bot_reply = format_game_response(game_data)
            except Exception as e:
                bot_reply = f"Game API Error: {str(e)}"
    
    if not bot_reply:                    
        anime_data = route_anime_query(user_message)
        if anime_data:
            try:
                    bot_reply = format_anime_response(anime_data)
            except Exception as e:
                    bot_reply = f"Anime API Error: {str(e)}"

    if not bot_reply and re.search(r"\b(who|what|when|where|why|how|history|science|info|information|explain|define|tell me about)\b", user_message.lower()):
        wiki_data = route_wikipedia_query(user_message)
        if wiki_data and "error" not in wiki_data:
            bot_reply = f"**{wiki_data['title']}**\n\n{wiki_data['extract']}"

    if not bot_reply:
            bot_reply = gemini_chat(session, user_message)


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
