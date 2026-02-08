from dotenv import load_dotenv
import os
import time
import openai
from openai import OpenAI

load_dotenv()

openai_api_key = os.getenv("OPENAI_API_KEY")

client = OpenAI(api_key=openai_api_key)

assistant_id = "asst_Pvg40TibQ2GIXd267gkfQpaG"

thread = client.beta.threads.create()
print("Thread ID:", thread.id)

client.beta.threads.messages.create(
    thread_id=thread.id,
    role="user",
    content="Мы создаем приложение для управления диетами, хранения показателей здоровья, предоставления рекомендаций по приложение использует номер телефона в виде логина, идентификация пользователя происходит по анкете, содержащей следующие атрибуты: номер телефона, адрес электронной почты, имя, дату рождения, группу крови. В приложение также вносятся данные о росте, весе, артериальном давлении, периодах сна и интенсивных нагрузках. База данных с информацией о пользователе хранится в облачном хранилище PaaS."
)

run = client.beta.threads.runs.create(
    thread_id=thread.id,
    assistant_id=assistant_id
)

while run.status in ("queued", "in_progress"):
    time.sleep(1)
    run = client.beta.threads.runs.retrieve(
        thread_id=thread.id,
        run_id=run.id
    )

messages = client.beta.threads.messages.list(thread_id=thread.id)

print("\n--- Ответы ассистента ---")
for msg in reversed(messages.data):
    if msg.role == "assistant":
        print(msg.content[0].text.value)
