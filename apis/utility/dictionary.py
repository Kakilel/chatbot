import requests

def define_word(word):
    url = f"https://api.dictionaryapi.dev/api/v2/entries/en/{word}"
    
    try:
        response = requests.get(url)
        response.raise_for_status()
        data = response.json()[0] 

        word = data.get('word', word)
        phonetic = data.get('phonetic', '')
        audio = ''
        if data.get('phonetics'):
            audio = next((p.get('audio') for p in data['phonetics'] if p.get('audio')), '')

        meanings = data.get('meanings', [])
        output = f"**{word.capitalize()}**\n"
        if phonetic:
            output += f"Phonetic: /{phonetic}/\n"
        if audio:
            output += f"[Pronunciation Audio]({audio})\n"

        for meaning in meanings:
            part_of_speech = meaning.get('partOfSpeech', '')
            definitions = meaning.get('definitions', [])
            if definitions:
                definition = definitions[0].get('definition', 'N/A')
                example = definitions[0].get('example', '')
                synonyms = definitions[0].get('synonyms', [])
                
                output += f"\n**Part of speech**: {part_of_speech}\n"
                output += f"Definition: {definition}\n"
                if example:
                    output += f"Example: {example}\n"
                if synonyms:
                    output += f"Synonyms: {', '.join(synonyms[:5])}\n"

        return output

    except Exception as e:
        return f"Could not fetch the definition for '{word}': {str(e)}"

