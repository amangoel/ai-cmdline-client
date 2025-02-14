def print_help():           # keep lines within 90 chars
    print(
        '''
Every input here looks like this:
    [symbol(s)] [input-tokens]
The [symbol(s)] indicate how the following [input-tokens] are to be interpreted.
A space must be left after [symbol(s}]. Any more space before [input-tokens] will be 
ignored.

List of [symbol(s)] and their meaning:
    !                   talk to the tool itself
    ? or ?<             send a chat message to an LLM model and get a response
    #                   send an image, with a question, to an LLM model and get a response
    $                   send a message to a reasoning LLM model and get a response

Syntax for !:
    ! h                 see this message again
    ! model list        print a numbered list of available models
    ! model set [?|#|$] [model#]
                        set the model to be queried for a functionality. [model#] should
                        be one of the numbers from the numbered list printed using the 
                        command above
    ! q                 exit this tool

Syntax for ?:
    ? [chat-message]    [chat-message] is any number of words
    
Syntax for ?<:
    ?< [file-path]      send the contents of the file at [file-path] as the chat message

Syntax for #:
    # [image-file-path] [question]
                        send the image at [image-file-path] for understanding along with 
                        the [question]        
                        
Syntax for $:
    $ [reasoning-prompt]    
                        [reasoning-prompt] is any number of words
        
Examples:
    ! model set ? 2
    ? Which is better - wireshark or tcpdump?
    ?< /tmp/prompt.txt
    # /tmp/image.png How many people are in the image?
    $ Solve the following problem: If A was thrice B's age 5 years ago and will be twice
      B's age 10 years from now. What are their ages now? 
    ''')

