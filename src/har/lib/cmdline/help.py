def print_help():
    print(
        '''
Every input here looks like this:
    [symbol(s)] [input-tokens]
The [symbol(s)] indicate how the following [input-tokens] are to be interpreted.
A space must be left after [symbol(s}]. Any more space before [input-tokens] will be ignored.

List of [symbol(s)] and their meaning:
    !                   talk to the tool itself
    ? or ?<             send a chat message to an LLM model and get a response
    #                   send an image, with a question, to an LLM model and get a response

Syntax for !:
    ! h                 see this message again
    ! model list        print a numbered list of available models
    ! model set [?|#] [model#]
                        set the model, indicated by the [model#] chosen from the list
                        printed using the command above, to be the one to be queried
                        for the functionality (? - CHAT, # - IMAGE-UNDERSTANDING) indicated 
    ! q                 exit this tool

Syntax for ?:
    ? [chat-message]    [chat-message] is any number of words
    
Syntax for ?<:
    ?< [file-path]      send the contents of the file at [file-path] as the chat message

Syntax for #:
    # [image-file-path] [question]
                        send the image at [image-file-path] for understanding along with 
                        the [question]        
        
Examples:
    ! model set ? 2
    ? Which is better - wireshark or tcpdump?
    ?< /tmp/prompt.txt
    # /tmp/image.png How many people are in the image?
    ''')

