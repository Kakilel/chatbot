import requests

def get_quote():
    url = 'https://zenquotes.io/api/random'
    try:
        response = requests.get(url,timeout=5)
        data = response.json()


        if isinstance(data,list)and len(data) >0:
            quote = data[0].get('q','No quote found.')
            author = data[0].get('a','Anonymous')
            return f'\'{quote}\' -{author}'
        else:
            return 'Cant fetch quote at the moment.'
    except requests.RequestException as e:
        return f'Network Error:{str(e)}'
    except Exception as e :
        return f'Unaexpected error:{str(e)}'     
print(get_quote())    