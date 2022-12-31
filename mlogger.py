import datetime


# levels:
# chat
# warn
# error
# verbose
# all means that the text will be logged to all files

def log(text, level="verbose"):
    time = str(datetime.datetime.now())[:-7]
    line = f"[{time}] {text}\n"
    
    if level == "chat" or level == all:
        with open('logs/chat.log', "a") as file:
            file.write(line)

    if level == "warn" or level == all:
         with open('logs/warn.log', "a") as file:
            file.write(line)

    if level == "error" or level == all:
         with open('logs/error.log', "a") as file:
            file.write(line)

    # log to verbose anyways
    with open('logs/verbose.log', "a") as file:
            file.write(f"[{level}] ".upper() + line)
    print(line)

