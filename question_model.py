class Question:

    def __init__(self, text, answer, options):
        """Constructor method with text, correct answer, and multiple-choice options. Creates a question object."""
        self.text = text
        self.answer = answer
        self.options = options
        