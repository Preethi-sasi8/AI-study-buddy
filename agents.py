
import os
from dotenv import load_dotenv

load_dotenv()
groq_api_key = os.getenv("GROQ_API_KEY")

from crewai import Agent, Task, Crew, LLM

#  Proper Groq LLM for CrewAI
llm = LLM(
    model="groq/llama-3.3-70b-versatile",
    api_key=groq_api_key
)



explainer = Agent(
    role="Study Explainer",
    goal="Explain topics in simple and easy terms.",
    backstory="You are a helpful teacher who simplifies complex topics.",
    llm=llm,
    verbose=True
)

quiz_creator = Agent(
    role="Quiz Creator",
    goal="Create 3 MCQs with answers.",
    backstory="You generate short quizzes to test understanding.",
    llm=llm,
    verbose=True
)
flashcard_agent = Agent(
    role="Flashcard Creator",
    goal="Generate clear and effective flashcards for revision.",
    backstory=(
        "You are an expert study assistant who creates concise "
        "question-and-answer flashcards to help students revise quickly. "
        "Your flashcards are clear, accurate, and exam-focused."
    ),
    llm=llm,
    verbose=True
)
def run_explainer(topic):

    explain_task = Task(
        description=f"Explain clearly: {topic}",
        expected_output="2-3 paragraph simple explanation.",
        agent=explainer
    )

    crew = Crew(
        agents=[explainer],
        tasks=[explain_task],
        verbose=True
    )

    result = crew.kickoff()
    return result.raw


def run_quiz(topic):
    quiz_task = Task(
        description=f"""
         Create 15 multiple choice questions about {topic}.

         VERY IMPORTANT:
         - Each question must have 4 COMPLETE answer options.
         - Each option must contain real text.
         - Do NOT leave options blank.
         - Mark the correct answer clearly.

         Format EXACTLY like this:

         Question 1: <question text>

         A) <option text>
         B) <option text>
         C) <option text>
         D) <option text>

         Correct Answer: A

         Repeat this format for all 5 questions.
         """,
        expected_output="15 properly formatted MCQs with full options and correct answer.",
        agent=quiz_creator
    )

    crew = Crew(
        agents=[quiz_creator],
        tasks=[quiz_task],
        verbose=True
    )

    result = crew.kickoff()
    return result.raw


def run_flashcards(topic):

    flashcard_task = Task(
        description=f"""
        Create 15 flashcards about {topic}.

        Format EXACTLY like this:

        Flashcard 1:
        Question: <question text>
        Answer: <answer text>

        Flashcard 2:
        Question: <question text>
        Answer: <answer text>

        Continue for 5 flashcards.
        """,
        expected_output="15 flashcards with Question and Answer clearly labeled.",
        agent=flashcard_agent
    )

    crew = Crew(
        agents=[flashcard_agent],
        tasks=[flashcard_task],
        verbose=True
    )

    result = crew.kickoff()
    return result.raw
