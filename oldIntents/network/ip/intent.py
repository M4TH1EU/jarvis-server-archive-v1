import socket


def get_ip_address():
    ip_address = socket.gethostbyname(socket.gethostname() + ".local")

    numbers = ip_address.split(".")
    numbers_in_letters = []
    for number in numbers:
        numbers_in_letters.append(trad(int(number)))

    return " point ".join(numbers_in_letters)


def tradd(num):
    global t1, t2
    ch = ''
    if num == 0:
        ch = ''
    elif num < 20:
        ch = t1[num]
    elif num >= 20:
        if (70 <= num <= 79) or (num >= 90):
            z = int(num / 10)  # add -1 for france format (quatre-vingt)
        else:
            z = int(num / 10)
        ch = t2[z]
        num = num - z * 10
        if (num == 1 or num == 11) and z < 8:
            ch = ch + ' et'
        if num > 0:
            ch = ch + ' ' + tradd(num)
        else:
            ch = ch + tradd(num)
    return ch


def tradn(num):
    global t1, t2
    ch = ''
    flagcent = False
    if num >= 1000000000:
        z = int(num / 1000000000)
        ch = ch + tradn(z) + ' milliard'
        if z > 1:
            ch = ch + 's'
        num = num - z * 1000000000
    if num >= 1000000:
        z = int(num / 1000000)
        ch = ch + tradn(z) + ' million'
        if z > 1:
            ch = ch + 's'
        num = num - z * 1000000
    if num >= 1000:
        if num >= 100000:
            z = int(num / 100000)
            if z > 1:
                ch = ch + ' ' + tradd(z)
            ch = ch + ' cent'
            flagcent = True
            num = num - z * 100000
            if int(num / 1000) == 0 and z > 1:
                ch = ch + 's'
        if num >= 1000:
            z = int(num / 1000)
            if (z == 1 and flagcent) or z > 1:
                ch = ch + ' ' + tradd(z)
            num = num - z * 1000
        ch = ch + ' mille'
    if num >= 100:
        z = int(num / 100)
        if z > 1:
            ch = ch + ' ' + tradd(z)
        ch = ch + " cent"
        num = num - z * 100
        if num == 0 and z > 1:
            ch = ch + 's'
    if num > 0:
        ch = ch + " " + tradd(num)
    return ch


def trad(nb):
    global t1, t2
    nb = round(nb, 2)
    t1 = ["", "un", "deux", "trois", "quatre", "cinq", "six", "sept", "huit", "neuf", "dix", "onze", "douze", "treize",
          "quatorze", "quinze", "seize", "dix-sept", "dix-huit", "dix-neuf"]
    t2 = ["", "dix", "vingt", "trente", "quarante", "cinquante", "soixante", "septante", "huitante", "nonante"]
    # for france
    #  t2 = ["", "dix", "vingt", "trente", "quarante", "cinquante", "soixante", "septante", "quatre-vingt", "nonante"]

    z1 = int(nb)
    z3 = (nb - z1) * 100
    z2 = int(round(z3, 0))
    if z1 == 0:
        ch = "zéro"
    else:
        ch = tradn(abs(z1))
    if z2 > 0:
        ch = ch + tradn(z2)
    if nb < 0:
        ch = "moins " + ch
    return ch


if __name__ == '__main__':
    print(trad(127))
    print(trad(192))
    print(trad(168))
