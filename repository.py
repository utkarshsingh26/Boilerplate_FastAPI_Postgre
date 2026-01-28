from sqlalchemy.orm import Session
import models

class QuizRepository:
    def __init__(self, db: Session):
        self.db = db

    def get_question(self, question_id: int):
        return self.db.query(models.Questions).filter(models.Questions.id == question_id).first()

    def get_choices(self, question_id: int):
        return self.db.query(models.Choices).filter(models.Choices.question_id == question_id).all()

    def create_question(self, text: str):
        db_question = models.Questions(question_text=text)
        self.db.add(db_question)
        self.db.commit()
        self.db.refresh(db_question)
        return db_question

    def create_choice(self, text: str, is_correct: bool, question_id: int):
        db_choice = models.Choices(choice_text=text, is_correct=is_correct, question_id=question_id)
        self.db.add(db_choice)
        # We commit inside the service to handle the transaction as a whole
