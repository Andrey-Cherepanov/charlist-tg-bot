from string import ascii_lowercase, digits

def translitirate(line):
    """ Returns translitirated from RU to EN line """
    alter = ascii_lowercase + digits + '_'
    alpha = {'а':'a',
     'б':'b',
     'в':'v',
     'г':'g',
     'д':'d',
     'е':'e',
     'ё':'yo',
     'ж':'zh',
     'з':'z',
     'и':'i',
     'й':'j',
     'к':'k',
     'л':'l',
     'м':'m',
     'н':'n',
     'о':'o',
     'п':'p',
     'р':'r',
     'с':'s',
     'т':'t',
     'у':'u',
     'ф':'f',
     'х':'kh',
     'ц':'c',
     'ч':'ch',
     'ш':'sh',
     'щ':'shch',
     'ы':'y',
     'ь':'\'',
     'э':'e',
     'ю':'yu',
     'я':'ja'}

    result = ''
    for c in line.strip():
        if c in alpha.keys():
            result += alpha[c]
        elif c in alter:
            result += c
    return result
