# adapted from the-sea.js by plaao (me)

# The radio is stored as a list of strings which is combined into one string when rendered.
# It is rendered internally in 40x8 resolution.
import math
import random
from CLIRender.classes import Vector2
from colorama import Fore, Style
from music_info import SEC_PER_TICK

radio_time = math.floor(random.random() * 2000)
alphabet = "abcdefghijklmnopqrstuvwxyz"


def init_populate_radio():
    global radio_time

    # Create 12 lists of 80 chars each and get an radio slice for every radio time value needed.
    radio_base = get_radio_slices(radio_time, radio_time + 80)

    radio_time += 80
    return radio_base


def get_radio_slice(xr, glitch):
    x = xr / 5
    c = math.cos(2 * x)+math.sin(0.3*x)+math.sin(1.23*x)
    y = -math.floor(2 * c * math.sin(x))/2 + 2

    # Returns a list of chars which can then be populated into the radio.
    cont_list = []
    for i in range(10):
        if random.random() <= 0.002 * glitch:
            cont_list.append(alphabet[math.floor(random.random() * len(alphabet))])

        else:
            if math.fabs(i-5)<=y:
                cont_list.append("|")
            else:
                cont_list.append(" ")

    return cont_list


def mutate_text(txt, glitch):
    for i in range(len(txt)):
        ch = txt[i]
        if ch in "# " and random.random() <= (0.0002 + ((radio_time % 1200) / 1200000)) * glitch:
            txt = txt[:i] + alphabet[math.floor(random.random() * len(alphabet))] + txt[i + 1:]

    return txt


def get_radio_slices(x1, x2):
    cont_list = [
        "",
        "",
        "",
        "",
        "",
        "",
        "",
        "",
        "",
        ""
    ]

    for i in range(x1,x2):
        radio_slice = get_radio_slice(i, 1)
        for j in range(10):
            cont_list[j] += radio_slice[j]
    


    return cont_list


def update_radio_slices(radio_content, radio_glitch):
    global radio_time
    
    # edits in place
    # get the new slice
    radio_slice = get_radio_slice(radio_time, radio_glitch)
    radio_time += 1
    
    # for every line in content, remove the first char and add the slice char
    for i in range(10):
        radio_content[i] = radio_content[i][1:] + radio_slice[i]


    raw_txt = unpack_content_to_text(radio_content)
    
    return mutate_text(raw_txt, radio_glitch)


def unpack_content_to_text(content):
    # Join every line with \n
    text=""
    text+="-"*80
    for line in content:
        text+=line[:12]+"#"+line[13:]
    text+="-"*80
    return text


def begin_radio():
    return init_populate_radio()

def radio_info(canvas):
    global radio_time
    real_time = radio_time * SEC_PER_TICK
    minutes = int(real_time // 60)
    seconds = int(real_time % 60)
    canvas.set_string(
        0, Vector2(32, 23), f"{minutes:02}:{seconds:02}/04:38", Fore.CYAN + Style.BRIGHT
    )
    canvas.set_string(
        0, Vector2(31, 12), "2019_01_31.wav", Fore.CYAN + Style.BRIGHT
    )
