import json_fix
import json
from strenum import StrEnum


class Question:
    """Represents a single Question of the evaluation dataset and their attributes.
    """
    def __init__(
        self,
        question="",
        transformed="",
        generated="",
        true_answer="",
        num_answers=-1,
        type="",
        source="",
        context="",
        true_input="",
        answered=-1,
        points=-1,
        total_answers=-1,
    ):
        """Initializes a Question object.

        Args:
            question (str, optional): The actual question from the source. Defaults to "".
            transformed (str, optional): The translated and transformed question. Defaults to "".
            generated (str, optional): The generated answer by a model. Defaults to "".
            true_answer (str, optional): The expected answer for this question. Defaults to "".
            num_answers (int, optional): The number of answers in the true_answer. Defaults to -1.
            type (str, optional): The type of the question. Must be of type "QuestionType". Defaults to "".
            source (str, optional): The source of the question. Must be of type "QuestionSource". Defaults to "".
            context (str, optional): The context needed to answer this question. Defaults to "".
            true_input (str, optional): The actual input used to generate the answer. Defaults to "".
            answered (1, optional): Denotes if question was not answered (0), wrong answered (1) or correct answered (2). Defaults to -1.
            points (int, optional): Number of correct answers in the generated answer. Defaults to -1.
            total_answers (int, optional): Number of total answers in the generated answer. Defaults to -1.
        """
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


class QuestionType(StrEnum):
    Single = ("single",)
    Multi = ("multi",)
    Transfer = "transfer"


class QuestionSource(StrEnum):
    Book = ("Book",)
    IS_2022_07_18 = ("IS_2022_07_18",)
    IS_2022_09_27 = ("IS_2022_09_27",)
    A_2021 = ("A_2021",)
