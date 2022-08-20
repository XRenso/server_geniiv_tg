from PIL import Image, ImageEnhance, ImageDraw, ImageFont
import cv2
import main
import textwrap
from os import listdir
import numpy
import sys
from random import shuffle

def choose_bg(baza_file=0, back=False):
    if baza_file == 0:
        files = [f for f in listdir("pics/") if  f.startswith("baza") and f.endswith(".jpg")]
        rand_file = numpy.random.randint(len(files)-1)
        shuffle(files)
        bg = Image.open(f"pics/{files[rand_file]}")
        if back == False:
            return bg
        elif back == True:
            return  f"pics/{files[rand_file]}"
    else:
        try:
            bg = Image.open(f"pics/baza{baza_file}.jpg")
            if back == False:
                return bg
            elif back == True:
                return f"pics/baza{baza_file}.jpg"
        except:
            files = [f for f in listdir("pics/") if f.startswith("baza") and f.endswith(".jpg")]
            rand_file = numpy.random.randint(len(files) - 1)
            shuffle(files)
            bg = Image.open(f"pics/{files[rand_file]}")
            if back == False:
                return bg
            elif back == True:
                return f"pics/{files[rand_file]}"

MAX_W, MAX_H = 1280, 895




text = None


def create_baza(style, BG=0):
    bg = choose_bg(BG)
    try:
        bg = bg.resize((MAX_W, MAX_H))
    except:
        pass
    enhancer = ImageEnhance.Brightness(bg)

    factor = 0.3
    im_output = enhancer.enhance(factor)
    im_output.save('pics/new_maga.jpg')
    new_bg = cv2.imread('pics/new_maga.jpg')

    if style == 2:
        text = cv2.imread("pics/text_baza.png")
    elif style == 1:
        text = cv2.imread("pics/quote_text.png")

    new_img = cv2.add(text,new_bg)
    cv2.imwrite('pics/ready.png', new_img)



myfont = ImageFont.truetype('c059-roman.ttf', 36)
factfont = ImageFont.truetype('fact.OTF', 36)


def create_text():
    text_i = main.make_fake(original=True,add_joke=False,censor=True,china_style=False)
    return text_i



def start(text_i, console=True, edited='stay'):
    stayed_text = text_i
    succes = True
    if console == True:
        print('\n' + text_i + '\n')
        text_i = input('Редакция - ')
        text_i.lower()

        if text_i == "skip":
            sys.exit('Skipped')
        elif text_i == "stay":
            text_i = stayed_text
        elif text_i == "new":
            start(create_text())
            succes = False
        else:
            pass
    elif console == False:

        if edited.lower() == "skip":
            succes = False
            pass
        else:
            succes = True

    if succes == True and console == True:
        return text_i
    elif succes == True and console == False:
        return  edited
    elif succes == False:
        return 'None'
final_text = None

def count_bg():
    files = [f for f in listdir("pics/") if f.startswith("baza") and f.endswith(".jpg")]
    return len(files)

def new_fact(BG=0):
    bg = choose_bg(BG,True)
    try:
        bg = bg.resize((MAX_W, MAX_H))
        im1 = Image.open(bg)
        im2 = Image.open('pics/new_fact_pattern.png')
        text = Image.open('pics/new_fact_text.png').convert('RGBA')
        avatar = Image.open('pics/avatar_fact.png').convert('RGBA')
        im1.putalpha(256)
        im2.putalpha(256)
        ready_img = Image.blend(im2, im1, 0.1)
        ready_img = ready_img.convert('RGB')
        ready_img.save('pics/ready.jpg')
        ready_img = Image.open('pics/ready.jpg').convert('RGBA')
        ready_img.paste(text, text)
        ready_img.paste(avatar, avatar)
        ready_img.save('pics/ready.png')
    except:
        pass


def create_smth(style, BG=0, console=True, edited='none'):
    global final_text
    if style == 1:
        current_h, pad = 448, 10
        create_baza(style, BG)
        final_text = textwrap.wrap(text=f"{main.get_random_quote()}{main.get_random_quote_name()}", width=49)
    elif style == 2:
        current_h, pad = 300, 10
    if style == 2:
        if console == True:
            new_fact(BG)
            final_text = textwrap.wrap(text=start(create_text()), width=30)
        elif console == False:
            if edited == 'none':
                return create_text()
            elif edited != 'none':
                new_fact(BG)
                textik = start(text_i='none',edited=edited,console=False)
                if textik != 'None':
                    final_text = textwrap.wrap(text=textik, width=30)
                elif textik == 'None':
                    return 'ernno'

    result = Image.open('pics/ready.png')
    add_text = ImageDraw.Draw(result)
    for line in final_text:
        if style == 1:
            w, h = add_text.textsize(line, font=myfont)
            add_text.text(((MAX_W - w) / 2, current_h), line, font=myfont)
            current_h+= h + pad
        elif style == 2:
            w, h = add_text.textsize(line, font=factfont)
            add_text.text((MAX_W / 2, current_h), line, font=factfont)
            current_h += h + pad


    result.save("pics/ready.png")
    return 'succes'



if __name__ == '__main__':
    # style = int(input('1)Цитата \n2)Факт \nЧто нужно - '))
    # bg = int(input('Фон - '))
    # create_smth(style)
    create_smth(2,0,True)