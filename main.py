import numpy.random
import randfacts
from googletrans import Translator
import pyjokes
import pymorphy2
import requests

translator = Translator()
def generate(censor):
    # if censor == True:
    #     f = randfacts.get_fact(True, only_unsafe=False)
    # elif censor == False:
    #     f = randfacts.get_fact(False, only_unsafe=True)
    f = randfacts.get_fact(censor, only_unsafe=not censor)
    fa = translator.translate(f, dest='ru', src='en')
    return fa.text

def make_china_style(ready):
    morph = pymorphy2.MorphAnalyzer()
    new_ready = ''
    j = ready.split()
    for i in j:
        p = morph.parse(i)[0]
        new_ready += p.normal_form + ' '
    return new_ready
def make_fake(original=False, add_joke=True, censor=True, china_style=False):
    fir = generate(censor)
    sec = generate(censor)
    while sec==fir:
        sec = generate(censor)
    thi = translator.translate(pyjokes.get_joke(), dest='ru').text
    first = fir.split()
    second = sec.split()
    third = thi.split()
    rand1 = numpy.random.randint(len(first)-1)
    rand2 = numpy.random.randint(len(second) - 1)
    rand_jok = numpy.random.randint(len(third) - 1)
    ready = ''
    for i in range(rand1+1):
        ready += first[i] + ' '
    for i in range(rand2 + 1):
        ready += second[i] + ' '
    if add_joke == True:
        for i in range(rand_jok + 1):
            ready += third[i] + ' '

    if china_style == True:
        ready = make_china_style(ready)
    if original == True:
        if add_joke == True:
            print(f"{fir}\n{sec} \n{thi}")
        elif add_joke == False:
            print(f"{fir}\n{sec}")
    elif original == False:
        pass
    return ready


def get_random_quote():
    try:
        response = requests.get("https://quote-garden.herokuapp.com/api/v3/quotes/random")
        if response.status_code == 200:

            json_data = response.json()
            data = json_data['data']

            quote = data[0]['quoteText']
            quote_translate = translator.translate(quote, dest='ru', src='en')
            quote_translate = f"«{quote_translate.text}» - "
            return quote_translate
        else:
            print("Error while getting quote")
    except:
        print("Something went wrong! Try Again!")

def get_random_quote_name():
    Man_of_quote = ''
    try:
        response = requests.get("https://quote-garden.herokuapp.com/api/v3/quotes/random")
        if response.status_code == 200:

            json_data = response.json()
            data = json_data['data']

            name = data[0]['quoteAuthor'].split()
            Man_of_quote += name[0]
        else:
            print("Error while getting Name")
    except:
        print("Something went wrong! Try Again!")
    try:
        response = requests.get("https://quote-garden.herokuapp.com/api/v3/quotes/random")
        if response.status_code == 200:

            json_data = response.json()
            data = json_data['data']

            surrname = data[0]['quoteAuthor'].split()
            Man_of_quote += f" {surrname[1]}"
        else:
            print("Error while getting Surrname")
    except:
        print("Something went wrong! Try Again!")
    Man_of_quote = translator.translate(Man_of_quote, dest='ru', src='en').text
    return Man_of_quote

if __name__ == '__main__':
    make_fake(original=False, censor=False, add_joke=False, china_style=False)
    # print(get_random_quote())
    print(get_random_quote_name())