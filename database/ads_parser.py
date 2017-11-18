import _sqlite3

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

        delimeter_count = 0
        entry = ""
        entry_count = 0

        # Read lines, until " appeares 56 times
        last_char = ' '
        second_last_char = ' '
        is_in_json = False

        # Due to the "" in product description and
        # iterate over every char
        line_counter = 0
        for line in infile:
            line_counter += 1
            for ch in line:
                if ch == '\n':
                    second_last_char = last_char
                    last_char = ch
                    continue

                # add ch to entry str
                entry += ch

                # After 18 columns, or 36 delimeters, there will be json string,
                # that requires special handling
                if delimeter_count == 36:
                    is_in_json = True

                # Handle the json string
                if is_in_json:
                    # json string will always end with }}
                    if (second_last_char + last_char) == "}}":
                        is_in_json = False
                        delimeter_count += 1
                else:
                    if delimeter_count >= 58:
                        #entries = entry.split('","')
                        entries = entry.split('","')
                        entries[0] = entries[0].strip('"')
                        #entries[28] = entries[28].replace('"','').replace('\n','')
                        counter = 0
                        #entries = map(replace_f_t, entries)

                        add_new_entry(tuple(entries))
                        conn.commit()
                        for item in entries:
                            print(column_names[counter] + ": " + item)
                            counter += 1


                        print("\n\nEntry: " + str(entry_count) + " Line: " + str(line_counter))
                        entry = ""
                        delimeter_count = 0
                        entry_count += 1

                        if entry_count == entries_num:
                            return
                    if ch == '"':
                        if last_char == '"':
                            if second_last_char == ',':
                                delimeter_count += 2
                            if second_last_char == '{':
                                delimeter_count = delimeter_count
                        else:
                            delimeter_count += 1

                second_last_char = last_char
                last_char = ch
    conn.commit()
    return

def remove_delim(str_list):
    str_list = [x.strip('"') for x in str_list]
    str_list = [x.strip('\n') for x in str_list]
    return str_list

def parse2(filename, lines_num):

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

        delimeter_count = 0
        entry = ""
        entry_count = 0

        # Read lines, until " appeares 56 times
        last_char = ' '
        second_last_char = ' '
        is_in_json = False
        last_line = ""

        # Due to the "" in product description and
        # iterate over every char
        line_counter = 0

        for line in infile:
            line_counter += 1
            partial = line.split('","')
            partial = remove_delim(partial)
            if(len(partial)):
                print(partial)
            if(line_counter == lines_num):
                return

    conn.commit()
    return