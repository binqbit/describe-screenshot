symbols = [' ', ',', '!', '?', ':', ';', '(', ')', '[', ']', '{', '}', '<', '>', '=', '+', '-', '*', '/', '&', '%', '@', '#', '$', '^', '~', '|', '\\']

def find_last_char(text):
    i = -1
    for symbol in symbols:
        j = text.rfind(symbol)
        if j > i:
            i = j
    return i

def print_tab(name, text):
    print("-" * (len(name) + 4))
    print(f"| {name} |")

    lines = []
    for line in text.split("\n"):
        while len(line) > 96:
            i = find_last_char(line[:96])
            if i == -1:
                i = 96
            lines.append(line[:i])
            line = line[i:]
        lines.append(line)
    
    print("-" * 100)
    for line in lines:
        print("| " + line.ljust(96) + " |")
    print("-" * 100)
