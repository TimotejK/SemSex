from googletrans import Translator

def translate_from_english(text):
    translator = Translator()
    translation = translator.translate(text, src='en', dest='sl')
    return translation.text

if __name__ == '__main__':
    translator = Translator()
    translation = translator.translate("The sky is blue and I like bananas", src='en', dest='sl')
    print(translation.text)