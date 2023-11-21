from msvcrt import getch
from sys import argv
from time import sleep, time_ns

from unidecode import unidecode

from utils import *

FUNCTIONS = {
    "input": target_input,
    "file": pack_text,
    "facts": fetch_fact,
    "news": fetch_headlines,
    "help": print_help,
}
DEFAULT_NUM = 5
WAIT_TIME = 0.01


def chalk_print_slice(target, i):
    """
    This function prints only the current character in red, to make sure it is
    easy to keep track where the cursor is.
    """
    string = target[:i]
    string += Chalk.color(target[i : i + 1], "red")
    string += target[i + 1 :]
    print(string, end="\r", flush=True)


def normalise(target):
    """
    Simply converts incorrect inverted commas with standard single quotes.
    """
    return unidecode(target.replace("`", "'"))


def run_mode():
    """
    Determines the switch passed in from the terminal and run the correct 
    function that will fill the text to be typed. The return value is the text
    that is to be typed (target).
    
    The default behaviour would be to retrieve 5 random facts.
    """
    if len(argv) < 2:  # if no arguments were passed, default behavior
        return fetch_fact()
    else:
        if argv[1].startswith("--"):
            switch_name = argv[1][2:]
            if switch_name not in FUNCTIONS.keys():
                exit(
                    "ERR: Invalid switch, possible switches:\n--input, --file, --facts, --news"
                )
            switch_arg = argv[2] if len(argv) == 3 else ""
            if switch_arg.isdigit(): switch_arg = int(switch_arg)
            return FUNCTIONS[switch_name](switch_arg)
        else:
            exit("ERR: Invalid switch format.")


def main():
    target = run_mode()
    

    print("Press 'ctl + c' to exit the program")
    sleep(0.5)
    print(Chalk.color("Target:", "red"))
    sleep(0.5)
    
    total_words = 0
    right_words = 0
    total_time = 0

    # count the amount of words in the target text
    words = sum([len(line.split(" ")) for line in target])

    # start the typing input
    for j, line in enumerate(target): # for each line in target
      
        i = 0
        key = ""
        line = normalise(line.replace("\n", ""))
        curr_target = line # make a copy so that it's not mutated
        chalk_print_slice(line, 0)
        wrong = 1
        time_new = time_ns()
        while i < len(line):
            try: # to intercept a key press
                sleep(WAIT_TIME)
                key = getch()
            except:
                continue

            if key == b"\x03": # catches "ctrl-c"
                exit("\n***** Exiting *****")

            key = key.decode("utf-8")
            if key == "\r":
                key = "\n"

            if key == line[i]: # correct keypress
                i += 1
                wrong = 1
                chalk_print_slice(curr_target, i)
            elif key != "": # incorrect keypress
                wrong -= 1

            if key != "" and wrong >= 0:
                total_words += 1
                total_time += time_ns() - time_new
                time_new = time_ns()

        # takes the string typed thusfar, and appends the current progress percentage
        # at the end
        output_string = Chalk.color(curr_target, "green")
        spaces = (90 - len(line)) * " "
        output_string += Chalk.color(f"{spaces}{(j + 1) * 100 / len(target):>3.1f}%", "yellow")

        print(output_string, flush=True)
        
        right_words += len(line)
        sleep(WAIT_TIME)

    print(Chalk.color("\nDone", "red"))
    sleep(0.5)
    
    word_diff = total_words - right_words
    word_percentage = right_words / total_words
    print(
        Chalk.color(
            f"\nTotal:\t{total_words}\nRight:\t{right_words}\nWrong:\t{word_diff}\nScore:\t{word_percentage:.2%}",
            "green"
        )
    )
    
    result_string = f"Total time: {total_time / 10**9:.2f}s\n"
    result_string += f"Total words: {words:3d}\n"
    result_string += f"WPM: {12 * total_words / (total_time / 10**9):.2f}\n"
    result_string += f"WPM (actual): {(words * 60) / (total_time / 10**9):.2f}"
    print(Chalk.color(result_string, "yellow"))
    
    print("\nWell done!")


if __name__ == "__main__":
    main()
