#import to make function usable in terminal like commands
import typer
app = typer.Typer(help="""keyf is a CLI program that lets you bind indexes to certain files, 
access them easily and use commands on them.""")

from os import name,system,listdir
import glob

from difflib import SequenceMatcher

#DESKTOP HELPER KEYF (CLI Command Line Interface)--

#CLASSES--
class Bind():
    """Bind class used to save name,path and index of directory."""
    def __init__(self,name,path,index):
        self.name = name
        self.path = path
        self.index = index

    def __str__(self):
        return self.name

#FUNCTIONS--

def text_with_color(color,text):
    """Changes text color."""
    
    if color == "Red":
        coloring = "\u001b[31m"
    elif color == "White":
        coloring = "\u001b[37m"
    elif color == "Blue":
        coloring = "\u001b[34m"
    elif color == "Yellow":
        coloring = "\u001b[33m"
    elif color == "Green":
        coloring = "\u001b[32m"
    elif color == "Grey":
        coloring = "\u001b[30;1m"
    
    return (coloring+text+"\u001b[0m")

def find_words(file,word_input):
    """Finds words and returns a list of strings."""
    word_indexes = []
    word_count = 0
    with open(file,"r") as file:
        for i,line in enumerate(file):
            for word in line.split():
                if word == word_input:
                    word_count += 1
                    word_indexes.append("word: {} | line: {}".format(word,i+1))
    
    return word_indexes,word_count

def search_by_name(name,binds_list):
    """Searches the name parameter and asks to show content inside."""
    similars = []
    for bind in binds_list:
        newpath = bind.path.replace('"',"")
        for filename in dir_content(newpath):
            similarity = SequenceMatcher(None,name.strip().lower(),filename.strip().lower())
            if filename.strip().lower() == name.strip().lower():
                file_path = glob.glob(newpath+"\\"+filename)
                ask_to_show = input(text_with_color("Yellow","show content? y/n: ")).lower().strip()
                if ask_to_show == "yes" or ask_to_show == "y":
                    print_file_content(file_path[0])
                return text_with_color("Grey","   file {} in {}, path: {}".format(filename,bind.name,file_path))
            elif similarity.ratio() >= 0.30:
                similars.append(text_with_color("Grey","   file {} in {}".format(filename,bind.name)))
    
    return similars

def choice_separator(full_choice):
    """Separe command from arguments, command (arg)."""
    full_choice_list = []
    sequence = []
    pointer = 0
    while pointer < len(full_choice):
        #checks strings with quotations
        if (full_choice[pointer] == "'" or full_choice[pointer] == '"') and pointer != len(full_choice):
            while pointer < len(full_choice):
                if full_choice[pointer] != "'" and full_choice[pointer] != '"':
                    sequence.append(full_choice[pointer])
                pointer += 1
            
            full_choice_list.append("".join(sequence[:]))
            sequence.clear()
        else:
            if not(full_choice[pointer].isspace()):
                sequence.append(full_choice[pointer])
            else:
                full_choice_list.append("".join(sequence[:]))
                sequence.clear()
        
            pointer += 1
    
    if len(sequence) > 0:
        full_choice_list.append("".join(sequence[:]))
    return full_choice_list

def dir_content(path):
    """Return list of directories inside a path."""
    directory = path
    return (listdir(directory))

def print_file_content(path):
    """Prints the content of a file using its path."""
    with open(path,"r",encoding="utf-8")as file:
        for line in file:
            print(text_with_color("Grey","   "+line))

def keyf_read_binds(binds_list):
    """Reads a list of binds inside binds.txt"""
    with open("binds.txt","r",encoding="utf-8")as file:
        sequence = []
        bind_data = []
        bind_list_string = []
        for line in file:
            for word in line.strip():
                if word != ",":
                    sequence.append(word)
                else:
                    bind_data.append("".join(sequence))
                    sequence.clear()
            bind_list_string.append(bind_data[:])
            bind_data.clear()
            
    for i,bind in enumerate(bind_list_string,start=1):
        binds_list.append(Bind(name=bind[0],path=bind[1],index=i))
    
    return binds_list

def keyf_add_binds():
    """Adds a bind to binds.txt."""
    name = input("Name of directory: ")
    path = input("Path of directory: ")
    with open("binds.txt","a",encoding="utf-8") as file:
        string = "\n{},{},".format(name,path)
        file.write(string)
        file.close()

def keyf_remove_binds():
    """Removes a bind from binds.txt"""
    index = int(input("index: "))

    with open("binds.txt","r",encoding="utf-8") as file:
        lines = file.readlines()

    with open("binds.txt","w",encoding="utf-8") as file:
        for i,line in enumerate(lines):
            if i != index-1:
                file.write(line)

def keyf_print(binds):
    """Prints commands and bind indexes."""
    print("      K E Y F")
    print("-"*20)
    print("Commands:")
    print("   "+text_with_color("Yellow","search (name)")+" -> search in the directories indexed, put name in quotation marks if name has whitespace")
    print("   "+text_with_color("Yellow","add")+" -> will add a new directory")
    print("   "+text_with_color("Yellow","remove")+" -> will remove a directory")
    print("   "+text_with_color("Yellow","inside (index)")+" -> show content inside directory")
    print("   "+text_with_color("Yellow","print")+" -> finds a word in a specific file path")
    print("   "+text_with_color("Yellow","wordfind")+" -> finds a word in a specific file")
    print("Indexes:")
    print("   "+text_with_color("Red","0. -> quits"))
    for bind in binds:
        print(text_with_color("Blue","   {}.{}".format(bind.index,bind.name)))
    print("-"*20)

def wordfind():
    """Find word in a specific file and show where it is and total count."""
    file_input = input("File path: ")
    word_input = input("Word: ").strip().lower()
    result = find_words(file_input,word_input)
    for i in result[0]:
        print(i)
    print("total count: {}".format(result[1]))

#COMMANDS--
@app.command()
def search(name):
    """Search in the directories indexed."""
    binds_list = []
    keyf_read_binds(binds_list)
    result = search_by_name(name,binds_list)
    if type(result) == str:
        print(result)
    else:
        for file in result:
            print(file)

@app.command()
def keyf():
    """Main command to access indexes and commands."""
    binds_list = []
    keyf_read_binds(binds_list)
    #warning for indexes size
    if len(binds_list) == 0:
        print(text_with_color("Red","use add command to add first index"))
    keyf_print(binds_list)
    choice = ""
    while choice != "0":
        full_choice = typer.prompt(">")
        full_choice_list = choice_separator(full_choice)
        choice = full_choice_list[0]
        if choice != "0":
            for bind in binds_list:
                if choice == str(bind.index):
                    print(bind.name,text_with_color("Grey",bind.path))
        
        if choice == "add":
            keyf_add_binds()
            print("added..")
        elif choice == "remove":
            keyf_remove_binds()
            print("removed..")
        elif choice == "inside":
            #command (arg) -> arg is index
            index = full_choice_list[1]
            for bind in binds_list:
                if index == str(bind.index):
                    newpath = bind.path.replace('"',"")
                    for filename in dir_content(newpath):
                        print(text_with_color("Grey","   "+filename))
        elif choice == "search":
            name = full_choice_list[1]
            result = search_by_name(name,binds_list)
            if type(result) == str:
                print(result)
            else:
                for file in result:
                    print(file)
        elif choice == "wordfind":
            wordfind()
        elif choice == "print":
            printpath = input("path: ")
            newprintpath = printpath.replace('"',"")
            print_file_content(newprintpath)
                        


    print("exiting...")


if __name__ == "__main__":
    app()