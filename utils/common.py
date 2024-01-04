from loader import dp
import keyboards as kb
import os
import aiogram


class Bot:
    def __init__(self, telegram_id: int):
        self.telegram_id = telegram_id

    async def send_file(self, path_file: str, caption_text: str = ''):
        with open(path_file, "rb") as file:
            await dp.bot.send_document(
                chat_id=self.telegram_id,
                document=file,
                caption=caption_text
            )

    async def download_file(self, path_folder: str, file_name: str, message_document: aiogram.types.document.Document):
        folder = f'{path_folder}{self.telegram_id}'

        if not os.path.exists(folder):
            os.makedirs(folder)

        # Очищаем папку пользователя
        await self.clear_user_folder(self.telegram_id, path_folder)

        # Сохраняем файл
        path_file = f'{path_folder}{self.telegram_id}/{file_name}'
        await message_document.download(destination_file=path_file)

    @staticmethod
    async def clear_user_folder(telegram_id: int, path_file: str):
        path = path_file + str(telegram_id) + '/'

        for filename in os.listdir(path):
            file_path = os.path.join(path, filename)
            try:
                if os.path.isfile(file_path):
                    os.remove(file_path)
            except Exception as e:
                print(f'Ошибка при удалении файла {file_path}. {e}')

    async def send_instruction(self, title: str, path: str):
        data = [
            {
                'path_file': f'{path}Инструкция.docx',
                'caption_text': f'Перед тем как приступить - <b>Изучите Инструкцию!</b>',
            },
            {
                'path_file': f'{path}Шаблон.xlsx',
                'caption_text': 'После ознакомления с инструкцией, пожалуйста, заполните <b>Шаблон</b> для загрузки',
            },
        ]

        await dp.bot.send_message(
            chat_id=self.telegram_id,
            text=title,
        )

        for item in data:
            await self.send_file(
                path_file=item['path_file'],
                caption_text=item['caption_text'],
            )

        await dp.bot.send_message(
            chat_id=self.telegram_id,
            text='Пришлите файл EXCEL:',
            reply_markup=kb.back,
        )
