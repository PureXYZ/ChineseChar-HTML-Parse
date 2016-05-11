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
c = conn.cursor()

#Create table

c.execute("CREATE TABLE {tn} ({idf} {idft})".format\
          (tn = main_table, idf = id_field, idft = field_type_int,))

c.execute("ALTER TABLE {tn} ADD COLUMN '{cn}' {ct} DEFAULT '{df}'"\
        .format(tn=main_table, cn=char_field, ct=field_type_txt, df="gg"))

c.execute("ALTER TABLE {tn} ADD COLUMN '{cn}' {ct} DEFAULT '{df}'"\
        .format(tn=main_table, cn=text_field, ct=field_type_txt, df="nore"))


#   Code for inserting a row
#c.execute("INSERT INTO main_table (id_num,chinese_char,text_field) VALUES ({id_num}, '{cc}', '{cd}')"\
#          .format(id_num=insert_num, cc=insert_char, cd=insert_text))


conn.commit()
conn.close()
