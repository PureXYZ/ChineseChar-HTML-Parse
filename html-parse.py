

import sqlite3
import os



input_html = open("input.html", "r")
os.remove("output.sqlite")

sqlite_out = "output.sqlite"
main_table = "main_table"
id_field = "id_num"
char_field = "chinese_char"
text_field = "text_field"
field_type_int = "INTEGER"
field_type_txt = "TEXT" 


conn = sqlite3.connect(sqlite_out)
conn.text_factory = str
c = conn.cursor()

#Create table

c.execute("CREATE TABLE {tn} ({idf} {idft})".format\
          (tn = main_table, idf = id_field, idft = field_type_int,))

c.execute("ALTER TABLE {tn} ADD COLUMN '{cn}' {ct} DEFAULT '{df}'"\
        .format(tn=main_table, cn=char_field, ct=field_type_txt, df="gg"))

c.execute("ALTER TABLE {tn} ADD COLUMN '{cn}' {ct} DEFAULT '{df}'"\
        .format(tn=main_table, cn=text_field, ct=field_type_txt, df="nore"))


item_row = []


def strip_tags(line):

    new_str = ""

    index = 0
    while index in range(len(line)):
        if (index + 2 < len(line)):
            if line[index:index + 3] == "<BR":
                new_str += "\n"
                index += 3
            elif line[index:index + 1] == "</":
                while line[index] != ">":
                    index += 1
            elif line[index] == "<":
                while line[index] != ">":
                    index += 1
            else:
                new_str += line[index]
        index += 1
    

    return new_str
                


while True:
    line = input_html.readline()
    if not line:
        print "Error! start id not found!"
        break
    elif line == '<TABLE border=1 id="start">\n':
        print "Start id found"
        break


while True:
    
    line = input_html.readline()
    
    if not line:
        print "Reached end of file."
        break
    elif line == '</TABLE id="end">\n':
        print "Reached end of table."
        break

    insert_char = "Error"
    insert_num = 1337
    insert_text = "Error again"
    
        
    start_tag_index = 0
    tag_num = 1
    is_open_tag = False

    line = line.rstrip('\n')

    for index,line_char in enumerate(line):
        
        if (index + 4 < len(line)):
            
            if line[index:index + 4] == "<TD>" or line[index:index + 5] == "<TD A":
                
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
        
    item_row.append([insert_num, insert_char, insert_text])
            
        

counter = len(item_row) - 1

while counter >= 0:
    insert_num = item_row[counter][0]
    insert_char = item_row[counter][1]
    insert_text = item_row[counter][2]
    c.execute("INSERT INTO main_table VALUES (?, ?, ?)", (insert_num, insert_char, insert_text))
    counter -= 1


conn.commit()
conn.close()

print "SQLite db created"
