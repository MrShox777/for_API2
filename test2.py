import requests
import re


def correct_spelling(text):
    """
    this function corrects wrong words in Russian and other languages
    :param text:
    :return: str: text
    """
    # Send HTTP POST request to Yandex.Speller API

    response_ = requests.post('https://speller.yandex.net/services/spellservice.json/checkText',
                             data={'text': text, 'lang': 'ru'})

    # Get the corrected text from the response
    a = response_.json()

    if a != []:
        # Define a regular expression pattern to match the misspelled words
        pattern = re.compile(r'\b(' + '|'.join(d['word'] for d in a) + r')\b')

        # Replace the misspelled words with the first suggestion in the 's' field of the corresponding dictionary
        corrected_text = pattern.sub(
            lambda match: a[next(i for i, d in enumerate(a) if d['word'] == match.group(1))]['s'][0], text)

        return corrected_text
    else:
        return text



