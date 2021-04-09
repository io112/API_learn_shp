import os
from typing import List

from telebot import TeleBot
from telebot.types import InlineQuery, InlineQueryResultArticle, InputTextMessageContent

api_key = os.getenv('API_KEY', 'define me')

bot = TeleBot(api_key)


class QueryValidator:
    def __init__(self):
        self.query = ''
        self.errors = []

    def validate(self) -> List[str]:
        if len(self.query.split()) != 2:
            self.errors.append('Некорретное количество аргументов')
            return self.errors
        a, b = self.query.split()
        if not a.isdigit():
            self.errors.append('Первый аргумент не число')
        if not b.isdigit():
            self.errors.append('Второй аргумент не число')
        return self.errors


@bot.inline_handler(func=lambda q: len(q.query) > 0)
def receive(q: InlineQuery):
    validator = QueryValidator()
    validator.query = q.query
    errors = validator.validate()
    result = []
    if len(errors) != 0:
        for error in errors:
            result.append(
                InlineQueryResultArticle(
                    id=f'error_{error[:3]}',  # ID отправляемого пользователю ответа
                    title='Ошибка',  # Заголовок
                    description=error,  # Текст описания (в нашем случае — ошибка)
                    input_message_content=InputTextMessageContent(  # Что отправляется при нажатии на этот вариант
                        message_text='Ошибка при вычислении'
                    )
                )
            )
    else:
        a, b = map(int, q.query.split())
        result.append(InlineQueryResultArticle(
            id='success',
            title='Результат',
            description=str(a + b),
            input_message_content=InputTextMessageContent(
                message_text=f'Результат: {a + b}'
            )
        ))
    bot.answer_inline_query(q.id, result)


if __name__ == '__main__':
    bot.polling(none_stop=True)
