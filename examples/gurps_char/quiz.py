from quiz import (
    CmdQuiz,
    QuizManager,
    from_yaml,
    QuizError,
)

from .character import Character
from .handlers import create_handlers_for


character = Character()


if __name__ == '__main__':
    try:
        questions = from_yaml("./examples/gurps_char/quiz.yml", encoding="utf-8")
        quiz_manager = QuizManager(
            questions=questions,
            handlers=create_handlers_for(character)
        )
        quiz = CmdQuiz(quiz_manager=quiz_manager)
        quiz.start_quiz()

        character.print()
    except QuizError as e:
        print(f"AN ERROR OCCURRED: {str(e)}")

    # input("Press [ENTER] to exit")
