import re
from sys import argv, stdin

import requests
from bs4 import BeautifulSoup

DEFAULT_NUM = 3


class Chalk:
    bcolors = {
        "header": "\033[95m",
        "ENDC": "\033[0m",
        "bold": "\033[1m",
        "underline": "\033[4m",
        "yellow": "\033[93m",
        "red": "\033[91m",
        "green": "\033[92m",
        "blue": "\033[94m",
        "cyan": "\033[96m",
    }

    def color(string, color):
        return f"{Chalk.bcolors[color]}{string}{Chalk.bcolors['ENDC']}"


def target_input():
    print("Type your input string below. Press ctrl-z + enter to stop input.")
    return stdin.read().split("\n")


def target_file(filepath):
    return pack_text(filepath)


def target_facts(param="3"):
    # num = DEFAULT_NUM if len(argv) < 2 else int(argv[2])
    return fetch_fact(int(param))


def target_headlines(param="3"):
    # num = DEFAULT_NUM if len(argv) < 2 else int(argv[2])
    return fetch_headlines(int(param))


def print_help():
    print(
        """\
This program allows you to practise your typing.
There are multiple ways to do this by using different modes:
    --input   -> allows typing directly what you want to practice. Nothing else needed
    --file    -> allows you to specify a input file as the next argument
    --facts   -> fetches interesting facts, can specify the amount of facts to get
    --news    -> fetches headlines from the bbc, can specify the number of them"""
    )
    exit(1)


def fetch_fact(n=3):
    url = "https://uselessfacts.jsph.pl/random.json?language=en"
    output = []
    for i in range(n):
        data = {"text": " " * 86}
        while len(data["text"]) > 85:
            response = requests.get(url)
            data = response.json()

        output += [data["text"]]
        print_progress("Getting random facts...\t", i, n)
    return output


def fetch_headlines(n=10):
    url = "https://www.bbc.com/news"
    output = []

    response = requests.get(url)
    soup = BeautifulSoup(response.text, "html.parser")
    headlines = soup.find("body").find_all("h3")
    for i in range(n):
        text = headlines[i].text.strip()
        if text not in output:
            output += [headlines[i].text.strip()]

    return output


def print_progress(message, i, n):
    count = i
    m = n - count - 1
    if n > 25:
        count = int(i / n * 25)
        m = 25 - count - 1
    text = "[" + "*" * (count + 1) + "." * m + "]"
    print(message, text, end="\r")


def pack_text(filepath):
    output = [""]
    i = 0
    with open(filepath) as file:
        file_data = file.read()
        file_text = file_data.replace("\n", " ").strip()
        file_text = re.sub("( ){2,}", " ", file_text)
        file_text = file_text.split(" ")
        for word in file_text:
            if len(output[i] + word) > 79:
                output[i] = output[i].strip()
                i += 1
                output += [""]
            output[i] += word + " "
        output[i] = output[i].strip()
    return output


if __name__ == "__main__":  # testing class
    num = int(argv[1])
    print(fetch_headlines(num))
