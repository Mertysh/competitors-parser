import textwrap as tw 
import asyncio 

from aiogram.utils import executor
from aiogram.types import Message, BotCommand
from aiogram.dispatcher import FSMContext 
from aioschedule import every, run_pending

from excel import table
import pars  
from configure import dp, bot, TG_CLIENT_ID
from state import My_state



async def set_commands():
    await bot.set_my_commands(
        [
            BotCommand('/start', 'Стартовое сообщение'),
            BotCommand('/check', 'Запустить проверку конкурентов'), 
            BotCommand('/table', 'Получить таблицу конкурентов'), 
            BotCommand('/give_table', 'Загрузить таблицу конкурентов'), 
        ]
    )


@dp.message_handler(commands=['start'], state='*')
async def start(message: Message):
    try:
        if message.from_user.id in TG_CLIENT_ID:
            text = tw.dedent(
                f'''\
                Полное описание команд
                /check - Запустить проверку конкурентов     
                /table - Получить таблицу конкурентов     
                /give_table - Загрузить таблицу конкурентов     
                '''
            )
            
            await bot.send_message(message.from_user.id, text)
    except Exception as ex:
            await bot.send_message(message.from_user.id, f'НЕИЗВЕСТНАЯ ОШИБКА!\n({ex})')


@dp.message_handler(commands=['give_table'], state='*')
async def give_offers_command(message: Message):
    if message.from_user.id in TG_CLIENT_ID: 
        await My_state.get_table.set()
        await bot.send_message(message.from_user.id, 'Бот ожидает файл')


@dp.message_handler(content_types=['document'], state=My_state.get_table)
async def give_offers_table(message: Message, state: FSMContext):
    try:    
        file_id = message.document.file_id
        file = await bot.get_file(file_id)

        await bot.download_file(file.file_path, f'./data/table.xlsx')

        await state.reset_state()

        await bot.send_message(message.from_user.id, 'Бот готов выполнять команды')

    except Exception as ex:
        await bot.send_message(message.from_user.id, f'НЕИЗВЕСТНАЯ ОШИБКА!\n({ex})')


@dp.message_handler(commands=['table'], state='*')
async def offers(message: Message):
    try:
        file = table()

        if type(file) == bytes:
            await bot.send_document(message.from_user.id, (f'table.xlsx', file))   
        else:
            await bot.send_message(message.from_user.id, 'Ошибка')

    except Exception as ex:
            await bot.send_message(message.from_user.id, f'НЕИЗВЕСТНАЯ ОШИБКА!\n({ex})')    


@dp.message_handler(commands=['check'], state='*')
async def to_mrc_check_command(message):
    try:
        answer = pars.check()
        if answer != '':
            await bot.send_message(message.from_user.id, answer)

        await bot.send_message(message.from_user.id, 'Бот готов выполнять команды')

    except Exception as ex:
        await bot.send_message(message.from_user.id, f'НЕИЗВЕСТНАЯ ОШИБКА!\n({ex})')


async def check():
    answer = pars.check()
    for user_id in TG_CLIENT_ID:
        if answer != '':
            await bot.send_message(user_id, answer)


async def scheduler():
    every(15).minutes.do(check)

    while True:
        await run_pending()
        await asyncio.sleep(1)


async def to_startup(_):
    asyncio.create_task(scheduler())



if __name__ == '__main__':
    executor.start(dp, set_commands())
    executor.start_polling(dp, skip_updates=True, on_startup=to_startup)
