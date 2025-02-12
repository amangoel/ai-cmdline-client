#!/usr/bin/env python

from ..lib.cmdline.cmdline import QUIT, NEXT_PROMPT, process_tool_command, process_chat_prompt
from ..lib.cmdline.cmdline import process_image_understanding_prompt
import readline


def main():
    print('Welcome to your helpful commandline client to hosted LLM models!')
    print("Type '! h' anytime to get hints and help about how to use this tool.")

    while True:
        user_input = input('> ')
        user_input = user_input.strip()
        if not user_input:
            continue

        process_tool_command_ret_val = process_tool_command(user_input)
        if process_tool_command_ret_val == QUIT:
            break
        elif process_tool_command_ret_val == NEXT_PROMPT:
            continue

        if process_chat_prompt(user_input) == NEXT_PROMPT:
            continue

        if process_image_understanding_prompt(user_input) == NEXT_PROMPT:
            continue

        print("Did not understand. Enter '! h' to get help.")
        continue

    print('Bye!!!')


if __name__ == '__main__':
    main()
