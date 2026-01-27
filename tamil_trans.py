# tamil_transliterator.py

vowel_map = {
    ' ': ' ', 'a': 'அ', 'aa': 'ஆ', 'ai': 'ஐ', 'au': 'ஔ', 'e': 'எ', 'ee': 'ஏ',
    'i': 'இ', 'ii': 'ஈ', 'o': 'ஒ', 'oo': 'ஓ', 'u': 'உ', 'uu': 'ஊ'
}

cons_map = {
    ' ': ' ', 'c': 'ச', 'h': 'ஹ', 'j': 'ஜ', 'k': 'க', 'g': 'க', 'l': 'ல', 'lx': 'ள',
    'm': 'ம', 'n': 'ன', 'nx': 'ண', 'ng': 'ங', 'nj': 'ஞ', 'nd': 'ந', 'p': 'ப', 'b': 'ப',
    'f': 'ஃப', 'r': 'ர', 'rx': 'ற', 's': 'ஸ', 'sx': 'ஷ', 't': 'த', 'd': 'த', 'tx': 'ட',
    'dx': 'ட', 'w': 'வ', 'v': 'வ', 'y': 'ய', 'zh': 'ழ'
}

dv_map = {
    ' ': ' ','a':'' ,'aa': 'ா', 'ai': 'ை', 'au': 'ௗ', 'e': 'ெ', 'ee': 'ே', 'i': 'ி',
    'ii': 'ீ', 'o': 'ொ', 'oo': 'ோ', 'u': 'ு', 'uu': 'ூ', 'eu': 'ு'
}

phone = ['a', 'aa', 'ai', 'au', 'b', 'c', 'd', 'dx', 'e', 'ee', 'eu', 'f', 'g', 'h', 'i',
         'ii', 'j', 'k', 'l', 'lx', 'm', 'n', 'nd', 'nx', 'ng', 'nj', 'o', 'oo', 'p', 'r',
         'rx', 's', 'sx', 't', 'tx', 'u', 'uu', 'w', 'y', 'zh', 'v']

cons = ['c', 'h', 'j', 'k', 'g', 'd', 'dx', 'b', 'l', 'lx', 'm', 'n', 'nx', 'ng', 'nj', 'nd',
        'p', 'f', 'r', 'rx', 's', 'sx', 't', 'tx', 'w', 'y', 'zh', 'v']

vowels = ['a', 'aa', 'ai', 'au', 'e', 'ee','eu', 'i', 'ii', 'o', 'oo', 'u', 'uu']

dv = ['a','aa', 'ai', 'au', 'e', 'ee','eu', 'i', 'ii', 'o', 'oo', 'u', 'uu']

map1 = {**vowel_map, **cons_map}
map2 = {**dv_map, **cons_map}


def transliterate_to_tamil(input_text: str) -> str:
    input_text = input_text.lower() + " "

    # Split input into phonemes
    phn = list(input_text)
    inv_phn = []
    i = 0

    while i < len(phn) - 1:
        phn2 = phn[i] + phn[i+1]
        # phn3 = phn[i] + phn[i+1] + phn[i+2]

        if phn2 in phone:
            inv_phn.append(phn2)
            i += 2
        elif phn[i] in phone:
            inv_phn.append(phn[i])
            i += 1
        else:
            inv_phn.append(phn[i])
            i += 1
    if i == len(phn) - 1:
        inv_phn.append(phn[i])
    tamil = ""
    prev_ph = " "
    i = 0

    while i < len(inv_phn) - 1:
        ph = inv_phn[i]
        nxt_ph = inv_phn[i + 1]

        c_v = ph in vowels
        c_c = ph in cons
        n_v = nxt_ph in vowels
        n_c = nxt_ph in cons

        if ph == ' ':
            tamil += ' '
            prev_ph = ' '
            i += 1

        elif c_v and prev_ph not in cons:
            tamil += vowel_map.get(ph, ph)
            prev_ph = ph
            i += 1

        elif c_v and prev_ph in cons:
            tamil += dv_map.get(ph, ph)
            prev_ph = ph
            i += 1

        elif c_c and nxt_ph == 'a':
            tamil += map2.get(ph, ph)   # implicit vowel
            prev_ph = 'a'
            i += 2                      # skip 'a'

        elif c_c and n_c:
            tamil += map2.get(ph, ph) + "்"
            prev_ph = ph
            i += 1

        elif c_c and nxt_ph == ' ':
            tamil += map2.get(ph, ph) + "்"
            prev_ph = ph
            i += 1

        else:
            tamil += map1.get(ph, ph)
            prev_ph = ph
            i += 1

    # Handle last phoneme
    last_phn = inv_phn[-1]
    if last_phn in vowels and prev_ph not in cons:
        tamil += vowel_map.get(last_phn, last_phn)
    elif last_phn in cons:
        tamil += map1.get(last_phn, last_phn) + "்"
    else:
        tamil += last_phn

    return tamil


