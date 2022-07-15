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

def find_words(path,word_input):
    """Finds words and returns a list of strings."""
    word_indexes = []
    word_count = 0
    with open(path,"r",encoding="utf-8") as file:
        for i,line in enumerate(file):
            for word in line.split():
                if word == word_input:
                    word_count += 1
                    word_indexes.append("word: {} | line: {}".format(word,i+1))
    
    return word_indexes,word_count

def check_file_type(filename):
    """check to see if is file or dir"""
    is_file = False
    for letter in filename:
        if letter == ".":
            is_file = True
            break

    if is_file == True:
        file_type = "file"
    else:
        file_type = "dir"
    return file_type

def search_by_name(name,binds_list):
    """Searches the name parameter and asks to show content inside."""
    similars = []
    found = False
    for bind in binds_list:
        newpath = bind.path.replace('"',"")
        for filename in dir_content(newpath):
            similarity = SequenceMatcher(None,name.strip().lower(),filename.strip().lower())
            if filename.strip().lower() == name.strip().lower():
                file_path = glob.glob(newpath+"\\"+filename)

                found = True

                return found,(filename,bind.name,file_path)
            elif similarity.ratio() >= 0.30:
                file_type = check_file_type(filename)
                similars.append(text_with_color("Grey","   {} {} in {}".format(file_type,filename,bind.name)))
    
    return found,similars

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
        if i == 1:
            #first index is dummy_dir explaining bind.txt and solves read bug
            pass
        else:
            binds_list.append(Bind(name=bind[0],path=bind[1],index=i-1))
    
    return binds_list

def inside_dir(index,binds_list):
    """Show what's inside a directory"""
    for bind in binds_list:
        if index == str(bind.index):
            newpath = bind.path.replace('"',"")
            for filename in dir_content(newpath):
                file_type = check_file_type(filename)
                print(text_with_color("Grey",(f"   {file_type} {filename}")))

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
            if i != index:
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
    print("   "+text_with_color("Yellow","print (name)")+" -> prints a file using its name")
    print("   "+text_with_color("Yellow","wordfind (word)")+" -> finds a word in any file inside indexes")
    print("Indexes:")
    print("   "+text_with_color("Red","0. -> quits"))
    for bind in binds:
        print(text_with_color("Blue",f"   {bind.index}.{bind.name}"))
    print("-"*20)

def wordfind(parameter,binds_list):
    """Find word in a specific file and show where it is and total count."""
    parameter = parameter.strip().lower()
    for bind in binds_list:
        newpath = bind.path.replace('"',"")
        for file in dir_content(newpath):
            reversed_name = file[::-1]
            if reversed_name[:3] == "txt":
                file_path = glob.glob(newpath+"\\"+file)
                word_indexes,word_count = find_words(file_path[0],parameter)
                if word_count != 0:
                    print(text_with_color("Grey",f"   in folder {bind.name} file named {file}:"))
                    print(text_with_color("Grey",f"      {word_indexes} total count: {word_count}"))
            else:
                pass

#COMMANDS--
@app.command()
def search(name):
    """Search in the directories indexed."""
    binds_list = []
    keyf_read_binds(binds_list)
    found,result = search_by_name(name,binds_list)
    if found == True:
        print(text_with_color("Grey",f"   file {result[0]} in {result[1]}, path: {result[2]}"))
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
        if len(full_choice_list) > 1:
            #parameter is arg ex: search (arg)
            parameter = full_choice_list[1]

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
            inside_dir(parameter,binds_list)
        elif choice == "search":
            found,result = search_by_name(parameter,binds_list)
            if found == True:
                print(text_with_color("Grey",f"   file {result[0]} in {result[1]}, path: {result[2]}"))
            else:
                for file in result:
                    print(file)
        elif choice == "wordfind":
            wordfind(parameter,binds_list)
        elif choice == "print":
            found,result = search_by_name(parameter,binds_list)
            if found == True:
                print(text_with_color("Grey",f"   file {result[0]} in {result[1]}, path: {result[2]}"))
                ask_to_show = input(text_with_color("Yellow","   show content? y/n: ")).lower().strip()
                if ask_to_show == "yes" or ask_to_show == "y":
                    print_file_content(result[2][0])
            else:
                print(text_with_color("Red","   Not found, maybe one of these?"))
                for file in result:
                    print(file)
                    


    print("exiting...")


if __name__ == "__main__":
    app()