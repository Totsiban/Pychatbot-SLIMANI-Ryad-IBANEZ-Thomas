from math import log

import os

import re

import string





def list_of_files(directory, extension):

    files_names = []

    for filename in os.listdir(directory):

        if filename.endswith(extension):

            files_names.append(filename)

    return files_names





def extract_president_names(file_name):

    """Extract the name of the president,

    take in parameter the name of the file"""

    name_pattern = re.compile(r'\b(?:Chirac|Giscard dEstaing|Hollande|Macron|Mitterand|Sarkozy)\s+(.*?)\b', re.IGNORECASE)

    match = name_pattern.search(file_name)

    if match:

        return match.group(1)

    return None





def associate_first_name(president_names):

    """associate the first name of the president with their name,

    take in parameter a list of all their name"""

    name_mapping = {

        "Chirac": "Jacques Chirac",

        "Giscard dEstaing": "Valéry Giscard dEstaing",

        "Mitterrand": "François Mitterrand",

        "Macron": "Emmanuel Macron",

        "Sarkozy": "Nicolas Sarkozy",

        "Hollande": "François Hollande"

    }



    first_names = []



    for full_name in president_names:

        first_name = name_mapping.get(full_name, "Unknown")

        first_names.append(first_name)

    return first_names





def pres_name(files_names):

    """Extract and associate each president's name with their first name,

     take in parameter the name of the file"""

    tab_all_name = []

    dic = {"Chirac": "Jacques Chirac",

           "Giscard dEstaing": "Valéry Giscard dEstaing",

           "Mitterrand": "François Mitterrand",

           "Macron": "Emmanuel Macron",

           "Sarkozy": "Nicolas Sarkozy",

           "Hollande": "François Hollande"

           }

    for name in files_names:

        if name[-5] == "1" or name[-5] == "2":

            tab_all_name.append(dic[name[11:-5]])

        else:

            tab_all_name.append(dic[name[11:-4]])

    tab_all_name = list(set(tab_all_name))

    return tab_all_name





def display_president_names(president_names):

    """Display all the name of the presidents,

    by taking in parameter a list of all their names """

    unique_names_set = set(president_names)



    print("List of President Names:")

    for name in unique_names_set:

        print(name)





def clean_and_store_files(input_dir, output_dir):

    """Remove the punctuation and the upper case of the input_dir and copied

    the cleaned string into a directory output_dir"""

    cleaned_dir = os.path.join(os.path.dirname(__file__), output_dir)

    os.makedirs(cleaned_dir, exist_ok=True)

    for file_name in os.listdir(input_dir):

        if file_name.endswith(".txt"):

            input_path = os.path.join(input_dir, file_name)

            output_path = os.path.join(cleaned_dir, file_name)

            with open(input_path, 'r', encoding='utf-8') as infile:

                content = infile.read().lower()

                content = content.replace("’", " ")

                content = content.replace("'", " ")  # Handle apostrophe

                content = content.replace(",", "")

                content = content.replace("–", " ")  # Handle dash

                content = content.replace("!", "")

                content = content.translate(str.maketrans('', '', string.punctuation))

                content = '\n'.join(line.strip() for line in content.split('\n') if line.strip())

            with open(output_path, 'w', encoding='utf-8') as outfile:

                outfile.write(content)





def calculate_tf(a_string):

    """Compute the Term Frequency of each word in a string take in parameter"""

    dic_tf = {}

    for words in a_string.split(" "):

        for word in words.split("\n"):

            if word.strip() not in dic_tf:

                dic_tf[word.strip()] = 1

            else:

                dic_tf[word.strip()] += 1

    return dic_tf





def calculate_idf(directory):

    """take a directory where all of cleaned speeches are in parameter

    and compute the Inverse Document Frequency"""

    idf = {}

    wordset = []

    modified_wordset = []

    list_doc = list_of_files(directory, 'txt')

    for doc in list_doc:

        with open(os.path.join(directory, doc), 'r', encoding='utf-8') as f:

            string_doc = f.read()

            wordset.append(set(string_doc.split()))



    for i in range(len(wordset) - 1):

        modified_wordset.append(list(wordset[i]))



    for i in range(len(modified_wordset) - 1):

        for word in modified_wordset[i]:

            if word in modified_wordset[i + 1]:

                if word not in idf:

                    idf[word] = 1

                else:

                    idf[word] += 1

    for value in idf.keys():

        idf[value] = log(len(list_doc) / idf[value])



    return idf





def td_idf_matrix(directory):

    """Take a directory in parameter and return a matrix

    with the td-idf of each words in all documents """

    matrix = []

    combined_dic = {}

    idf = calculate_idf(directory)

    for file_name in list_of_files(directory, 'txt'):

        with open(os.path.join(directory, file_name), 'r', encoding='utf-8') as file:  # the list with all the file name

            f = file.read()

            combined_dic.update(calculate_tf(f))



    for file_name in list_of_files(directory, 'txt'):

        with open(os.path.join(directory, file_name), 'r', encoding='utf-8') as file:

            f = file.read()

            tf = calculate_tf(f)



            tf_idf_vector = {word: tf_value * idf.get(word, 0) for word, tf_value in tf.items()}

            matrix.append(tf_idf_vector)



    return matrix
