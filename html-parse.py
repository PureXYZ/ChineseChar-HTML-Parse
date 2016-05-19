#   Opens input.html in same directory and outputs output.sqlite
#   This will read in table with start tag: <TABLE id="start"> 
#   to end tag </TABLE id="end">.
#   Each line it will read in data in <TR> tags.
#
#   Based on the sample html, first input is the id number,
#       second is the character, and last is the definition
#   Extra functions also clean input.

import sqlite3
import os



input_html = open("input.html", "r")

#   Delete output file if exists!
os.remove("output.sqlite")

sqlite_out = "output.sqlite"
main_table = "main_table"
id_field = "_id"
char_field = "chinese_char"
text_field = "text_field"
field_type_int = "INTEGER"
field_type_txt = "TEXT" 


conn = sqlite3.connect(sqlite_out)
conn.text_factory = str
c = conn.cursor()

#   Create table with column "_id"
c.execute("CREATE TABLE {tn} ({idf} {idft})"\
          .format(tn = main_table, idf = id_field,
                  idft = field_type_int,))

#   Add column "chinese_char" for simplified char
c.execute("ALTER TABLE {tn} ADD COLUMN '{cn}' {ct} DEFAULT '{df}'"\
        .format(tn=main_table, cn=char_field,
                ct=field_type_txt, df="gg"))

#   Add column "chinese_char2" for traditional char
c.execute("ALTER TABLE {tn} ADD COLUMN '{cn}' {ct} DEFAULT '{df}'"\
        .format(tn=main_table, cn="chinese_char2",
                ct=field_type_txt, df="gg2"))

#   Add column "chinese_char_alt" for alternate char
c.execute("ALTER TABLE {tn} ADD COLUMN '{cn}' {ct} DEFAULT '{df}'"\
        .format(tn=main_table, cn="chinese_char_alt",
                ct=field_type_txt, df="gg_alt"))

#   Add column "text_field" for definition
c.execute("ALTER TABLE {tn} ADD COLUMN '{cn}' {ct} DEFAULT '{df}'"\
        .format(tn=main_table, cn=text_field, ct=field_type_txt, df="nore"))


#   Array of all data to be inserted
item_row = []


#   strip_tags(str) will take in a string and produce the
#       string with all tags removed (e.g. <TAG></TAG>, except <BR> which is
#       replaced with '\n'
def strip_tags(line):

    new_str = ""

    index = 0
    while index in range(len(line)):
        if (index + 2 < len(line)):
            if line[index:index + 3] == "<BR":
                new_str += "\n"
                index += 4
            elif line[index:index + 1] == "</":
                while line[index] != ">":
                    index += 1
                index += 1
            elif line[index] == "<":
                while line[index] != ">":
                    index += 1
                index += 1
        if index < len(line):
            new_str += line[index]
        index += 1

    return new_str


#   get_traditional(str) returns all characters inside "(F" and ")" brackets
#   returns None if nothing
def get_traditional(line):
    new_str = ""
    if len(line) <= 3:
        return line
    else:
        index = 0
        while index < len(line):
            if index + 1 < len(line):
                if line[index:index + 2] == "(F":
                    index += 2
                    while line[index] != ")":
                        new_str += line[index]
                        index += 1
            index += 1
        if new_str:
            return new_str
        else:
            return None
    
                    
#   get_simplified(str) returns first chinese character in string (3 chars)
def get_simplified(line):
    return line[0:3]


#   get_alt(str) returns all characters inside "(A" and ")" brackets
#   returns None if nothing
def get_alt(line):
    new_str = ""
    if len(line) <= 3:
        return
    else:
        index = 0
        while index < len(line):
            if index + 1 < len(line):
                if line[index:index + 2] == "(A":
                    index += 2
                    while line[index] != ")":
                        new_str += line[index]
                        index += 1
            index += 1
        if new_str:
            return new_str
        else:
            return None


# sanitize(str) returns string with HTML tags &LT; replaced with
#       "<" and &GT; replaced with ">"
def sanitize(line):
    new_str = ""
    counter = 0;
    while counter < len(line):

        if counter + 4 < len(line):
            if line[counter:counter + 4] == "&LT;":
                counter += 4
                new_str += "<"
            elif line[counter:counter + 4] == "&GT;":
                counter += 4
                new_str += ">"

        new_str += line[counter]
        counter += 1
    return new_str
                

#   reads line until start tag reached
while True:
    line = input_html.readline()
    if not line:
        print "Error! start id not found!"
        break
    elif line == '<TABLE border=1 id="start">\n':
        print "Start id found"
        break

#   reads lines in table until end tag
while True:
    
    line = input_html.readline()
    
    if not line:
        print "Reached end of file."
        break
    elif line == '</TABLE id="end">\n':
        print "Reached end of table."
        break

    insert_char = "Error"
    insert_char2 = "Error2"
    insert_char_alt = "Error_alt"
    insert_num = 1337
    insert_text = "Error again"
    
        
    start_tag_index = 0
    tag_num = 1
    is_open_tag = False

    line = line.rstrip('\n')

    for index,line_char in enumerate(line):
        
        if (index + 4 < len(line)):
            
            if line[index:index + 4] == "<TD>" or\
               line[index:index + 5] == "<TD A":
                
                if is_open_tag:
                    print "Error! Nested tags!"
                    break

                if line[index:index + 4] == "<TD>":
                    start_tag_index = index + 4
                elif line[index:index + 5] == "<TD A":
                    start_tag_index = index + 19
                    
                is_open_tag = True
                
            elif line[index:index + 5] == "</TD>":
                
                if not is_open_tag:
                    print "Error! Extra close tag!"
                    break
                
                if tag_num == 1:
                    insert_num =  int(line[start_tag_index:index])
                    tag_num += 1
                elif tag_num == 2:
                    insert_char = strip_tags(line[start_tag_index:index])
                    tag_num += 1
                elif tag_num == 3:
                    insert_text = strip_tags(line[start_tag_index:index])
                    tag_num += 1

                is_open_tag = False
        else:
            break
        
    item_row.append([insert_num, get_simplified(insert_char),
                     get_traditional(insert_char),get_alt(insert_char),
                     sanitize(insert_text)])
            
        

counter = len(item_row) - 1

while counter >= 0:
    insert_num = item_row[counter][0]
    insert_char = item_row[counter][1]
    insert_char2 = item_row[counter][2]
    insert_char_alt = item_row[counter][3]
    insert_text = item_row[counter][4]
    c.execute("INSERT INTO main_table VALUES (?, ?, ?, ?, ?)",
              (insert_num, insert_char, insert_char2, insert_char_alt, insert_text))
    counter -= 1


conn.commit()
conn.close()

print "SQLite db created"
