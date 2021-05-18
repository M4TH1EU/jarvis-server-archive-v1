import spacy

nlp = spacy.load("fr_core_news_md")


def get_weather(city):
    return "ensoleillé"


def chatbot(statement):
    howAreYouDetection = [nlp("comment ca va"), nlp("ca va"), nlp("comment vas-tu"), nlp("tu va bien"), nlp("est-ce que ça va")]
    turnOnLightsDetection = [nlp("allume la lumière"), nlp("allume les lumières"), nlp("allume les lampes"), nlp("allumer la lumière")]

    selectedNLPs = turnOnLightsDetection
    statement = nlp(statement)
    min_similarity = 0.75

    similarites = []

    for sentence in selectedNLPs:
        word_tokenize(sentence)
        similarites.append(sentence.similarity(statement))

    if any(similarity > min_similarity for similarity in similarites):
        return "Validé"
    else:
        return "Pas compris"


if __name__ == '__main__':
    while 1:
        print(chatbot(input("Phrase : ")))
