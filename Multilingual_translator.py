import requests, sys
from bs4 import BeautifulSoup

args = sys.argv
languages = ['Arabic', 'German', 'English', 'Spanish', 'French', 'Hebrew', 'Japanese', 'Dutch', 'Polish', 'Portuguese',
             'Romanian', 'Russian', 'Turkish']

if len(args) > 1:
    try:
        src_lang = languages.index(args[1].title())
    except ValueError:
        print(f"Sorry, the program doesn't support {args[1]}")
        sys.exit()
    try:
        if args[2] == "all":
            trg_lang = -1
        else:
            trg_lang = languages.index(args[2].title())
    except ValueError:
        print(f"Sorry, the program doesn't support {args[2]}")
        sys.exit()

    word_to_translate = args[3]
else:
    print("Hello, you're welcome to the translator. Translator supports:")
    for i in range(len(languages)):
        print(f"{i + 1}. {languages[i]}")

    src_lang = int(input("Type the number of your language:")) - 1
    trg_lang = int(input("Type the number of language you want to translate to or '0' to translate to all languages:")) - 1

    word_to_translate = input("Type the word you want to translate:").lower()
    print()

if trg_lang == -1:
    target_languages = [n.lower() for n in languages if n != languages[src_lang]]
else:
    target_languages = [languages[trg_lang].lower()]

with open(f"{word_to_translate}.txt", 'w', encoding='utf-8') as translateFile:
    for translation in target_languages:
        try:
            r = requests.get(
            f'https://context.reverso.net/translation/{languages[src_lang].lower()}-{translation}/{word_to_translate}',
            headers={'User-Agent': 'Mozilla/5.0'})
        except requests.exceptions.ConnectionError:
            print("Something wrong with your internet connection")
            sys.exit()
        soup = BeautifulSoup(r.content, 'html.parser')

        words = soup.find('div', {'id': 'translations-content'})
        try:
            word_list = words.text.split('\n')
        except AttributeError:
            print(f"Sorry, unable to find {word_to_translate}")
            sys.exit()

        word_translations = [i.lstrip().rstrip() for i in word_list if any(i)]

        src_examples, trg_examples = (list(), list())

        texts_src = soup.find_all('div', {'class': 'src ltr'})
        for i in texts_src:
            src_examples.append(i.text.lstrip().rstrip())
        # because of arabic lang - which cause fault...
        if translation == "arabic":
            texts_trg = soup.find_all('div', {'class': 'trg rtl arabic'})
        elif translation == "hebrew":
            texts_trg = soup.find_all('div', {'class': 'trg rtl'})
        else:
            texts_trg = soup.find_all('div', {'class': 'trg ltr'})

        for i in texts_trg:
            trg_examples.append(i.text.lstrip().rstrip())

        translateFile.write(f"{translation.title()} Translations:\n")
        translateFile.write(word_translations[0] + "\n")
        translateFile.write("\n")

        translateFile.write(f"{translation.title()} Example:\n")
        translateFile.write(src_examples[0] + ":\n")
        translateFile.write(trg_examples[0] + "\n")
        translateFile.write("\n\n")


file = open(f"{word_to_translate}.txt", 'r', encoding='utf-8')
print(file.read())
file.close()
