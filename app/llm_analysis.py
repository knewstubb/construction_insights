from openai import OpenAI
from app.models import Feedback
from flask import current_app
import os

# Initialize the OpenAI client
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def analyze_trends(query):
    # Fetch all feedback data
    feedbacks = Feedback.query.all()
    
    # Prepare the data for analysis
    feedback_text = "\n".join([
        f"Date: {f.timestamp}, Highlights: {f.highlights}, Lowlights: {f.lowlights}, Emerging Issues: {f.emerging_issues}"
        for f in feedbacks
    ])
    
    # Prepare the prompt for GPT-4o mini
    prompt = f"""
    As an AI specialized in analyzing construction site feedback, please review the following data and address the query:

    {feedback_text}

    Query: {query}

    Provide a concise, insightful analysis focusing on trends, recurring issues, or notable patterns. If the information is insufficient to answer definitively, state so and suggest what additional data might be helpful.
    """
    
    try:
        # Generate the response using GPT-4o mini
        response = client.chat.completions.create(
            model="gpt-4o-mini",  # Using the GPT-4o mini model
            messages=[
                {"role": "system", "content": "You are a construction site feedback analyst using the latest GPT-4o mini model."},
                {"role": "user", "content": prompt}
            ],
            max_tokens=300,
            n=1,
            stop=None,
            temperature=0.7,
        )
        
        # Extract the generated text from the response
        analysis = response.choices[0].message.content.strip()
        return analysis
    
    except Exception as e:
        current_app.logger.error(f"Error in OpenAI API call: {str(e)}")
        return "An error occurred while analyzing the feedback. Please try again later."