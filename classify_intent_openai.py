import openai
import json
openai.api_key = "sk-..."

def classify_new_intent(user_message):
    prompt = f"""
        You are a chatbot NLU classifier. Based on this user message, suggest an intent name and a training example.

        Message: \"{user_message}\"
        Respond in JSON:
        {{
        \"intent\": \"...\",
        \"example\": \"...\"
        }}
    """
    response = openai.ChatCompletion.create(
        model="gpt-4",
        messages=[{"role": "user", "content": prompt}],
        temperature=0
    )
    return json.loads(response.choices[0].message.content.strip())