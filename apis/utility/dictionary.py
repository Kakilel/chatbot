import requests
import re

def define_word(word):
    url = f"https://api.dictionaryapi.dev/api/v2/entries/en/{word}"
    
    try:
        response = requests.get(url, timeout=5)
        response.raise_for_status()
        data = response.json()[0] 

        word = data.get('word', word)
        phonetic = data.get('phonetic', '')
        audio = ''
        if data.get('phonetics'):
            audio = next((p.get('audio') for p in data['phonetics'] if p.get('audio')), '')

        meanings = data.get('meanings', [])
        output = f" **{word.capitalize()}**\n"
        if phonetic:
            output += f" Phonetic: /{phonetic}/\n"
        if audio:
            output += f"[ Pronunciation Audio]({audio})\n"

        for meaning in meanings[:2]:  
            part_of_speech = meaning.get('partOfSpeech', 'unknown')
            definitions = meaning.get('definitions', [])
            if definitions:
                definition = definitions[0].get('definition', 'N/A')
                example = definitions[0].get('example', '')
                synonyms = definitions[0].get('synonyms', [])
                
                output += f"\n**Part of speech**: _{part_of_speech}_\n"
                output += f"Definition: {definition}\n"
                if example:
                    output += f"Example: _{example}_\n"
                if synonyms:
                    output += f"Synonyms: {', '.join(synonyms[:5])}\n"

        return output

    except Exception as e:
        return f"Could not fetch the definition for '{word}': {str(e)}"


def route_define_query(text: str):
    text = text.lower()

    match = re.search(r"(?:define|definition of|meaning of|what does|word meaning(?: for)?)\s+([a-z\-']+)", text)
    if match:
        word = match.group(1)
        return define_word(word)

    return None
