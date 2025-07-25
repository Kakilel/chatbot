import requests

def get_activity():
    url = 'https://www.boredapi.com/api/activity'

    try:
        response = requests.get(url)
        response.raise_for_status()
        data = response.json()

        activity = data['activity']
        type = data.get('type','random')
        participants = data.get('participants',1)
        price = data.get('price',0)
        accessibility = data.get('accessibility',0)
        link = data.get('link','')


        emojis = {
            "education": "📚",
            "recreational": "🎨",
            "social": "🗣️",
            "diy": "🛠️",
            "charity": "❤️",
            "cooking": "👩‍🍳",
            "relaxation": "🧘",
            "music": "🎵",
            "busywork": "📋"
        }
        if price == 0:
            price_label = 'No Cost!'
        elif price <0.3:
            price_label = 'Cheap!'
        elif price<0.6:
            price_label = 'Moderate'
        else:
            price_label = 'Pricey'

        if accessibility<=0.2:
            difficulty = 'Easy'
        elif accessibility <=0.5:
            difficulty='Moderate'
        else:
            difficulty ='Hard'                        

        emoji = emojis.get(type.lower(),'🎲')

        suggestion = f'{emoji}**{activity}**\n'
        suggestion += f'Participants:{participants}'
        suggestion += f'{price_label} | {difficulty}\n'
        if link:
            suggestion += f'More info:{link}'
        
        return suggestion
    
    except Exception as e:
        return f"Couldn't fetch a boredom-buster{str(e)}"

print (get_activity())    