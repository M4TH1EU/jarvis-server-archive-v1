import csv

# our csv file and a csv reader (encoded in utf8 for special character compatibility)
csv_file = open('Sentences.csv', encoding="utf-8")
csv_reader = csv.reader(csv_file, delimiter='|')

# our sentences, column number and id(s)
sentences = {}
column = 0
sentencesId = csv_file.readline().split("|")

# for every line in our .csv file
for lines in csv_reader:

    # for every hotwords in our .csv file (based on first line)
    for sentenceId in sentencesId:

        # if there some empty "fake" column then don't try to register them
        if 'Column' in sentenceId:
            break
        else:
            # fix an issue with first id
            sentenceId = sentenceId.replace('\ufeff', '')

            # creating an entry to be able to use .append afterward
            if sentenceId not in sentences:
                sentences[sentenceId] = []

            # if the entry is not empty then add it to the sentences dict
            if lines[column] != "":
                sentences[sentenceId].append(lines[column])

        # increment column
        column = column + 1

    # reset column
    column = 0
