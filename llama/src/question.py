import json_fix
import json

class Question:
    def __init__(self, question, transformed, generated, true_answer, num_answers, type, source, context, true_input, answered, points, total_answers):
        self.question: str = question
        self.transformed: str = transformed
        self.generated: str = generated
        self.true_answer: str = true_answer
        self.num_answers: int = num_answers
        self.type: str = type
        self.source: str = source
        self.context: str = context
        self.true_input: str = true_input
        self.answered: int = answered
        self.points: int = points
        self.total_answers: int = total_answers
    def __json__(self):
        return self.__dict__
    
    @staticmethod
    def read_json(file_name) -> list["Question"]:
        with open(file_name, "r", encoding="utf-8") as json_file:
            data = json.load(json_file, object_hook=lambda d: Question(**d))
        return data