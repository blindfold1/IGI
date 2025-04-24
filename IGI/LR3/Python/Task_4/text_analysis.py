class TextAnalysisResult:
    __slots__ = ('max_length_count', 'words_with_punctuation', 'longest_word_ending_with_e')

    def __init__(self, max_length_count: int, words_with_punctuation: list[str], longest_word_ending_with_e: str):
        self.max_length_count = max_length_count
        self.words_with_punctuation = words_with_punctuation
        self.longest_word_ending_with_e = longest_word_ending_with_e

def count_max_length_words(text: str) -> int:
    if not text.strip():
        return 0

    words = []
    current_word = ""
    for char in text:
        if char.isalnum() or char == '-':
            current_word += char
        else:
            if current_word:
                words.append(current_word)
            current_word = ""
    if current_word:
        words.append(current_word)

    if not words:
        return 0

    max_length = max(len(word) for word in words)
    return sum(1 for word in words if len(word) == max_length)

def find_words_with_punctuation(text: str) -> list[str]:
    if not text.strip():
        return []

    words_with_punctuation = []
    current_word = ""
    i = 0
    while i < len(text):
        if text[i].isalnum() or text[i] == '-':
            current_word += text[i]
        else:
            if current_word and i < len(text) and text[i] in {',', '.'}:
                words_with_punctuation.append(current_word)
            current_word = ""
        i += 1
    return words_with_punctuation

def find_longest_word_ending_with_e(text: str) -> str:
    if not text.strip():
        return ""

    words = []
    current_word = ""
    for char in text:
        if char.isalnum() or char == '-':
            current_word += char
        else:
            if current_word:
                words.append(current_word)
            current_word = ""
    if current_word:
        words.append(current_word)

    e_words = [word for word in words if word.lower().endswith('e')]
    if not e_words:
        return ""

    longest_word = max(e_words, key=len)
    return longest_word

def analyze_text(text: str) -> TextAnalysisResult:
    max_length_count = count_max_length_words(text)
    words_with_punctuation = find_words_with_punctuation(text)
    longest_word_ending_with_e = find_longest_word_ending_with_e(text)
    return TextAnalysisResult(max_length_count, words_with_punctuation, longest_word_ending_with_e)