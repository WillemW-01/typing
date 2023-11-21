# Simple Terminal Typing Game

This program is a simple python script that will allow the user to practise their
typing skills. There are multiple ways to generate text to type, and at the end,
the user will be able to view their `wpm`, `score`, and `time` results.

The cursor's position will be highlighted in red to indicate how far along the
line the user has typed.

## Usage

First install libraries (optionally in a `venv`):

`$ pip3 install -r requirements.txt`

Then, execute program:

`$ python TypingGame.py <input_switch> [input_argument]`

Where `input_switch` is mandatory and one of the following:

| Switch  | Description                                                                                                                                     |
| ------- | ----------------------------------------------------------------------------------------------------------------------------------------------- |
| `help`  | prints out the help message                                                                                                                     |
| `input` | user can type input from stdinput in terminal and use that as typing target.                                                                    |
| `file`  | use a file specified by a filepath as `input_argument`                                                                                          |
| `facts` | fetches a specified number of random facts from an online api (default 3), can specify a different amount by adding `input_argument` (optional) |
| `news`  | scrapes news headlines from the BBC world news website. Can specify more headlines just as above.                                               |
