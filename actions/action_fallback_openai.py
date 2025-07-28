from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher
from rasa_sdk.events import UserUtteranceReverted
from actions.db import save_message, semantic_search
from classify_intent_openai import classify_new_intent
from append_intent_to_nlu import append_intent
import openai

openai.api_key = ""

class ActionFallbackOpenAI(Action):
    def name(self):
        return "action_fallback_openai"

    def run(self, dispatcher, tracker, domain):
        user_msg = tracker.latest_message.get("text")

        # 1. Semantic Search
        context = semantic_search(user_msg)

        # 2. OpenAI answer
        prompt = f"Context: {context}\nUser: {user_msg}\nAnswer:" 
        response = openai.ChatCompletion.create(
            model="gpt-4",
            messages=[{"role": "user", "content": prompt}]
        )
        answer = response.choices[0].message.content

        # 3. Show answer
        dispatcher.utter_message(answer)

        # 4. Save history
        save_message(tracker.sender_id, user_msg, answer)

        # 5. Optional: Auto intent classification
        result = classify_new_intent(user_msg)
        append_intent(result["intent"], [result["example"]])

        return [UserUtteranceReverted()]