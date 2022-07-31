from PIL import Image, ImageEnhance, ImageDraw, ImageFont
import cv2
import main
import textwrap
from os import listdir
import numpy
import sys
from random import shuffle




def choose_bg(baza_file=0):
    match baza_file:
        case 0:
            files = [f for f in listdir("pics/") if  f.startswith("baza") and f.endswith(".jpg")]
            rand_file = numpy.random.randint(len(files)-1)
            shuffle(files)
            bg = Image.open(f"pics/{files[rand_file]}")
            return bg
        case _:
            try:
                bg = Image.open(f"pics/baza{baza_file}.jpg")
                return bg
            except:
                files = [f for f in listdir("pics/") if f.startswith("baza") and f.endswith(".jpg")]
                rand_file = numpy.random.randint(len(files) - 1)
                shuffle(files)
                bg = Image.open(f"pics/{files[rand_file]}")
                return bg

MAX_W, MAX_H = 1280, 895




text = None


def create_baza(style, BG=0):
    bg = choose_bg(BG)
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
    cv2.imwrite('pics/ready.jpg', new_img)



myfont = ImageFont.truetype('c059-roman.ttf', 36)



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
        match text_i:
            case "skip":
                sys.exit('Skipped')
            case "stay":
                text_i = stayed_text
            case "new":
                start(create_text())
                succes = False
            case _:
                pass
    elif console == False:
        edited.lower()
        match edited:
            case "skip":
                succes = False
                pass
            case "_":
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


def create_smth(style, BG=0, console=True, edited='none'):
    global final_text
    current_h, pad = 448, 10

    if style == 2:
        if console == True:
            create_baza(style, BG)
            final_text = textwrap.wrap(text=start(create_text()), width=49)
        elif console == False:
            if edited == 'none':
                return create_text()
            elif edited != 'none':
                create_baza(style, BG)
                textik = start(text_i='none',edited=edited,console=False)
                if textik != 'None':
                    final_text = textwrap.wrap(text=textik, width=49)
                elif textik == 'None':
                    return 'ernno'
    elif style == 1:
        create_baza(style, BG)
        final_text = textwrap.wrap(text=f"{main.get_random_quote()}{main.get_random_quote_name()}", width=49)
    result = Image.open('pics/ready.jpg')
    add_text = ImageDraw.Draw(result)
    for line in final_text:
        w, h = add_text.textsize(line, font=myfont)
        add_text.text(((MAX_W - w) / 2, current_h), line, font=myfont)
        current_h+= h + pad
    result.save("pics/ready.jpg")
    return 'succes'


if __name__ == '__main__':
    style = int(input('1)Цитата \n2)Факт \nЧто нужно - '))
    bg = int(input('Фон - '))
    create_smth(style)