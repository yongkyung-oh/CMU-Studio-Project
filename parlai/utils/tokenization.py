"""Sentence tokenization using NLTK's non-pickle Punkt tables."""


def sentence_tokenizer(language='english'):
    from nltk.tokenize import PunktTokenizer

    if not isinstance(language, str) or not language.isascii() or not language.isalpha():
        raise ValueError('Punkt language must contain ASCII letters only.')
    try:
        return PunktTokenizer(language)
    except LookupError as error:
        raise LookupError(
            'Punkt tables are missing. Install them explicitly with '
            '`python -m nltk.downloader punkt_tab` before using NLTK tokenization.'
        ) from error
