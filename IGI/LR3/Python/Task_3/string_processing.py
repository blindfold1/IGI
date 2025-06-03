class PunctuationAnalysisResult:

    __slots__ = ('space_count', 'punctuation_count')

    def __init__(self, space_count: int, punctuation_count: int):
        self.space_count = space_count
        self.punctuation_count = punctuation_count

def count_spaces_and_punctuation(text: str) -> PunctuationAnalysisResult:

    if not text:
        return PunctuationAnalysisResult(0, 0)


    punctuation_marks = {'.', ',', ';', ':', '!', '?', '-', '(', ')', '[', ']', '{', '}', '"', "'"}

    space_count = 0
    punctuation_count = 0


    for char in text:
        if char.isspace():
            space_count += 1
        elif char in punctuation_marks:
            punctuation_count += 1

    return PunctuationAnalysisResult(space_count, punctuation_count)