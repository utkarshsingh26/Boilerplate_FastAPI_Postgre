import pytest
from unittest.mock import MagicMock
from sqlalchemy.orm import Session
from service import QuizService
from repository import QuizRepository
import models

# --- Fixtures ---

@pytest.fixture
def mock_db_session():
    """Creates a mock SQLAlchemy Session."""
    return MagicMock(spec=Session)

@pytest.fixture
def quiz_service(mock_db_session):
    """Initializes the service with a repository using the mock DB."""
    repo = QuizRepository(mock_db_session)
    return QuizService(repo)

# --- Test Cases ---

def test_get_question_with_choices_success(quiz_service, mock_db_session):
    """Ensure the service returns a question when it exists in the DB."""
    # Setup: Mock the repository's get_question return value
    mock_question = models.Questions(id=1, question_text="What is Allomancy?")
    quiz_service.repo.get_question = MagicMock(return_value=mock_question)
    
    result = quiz_service.get_question_with_choices(1)
    
    assert result.id == 1
    assert result.question_text == "What is Allomancy?"
    quiz_service.repo.get_question.assert_called_once_with(1)

def test_get_question_with_choices_not_found(quiz_service):
    """Ensure the service returns None when a question doesn't exist."""
    quiz_service.repo.get_question = MagicMock(return_value=None)
    
    result = quiz_service.get_question_with_choices(999)
    
    assert result is None

def test_create_full_question_coordination(quiz_service, mock_db_session):
    """Tests that the service coordinates question and choice creation correctly."""
    # Mock data for the input
    class MockChoice:
        def __init__(self, text, correct):
            self.choice_text = text
            self.is_correct = correct

    class MockQuestionInput:
        question_text = "Who is the Hero of Ages?"
        choices = [MockChoice("Vin", False), MockChoice("Sazed", True)]

    # Mock the repo methods
    mock_new_q = models.Questions(id=10, question_text=MockQuestionInput.question_text)
    quiz_service.repo.create_question = MagicMock(return_value=mock_new_q)
    quiz_service.repo.create_choice = MagicMock()
    
    # Execute
    result = quiz_service.create_full_question(MockQuestionInput)
    
    # Assertions
    assert result.id == 10
    assert quiz_service.repo.create_question.called
    # Ensure create_choice was called for each choice in the list
    assert quiz_service.repo.create_choice.call_count == 2
    # Ensure the transaction was committed exactly once
    mock_db_session.commit.assert_called_once()
