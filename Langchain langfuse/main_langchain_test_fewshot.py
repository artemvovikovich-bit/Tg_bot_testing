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
    # Инициализация модели ChatOpenAI с заданным именем модели и температурой (контроль креативности)
    llm = ChatOpenAI(
        model_name="gpt-4.1",
        temperature=0.3,
        top_p=1.0,
        # ключ для доступа к OpenAI API (обычно берется из переменной окружения)
        openai_api_key=os.getenv("OPENAI_API_KEY")
    )
    prompt = PromptTemplate(
        input_variables=["user_input"],
        template="""
    Ты - профессиональный юрист в области законодательства по защите персональных данных, ты анализируешь описание цифрового сервиса на предмет его соответствия законодательству о персональных данных и даешь короткие, конкретные консультации.  Отвечай на основе текстов федеральных законов РФ, указов и постановлений. 
Консультации должны включать в себя следующие разделы:
- нормы закона, которую ты берешь из загруженного контекста и под которую подпадает описание цифрового сервиса, 
- возможные последствия нарушения соответствующих норм, 
- рекомендации по эффективному дизайну сервиса, чтобы обеспечить выполнение норм законодательства, практические примеры и фичи.
Формат вывода – таблица со столбцами: 
- норма закона, 
- последствия нарушения, 
- рекомендация по дизайну, 
- практический пример реализации.


    Запрос пользователя:
      ''''
      {user_input}
      ''''
    
    """
    )

    # Создание цепочки (chain), которая связывает языковую модель (llm) и шаблон промпта (prompt)
    chain = LLMChain(llm=llm, prompt=prompt)

    # Вызов цепочки с передачей user_input; передача langfuse_handler для автоматической трассировки и логирования
    response = chain.invoke({"user_input": user_input}, config={
                            "callbacks": [langfuse_handler]})

    # Выводим результат модели в консоль
    print("Модель:", response['text'])

    # Возвращаем текст ответа для дальнейшего использования
    return response['text']


# Пример вызова функции conversation с запросом на описание товара
text = conversation('Мы разрабатываем приложение, которое собирает информацию о параметрах здоровья человека с носимого гаджета в реальном времени, информацию о диете и потребляемых калориях, анализирует данные и составляет рекомендации. При регистрации приложение использует номер телефона в качестве ID, пользователь должен заполнить анкету с именем, датой рождения, email, физическими параметрами (рост, вес, группа крови). Данные пользователей хранятся в облачном хранилище. Возможна обработка деперсонифицированной информации пользователей и заказ сравнительных отчетов.')
