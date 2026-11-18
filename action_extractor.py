
from llm_service import generate_response


def extract_meeting_insights(transcript):

    # Limit transcript length for faster analysis
    transcript = transcript[:1500]

    prompt = f"""
Analyze this meeting transcript.

Give the result in this format:

SUMMARY:
- Give 2 short points.

DECISIONS:
- List important decisions.

ACTION ITEMS:
- Person - Task - Deadline.

Use simple and clear English.
Do not add information that is not in the transcript.

Transcript:
{transcript}
"""

    return generate_response(prompt)
