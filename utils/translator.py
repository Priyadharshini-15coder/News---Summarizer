from deep_translator import GoogleTranslator

def translate_to_tamil(text):
    try:
        return GoogleTranslator(source='auto', target='ta').translate(text)
    except:
        return "Translation failed"