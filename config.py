from aiogram import Bot, types
from aiogram.dispatcher import Dispatcher
from aiogram.utils import executor

bot = Bot(token='5423849587:AAFis990LFuyxrOJNG1NYrvHoFloMvesPNQ')
dp = Dispatcher(bot)
async def on_startup(_):
    print('Бот онлайн')

@dp.message_handler(commands="start")
async def cmd_start(message: types.Message):
    poll_keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    poll_keyboard.add(types.KeyboardButton(text='КПК "Содействие"'))
    poll_keyboard.add(types.KeyboardButton(text='КПК "Фин Ит"'))
    poll_keyboard.add(types.KeyboardButton(text='ПК "Контур"'))
    poll_keyboard.add(types.KeyboardButton(text='ООО "АльфаСитиФинанс"'))
    poll_keyboard.add(types.KeyboardButton(text='ООО "Финконсалтинг"'))
    poll_keyboard.add(types.KeyboardButton(text='ООО "Единый центр приема платежей"'))
    poll_keyboard.add(types.KeyboardButton(text='СЛК "Развитие"'))
    poll_keyboard.add(types.KeyboardButton(text='ЛК "Развитие"'))
    poll_keyboard.add(types.KeyboardButton(text="Развитие СК"))
    poll_keyboard.add(types.KeyboardButton(text="ИП Щецов"))
    poll_keyboard.add(types.KeyboardButton(text='БФ "Аллея Победителей"'))#request_poll=types.KeyboardButtonPollType(type=types.PollType.QUIZ)))
    poll_keyboard.add(types.KeyboardButton(text="Отмена"))
    await message.answer("Выберете организацию", reply_markup=poll_keyboard)


@dp.message_handler(lambda message: message.text == 'КПК "Содействие"')
async def action_cancel(message: types.Message):
    remove_keyboard = types.ReplyKeyboardRemove()
    await message.answer("Введите остатки по банку:", reply_markup=remove_keyboard)

@dp.message_handler(lambda message: message.text)
async def action_cancel(message: types.Message):
     remove_keyboard = types.ReplyKeyboardRemove()
     await message.answer("Введите остатки по кассе:", reply_markup=remove_keyboard)

'''@dp.message_handler(lambda message: message.text)
async def action_cancel(message: types.Message):
    remove_keyboard = types.ReplyKeyboardRemove()
    await message.answer("Продолжить заполнение остатков по другой организации?", reply_markup=remove_keyboard)'''

# Хэндлер на текстовое сообщение с текстом “Отмена”
@dp.message_handler(lambda message: message.text == "Отмена")
async def action_cancel(message: types.Message):
    remove_keyboard = types.ReplyKeyboardRemove()
    await message.answer("Действие отменено. Введите /start, чтобы начать заново.", reply_markup=remove_keyboard)


#@dp.message_handler()
#async def echo_send(message: types.Message):
#    await message.reply(message.text)


executor.start_polling(dp, skip_updates=True, on_startup=on_startup)

