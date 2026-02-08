import time
import openai

from openai import OpenAI
from langchain_classic.chains import LLMChain
from langchain_core.prompts import PromptTemplate
from langchain_openai import ChatOpenAI
from langfuse.langchain import CallbackHandler

from dotenv import load_dotenv
import os
from langfuse import observe, get_client

load_dotenv()

# Langfuse ключи (секретный и публичный ключи для аутентификации с Langfuse API)
# установка секретного ключа Langfuse в переменные окружения
os.environ["LANGFUSE_SECRET_KEY"] = os.getenv("LANGFUSE_SECRET_KEY")
# установка публичного ключа Langfuse в переменные окружения
os.environ["LANGFUSE_PUBLIC_KEY"] = os.getenv("LANGFUSE_PUBLIC_KEY")
# установка адреса хоста Langfuse API
os.environ["LANGFUSE_HOST"] = os.getenv("LANGFUSE_HOST")

# Your openai key (ключ API для доступа к OpenAI)
# установка ключа OpenAI API в переменные окружения
os.environ["OPENAI_API_KEY"] = os.getenv("OPENAI_API_KEY")

langfuse_handler = CallbackHandler()


@observe
def conversation(user_input):
 # 1. Подключение к OpenAI API через клиент OpenAI
    client = OpenAI()

    # 2. Указываем ID уже существующего ассистента, который будет выполнять ответы
    assistant_id = "asst_Pvg40TibQ2GIXd267gkfQpaG"

    # 3. Создаем новый поток (thread) для диалога с ассистентом
    thread = client.beta.threads.create()

    # 4. Отправляем сообщение от пользователя в созданный поток
    client.beta.threads.messages.create(
        thread_id=thread.id,
        role="user",
        content=user_input
    )

    # 5. Запускаем ассистента в этом потоке, чтобы он начал отвечать на сообщение
    run = client.beta.threads.runs.create(
        thread_id=thread.id,
        assistant_id=assistant_id
    )

    # 6. Асинхронно ждем завершения генерации модели, проверяя статус с интервалом в 1 секунду
    while run.status in ("queued", "in_progress"):
        time.sleep(1)
        run = client.beta.threads.runs.retrieve(
            thread_id=thread.id,
            run_id=run.id
        )

    # 7. Получаем список всех сообщений в потоке после завершения работы ассистента
    messages = client.beta.threads.messages.list(thread_id=thread.id)

    print("\n--- Ответы ассистента ---")
    # Выводим последний ответ ассистента (самое последнее сообщение с ролью assistant)
    for msg in reversed(messages.data):
        if msg.role == "assistant":
            result = msg.content[0].text.value
            print(msg.content[0].text.value)
            break

    # Возвращаем полученный текст ответа
    return result


# Пример вызова функции conversation с запросом на описание товара
text = conversation('Мы разрабатываем приложение, которое собирает информацию о параметрах здоровья человека с носимого гаджета в реальном времени, информацию о диете и потребляемых калориях, анализирует данные и составляет рекомендации. При регистрации приложение использует номер телефона в качестве ID, пользователь должен заполнить анкету с именем, датой рождения, email, физическими параметрами (рост, вес, группа крови). Данные пользователей хранятся в облачном хранилище. Возможна обработка деперсонифицированной информации пользователей и заказ сравнительных отчетов.')
