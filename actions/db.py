import psycopg2
import openai

DB_CONFIG = {
    "dbname": "yourdb",
    "user": "user",
    "password": "pass",
    "host": "localhost"
}

conn = psycopg2.connect(DB_CONFIG)

def get_embedding(text, model="text-embedding-ada-002"):
    response = openai.Embedding.create(
        input=[text],
        model=model
    )
    return response["data"][0]["embedding"]

def save_message(user_id, user_text, bot_reply):
    with conn.cursor() as cur:
        cur.execute("INSERT INTO chat_history (user_id, user_message, bot_reply) VALUES (%s, %s, %s)",
                    (user_id, user_text, bot_reply))
        conn.commit()

def semantic_search(query):
    embedding = get_embedding(query, model="text-embedding-ada-002")
    with conn.cursor() as cur:
        cur.execute("""
            SELECT text FROM documents ORDER BY embedding <#> %s LIMIT 1;
        """, (embedding,))
        result = cur.fetchone()
    return result[0] if result else ""