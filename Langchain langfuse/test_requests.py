import requests  # Импорт библиотеки requests для выполнения HTTP-запросов
import json  # Импорт модуля json для работы с JSON-данными
from dotenv import load_dotenv
import os
load_dotenv()  # Загрузка переменных окружения из .env файла
api_key = os.getenv("OPENAI_API_KEY")

# URL эндпойнта OpenAI API для создания чат-комплитов
url = "https://api.openai.com/v1/chat/completions"


headers = {
    # Заголовок авторизации с Bearer токеном API ключа
    "Authorization": f"Bearer {api_key}",
    # Указание, что тело запроса будет в формате JSON
    "Content-Type": "application/json"
}


data = {
    "model": "gpt-4o-mini",  # Название модели, с которой происходит взаимодействие
    "messages": [  # Список сообщений для контекста диалога с моделью
        # Сообщение от системы (инструкции для модели)
        {"role": 'system', "content": "Рассказывай о сложных вещах простыми словами. Помни, что примеры из реальной жизни помогают лучше усвоить концепцию."},
        # Сообщение пользователя (вопрос)
        {"role": "user",
            "content": "Опиши в двух предложениях практический смысл натурального логарифма и числа e (экспоненты)."}
    ],
    # Параметр "температура" для управления креативностью модели (меньше - более детерминированный ответ)
    "temperature": 0.5
}

# Отправка POST-запроса к API с заголовками и сериализованными данными JSON
response = requests.post(url, headers=headers, data=json.dumps(data))

# Вывод JSON-ответа в удобном для чтения виде, с поддержкой русских символов
# Вывод HTTP-статуса ответа (например, 200 - успешно)
print(response.status_code)
print(json.dumps(response.json(), indent=2, ensure_ascii=False))
