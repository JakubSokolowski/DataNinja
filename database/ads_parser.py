import _sqlite3
import re

conn = _sqlite3.connect('ads_2016_11_01.db')
cursor = conn.cursor()

#conn.commit() conn.close()

def replace_f_t(x):
    if x == "f":
        return "0"
    elif x == "t":
       return "1"
    else:
        return x

def add_new_entry(entry):
    cursor.execute("""INSERT INTO ads VALUES(?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)""", entry)
    return


def parse(filename, entries_num):

    #   TO READ FILE U GOTTA:
    # - read all 29 columns



    # All column names used in ads tab, used in debugging to see where did i f-up
    column_names = ["id",
    "region_id",
    "category_id",
    "subregion_id",
    "district_id",
    "city_id",
    "accurate_location",
    "user_id",
    "sorting_date",
    "created_at_first",
    "valid_to",
    "title",
    "description",
    "full_description",
    "has_phone",
    "params",
    "private_business",
    "has_person",
    "photo_sizes",
    "paidads_id_index",
    "paidads_valid_to",
    "predict_sold",
    "predict_replies",
    "predict_views",
    "reply_call",
    "reply_sms",
    "reply_chat",
    "reply_call_intent",
    "reply_chat_intent"]

    with open(filename) as infile:

        # First step is to create entry string
        # by adding all 29 columns
        entry_str = ""
        # Columns are separated as follows "column1","column2"
        # so, that means 2 delimeters per column

        # Entry format:
        # "col1","col2"..."col28","col29"
        # NEWLINE
        # col1","col2"..."col28","col29"

        delimeter_count = 0
        entry_count = 0

        # Read lines, until " appeares 58 times2
        last_char = ' '
        second_last_char = ' '
        is_in_json = False

        # Due to the "" in product description and
        # iterate over every char


        # CORNER CASES TO HANDLE:
        # 1. Being inside of .json column (col 19, delim 38)
        # 2. Finished entry, newline
        # 3. Being inside of description, ignore ""
        #
        line_counter = 0
        for line in infile:
            for ch in line:

                # Ignore the newlines
                #if ch == '\n':
                #    second_last_char = last_char
                #    last_char = ch
                #    continue

                # Add ch to entry str
                entry_str += ch

                # After 18 columns, or 36 delimeters, there will be json string,
                # that requires special handling
                if delimeter_count == 37:
                    is_in_json = True

                # Handle the json string
                if is_in_json:
                    # json string will always end with }}
                    if (second_last_char + last_char) == "}}":
                        is_in_json = False
                        delimeter_count += 1
                else:
                    if ch == '"':
                        if last_char == '"':
                            if second_last_char == ',':
                                delimeter_count += 2
                            if second_last_char == '{':
                                delimeter_count = delimeter_count
                        else:
                            delimeter_count += 1
                    if delimeter_count == 58:
                        print(entry_str)
                        # entries = entry.split('","')
                        entries = entry_str.split('","')
                        entries[0] = entries[0].strip('"')
                        print("Length of entry list" + str(len(entries)))
                        assert (len(entries) == 29)
                        # entries[28] = entries[28].replace('"','').replace('\n','')
                        counter = 0
                        # entries = map(replace_f_t, entries)

                        # add_new_entry(tuple(entries))
                        # conn.commit()
                        for item in entries:
                            print(counter)
                            print(column_names[counter] + ": " + item)
                            counter += 1

                        print("\n\nEntry: " + str(entry_count) + " Line: " + str(line_counter))
                        entry_str = ""
                        delimeter_count = 0
                        entry_count += 1

                        if entry_count == entries_num:
                            return
                second_last_char = last_char
                last_char = ch
    conn.commit()
    return

def remove_delim(str_list):
    str_list = [x.strip('"') for x in str_list]
    str_list = [x.strip('\n') for x in str_list]
    return str_list

def chunks(l, n):
    """Yield successive n-sized chunks from l."""
    for i in range(0, len(l), n):
        yield l[i:i + n]

def parse2(filename):

    column_names = ["id",
    "region_id",
    "category_id",
    "subregion_id",
    "district_id",
    "city_id",
    "accurate_location",
    "user_id",
    "sorting_date",
    "created_at_first",
    "valid_to",
    "title",
    "description",
    "full_description",
    "has_phone",
    "params",
    "private_business",
    "has_person",
    "photo_sizes",
    "paidads_id_index",
    "paidads_valid_to",
    "predict_sold",
    "predict_replies",
    "predict_views",
    "reply_call",
    "reply_sms",
    "reply_chat",
    "reply_call_intent",
    "reply_chat_intent"]


    with open(filename) as infile:
        columns = infile.read()
        split = re.split('","|"\n"',columns)
        entry = []
        counter = 0
        entry_counter = 0
        for item in split:
            if(counter == 29):
                    entry[0] = entry[0].strip('"')
                    print(entry)
                    entries = map(replace_f_t, entry)
                    if entry_counter != 0:
                        add_new_entry(tuple(entries))
                    entry = []
                    counter = 0
                    entry_counter+=1
            entry.append(item)
            counter += 1
        conn.commit()
    return