# Reverse transliteration (Tamil to Latin)
def transliterate_to_latin(tamil_text: str) -> str:
    tamil_text = tamil_text.upper()

    tamil_arr = ['அ','ஆ','இ','ஈ','உ','ஊ','எ','ஏ','ஐ','ஒ','ஓ','ஔ',
                 'க','ங','ச','ஜ','ஞ','ட','த','ந','ண','ன','ப','ம','ய','ர','ற','ல','ள','ழ','வ',
                 'ஷ','ஸ','ஹ','ஃ','ா','ி','ீ','ு','ூ','ெ','ே','ை','ொ','ோ','ௌ','்']

    cons_arr = ['க','ங','ச','ஜ','ஞ','ட','த','ந','ண','ன','ப','ம','ய','ர','ற','ல','ள','ழ','வ','ஷ','ஸ','ஹ']

    map_rev = {
        'அ':'a', 'ஆ':'aa', 'இ':'i', 'ஈ':'ii', 'உ':'u', 'ஊ':'uu', 'எ':'e', 'ஏ':'ee', 'ஐ':'ai',
        'ஒ':'o', 'ஓ':'oo', 'ஔ':'au', 'க':'k', 'ங':'ng', 'ச':'c', 'ஜ':'j', 'ஞ':'nj', 'ட':'tx',
        'த':'t', 'ந':'nd', 'ண':'nx', 'ன':'n', 'ப':'p', 'ம':'m', 'ய':'y', 'ர':'r', 'ற':'rx',
        'ல':'l', 'ள':'lx', 'ழ':'zh', 'வ':'w', 'ஷ':'sx', 'ஸ':'s', 'ஹ':'h', 'ஃப':'f',
        'ா':'aa', 'ி':'i', 'ீ':'ii', 'ு':'u', 'ூ':'uu', 'ெ':'e', 'ே':'ee', 'ை':'ai',
        'ொ':'o', 'ோ':'oo', 'ௌ':'au'
    }

    english = ""
    phn = list(tamil_text) + [' ']

    i = 0
    while i < len(phn) - 1:
        ch = phn[i]
        if ch in [' ', '\t', '\n']:
            english += ' '
            i += 1
            continue

        if ch == '்':  # pulli - ignore in transliteration
            i += 1
            continue

        if ch in tamil_arr:
            conv = map_rev.get(ch, ch)
            # If consonant and next is consonant or space, add implicit 'a'
            if ch in cons_arr:
                next_ch = phn[i+1]
                if next_ch in cons_arr or next_ch in [' ', '\t', '\n']:
                    english += conv + 'a'
                else:
                    english += conv
            else:
                english += conv
        else:
            english += ch
        i += 1

    return english.strip()


def main():
    import argparse

    parser = argparse.ArgumentParser(description="Tamil transliteration tool")
    parser.add_argument('mode', choices=['to_tamil', 'to_latin'], help="Mode of transliteration")
    parser.add_argument('text', help="Input text to transliterate")

    args = parser.parse_args()

    if args.mode == 'to_tamil':
        output = transliterate_to_tamil(args.text)
    else:
        output = transliterate_to_latin(args.text)

    print(output)


if __name__ == "__main__":
    main()
