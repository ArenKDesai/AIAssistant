from KEYS import gpt_key, user_name
import requests
from openai import OpenAI
import re
from bs4 import BeautifulSoup

client = OpenAI(api_key=gpt_key)

keywords = [
    'weather',
    'temperature'
]

def search_keywords(sentence):
    regex_pattern = '|'.join(keywords)
    matches = re.findall(regex_pattern, sentence, flags=re.IGNORECASE)
    return matches

def process_convo(convo):
    keywords_found = search_keywords(convo)
    tag = []

    if 'weather' in keywords_found or 'temperature' in keywords_found:
        url = 'https://forecast.weather.gov/MapClick.php?textField1=43.07&textField2=-89.39'
        r = requests.get(url)
        soup = BeautifulSoup(r.text, 'html.parser')
        temp = soup.select('.myforecast-current-lrg')[0].text
        weather = soup.select('.myforecast-current')[0].text
        tn_weather = soup.select('.short-desc')[0].text
        tn_temp = soup.select('.temp-low')[0].text
        tag.append(f"weather_current={weather}")
        tag.append(f"temperature_current={temp}")
        tag.append(f"weather_tonight={tn_weather}")
        tag.append(f"temperature_tonight={tn_temp}")

    print(f'Prompt: {convo} {tag}')
    return f'{convo} {tag}'

def get_response(convo):
    response = client.chat.completions.create(
        model = 'gpt-3.5-turbo',
        messages = [
            {
                'role':'system',
                'content':f'''You are Beans, the sassy, sarcastic AI Assistant of {user_name}.
                 You act with a mind of your own and always stay in character. 
                 Anything in brackets is a Python list of optional information you may include in your message. 
                 Keep your answers concise. 
                 No matter what, you never break character. 
                 Your response will be converted into speech, so only respond as if you are speaking out loud.'''
            },
            {
                'role':'user',
                'content':process_convo(convo)
            }
        ],
        temperature=1,
        max_tokens=64
    )

    gpt_response = response.choices[0].message.content
    print(f'Response: {gpt_response}')
    return gpt_response