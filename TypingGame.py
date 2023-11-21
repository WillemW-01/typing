from msvcrt import getch
from sys import argv, stdin
from time import sleep, time_ns

from unidecode import unidecode

from utils import *

global modes
modes = ["input", "file", "facts", "news"]
functions = {
    "input": target_input,
    "file": target_file,
    "facts": target_facts,
    "news": target_headlines,
    "help": print_help,
}
DEFAULT_NUM = 5


def chalk_print(target, i):
    string = target[:i]
    string += Chalk.color(target[i : i + 1], "red")
    string += target[i + 1 :]
    print(string, end="\r", flush=True)


def normalise(target):
    return unidecode(target.replace("`", "'"))


def get_mode():
    if len(argv) < 2:
        return 2
    else:
        if argv[1].startswith("--"):
            return functions[argv[1][2:]]
        else:
            print(
                """Invalid switch, possible switches:
                    --input, --file, --facts, --news"""
            )
            exit(0)


def get_target(mode_function):
    args_length = len(argv)
    if args_length == 1:
        pass
    elif args_length == 2:
        pass
    elif args_length == 3:
        pass

    target = ""
    if len(argv) < 2:  # if no arguments were passed
        target = target_facts()
    else:
        try:
            target = mode_function() if len(argv) <= 2 else mode_function(argv[2])
        except Exception:
            print("No correction option. Exiting.")
            exit(0)

    return target


def main():
    target = get_target(get_mode())
    WAIT_TIME = 0.01

    print("Press 'ctl + c' to exit the program")
    sleep(0.5)
    print(Chalk.color("Target:", "red"))
    sleep(0.5)
    total_words = 0
    right_words = 0
    total_time = 0

    # count the amount of words in the target text
    words = 0
    for line in target:
        words += len(line.split(" "))

    # start the typing input
    for j in range(0, len(target)):
        i = 0
        key = ""
        target[j] = normalise(target[j].replace("\n", ""))
        # print("Line {0:3d}:".format(j))
        curr_target = target[j]
        chalk_print(target[j], 0)
        wrong = 1
        time_new = time_ns()
        while i < len(target[j]):
            sleep(WAIT_TIME)
            try:
                key = getch()
            except:
                continue

            if key == b"\x03":
                print("\n***** Exiting *****")
                exit(0)

            key = key.decode("utf-8")
            if key == "\r":
                key = "\n"

            if key == target[j][i]:
                i += 1
                wrong = 1
                chalk_print(curr_target, i)
            elif key != "":
                wrong -= 1

            if key != "" and wrong >= 0:
                total_words += 1
                total_time += time_ns() - time_new
                time_new = time_ns()

        output_string = Chalk.color(curr_target, "green")
        spaces = 90 - len(target[j])
        output_string += " " * spaces + Chalk.color(
            "{:>3.1f}%".format((j + 1) * 100 / len(target)), "yellow"
        )

        print(output_string, flush=True)
        right_words += len(target[j])
        sleep(WAIT_TIME)

    print(chalk.color("\nDone", "red"))
    sleep(0.5)
    print(
        chalk.color(
            "\nTotal:\t{0}\nRight:\t{1}\nWrong:\t{2}\nScore:\t{3:.2%}".format(
                total_words,
                right_words,
                total_words - right_words,
                right_words / total_words,
            ),
            "green",
        )
    )
    print(Chalk.color("Total time: {0:.2f}s".format(total_time / 10**9)), "yellow")
    print(Chalk.color("Total words: {0:3d}".format(words)), "yellow")
    print(
        Chalk.color(
            "WPM: {0:.2f}".format(12 * total_words / (total_time / 10**9)), "yellow"
        )
    )
    print(
        Chalk.color(
            "WPM (actual): {0:.2f}".format((words * 60) / (total_time / 10**9)),
            "yellow",
        )
    )

    print("\nWell done!")


if __name__ == "__main__":
    main()
