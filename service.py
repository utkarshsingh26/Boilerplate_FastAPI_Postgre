from repository import QuizRepository

class QuizService:
    def __init__(self, repo: QuizRepository):
        self.repo = repo

    def get_question_with_choices(self, question_id: int):
        question = self.repo.get_question(question_id)
        if not question:
            return None
        return question

    def create_full_question(self, question_data):
        # Business logic: Create the question first
        new_q = self.repo.create_question(question_data.question_text)
        
        # Then create all associated choices
        for choice in question_data.choices:
            self.repo.create_choice(choice.choice_text, choice.is_correct, new_q.id)
            
        self.repo.db.commit() # Finalize the transaction
        return new_q
