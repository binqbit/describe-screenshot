
def print_tab(name, text):
    print("-" * (len(name) + 4))
    print(f"| {name} |")

    list = text.split("\n")
    new_list = []
    for line in list:
        while len(line) > 96:
            new_list.append(line[:96])
            line = line[96:]
        new_list.append(line)
    
    print("-" * 100)
    for line in new_list:
        print("| " + line.ljust(96) + " |")
    print("-" * 100)