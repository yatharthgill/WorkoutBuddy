from openai import OpenAI
from app.config.settings import settings

client = OpenAI(
    base_url="https://api.groq.com/openai/v1",
    api_key=settings.GROQ_API_KEY
)

def get_groq_response(user_message: str) -> str:
    try:
        response = client.chat.completions.create(
            model="openai/gpt-oss-20b",
            messages=[
                {"role": "system", "content": "You're a helpful fitness assistant."},
                {"role": "user", "content": user_message}
            ]
        )
        return response.choices[0].message.content.strip()
    except Exception as e:
        return f"⚠️ Error: {str(e)}"
def get_groq_chat_response(user_message: str) -> str:
    try:
        response = client.chat.completions.create(
            model="openai/gpt-oss-20b",
messages = [
    {
        "role": "system",
        "content": (
            "Your name is WorkOutBuddy and tell your name during some answers."
            "You are a helpful and expert fitness assistant. "
            "Only answer questions related to fitness, health, workouts, nutrition, or diet. "
            "If the question is unrelated, politely refuse. "
            "Keep all answers as short and concise as possible."
            
        )
    },
    {"role": "user", "content": user_message}
]

        )
        return response.choices[0].message.content.strip()
    except Exception as e:
        return f"⚠️ Error: {str(e)}"
