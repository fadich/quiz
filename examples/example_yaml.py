from quiz import (
    CmdQuiz,
    QuizManager,
    from_yaml,
)


class Points:

    def __init__(self):
        self.points = 0

    def increase(self):
        self.points += 1

    def decrease(self):
        self.points -= 1


points = Points()
questions = from_yaml("./examples/resources/example.yml")
quiz_manager = QuizManager(
    questions=questions,
    handlers={
        "increase": points.increase,
        "decrease": points.decrease,
    }
)
quiz = CmdQuiz(quiz_manager=quiz_manager)


if __name__ == '__main__':
    quiz.start_quiz()

    print("###" * 6)
    print(f"### Points: {points.points:>2} ###")
    print("###" * 6)
