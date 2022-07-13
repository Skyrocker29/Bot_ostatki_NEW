from aiogram import types, Dispatcher
from create import dp, bot
from keyboards import kb, kb_undo, bank_list
from aiogram.types import ReplyKeyboardRemove
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Text
from aiogram.dispatcher.filters.state import State, StatesGroup
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart


class FSMAdmin(StatesGroup):
    bank = State()
    kassa = State()
    enterprice = State()

async def command_start(message: types.Message):
    await message.delete()
    await FSMAdmin.bank.set()
    await message.answer('Выберите организацию', reply_markup=kb)

async def cancel_handler(message: types.Message, state: FSMContext):
    current_state = await state.get_state()
    if current_state is None:
        return
    await state.finish()
    await message.answer('Отменено')
    await FSMAdmin.bank.set()
    await message.answer('Выберите организацию', reply_markup=kb)

async def fsm_bank(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['bank'] = message.text
    await FSMAdmin.next()
    await message.answer(message.text, reply_markup=ReplyKeyboardRemove())
    await message.answer('Введите остатки по кассе:', reply_markup=kb_undo)

async def fsm_kassa(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['kassa'] = message.text
    await FSMAdmin.next()
    await message.answer('Введите остатки по банку:')

async def fsm_enterprice(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['enterprice'] = message.text
    async with state.proxy() as data:
        await message.answer(
            '*Организация*:  ' + data['bank'] + '\n' +
            '*Остатки по кассе*:  ' + data['kassa'] + '\n' +
            '*Остатки по банку*:  ' + data['enterprice'],
        reply_markup=ReplyKeyboardRemove(), parse_mode='Markdown')

        email_sendler = "it1@lizing-p.ru"
        password = "tzDp3ZmuMi4U"
        email_getter = "it1@lizing-p.ru"

        msg = MIMEMultipart()
        msg['From'] = email_getter
        msg['To'] = email_sendler
        msg['Subject'] = 'Остатки средств по ' + data['bank']

        smtp_server = smtplib.SMTP("mail.nic.ru", 587)
        smtp_server.starttls()

        table = {"Организация": data['bank'], "Остатки по банку": data['enterprice'], "Остатки по кассе": data['kassa']},{"Организация": data['bank'], "Остатки по банку": data['enterprice'], "Остатки по кассе": data['kassa']}
        result = ''
        for i in table:
            result += f"<tr><td>{i['Организация']}</td><td>{i['Остатки по банку']}</td><td>{i['Остатки по кассе']}</td></tr>"

        html = f"""\
               <html>
                 <head></head>
                 <body>
                       <table border="1">
                           <tr>
                               <th>Организация</th>
                               <th>Остатки по банку</th>
                               <th>Остатки по кассе</th>
                           </tr>
                           {result}
                       </table>
                 </body>
               </html>
               """
        msg.attach(MIMEText(html, 'html', 'utf-8'))

        server = smtplib.SMTP("mail.nic.ru", 587)  # Создаем объект SMTP
        server.set_debuglevel(True)  # Включаем режим отладки - если отчет не нужен, строку можно закомментировать
        server.starttls()  # Начинаем шифрованный обмен по TLS
        server.login(email_sendler, password)  # Получаем доступ
        server.send_message(msg)  # Отправляем сообщение
        server.quit()


    await state.finish()
    await FSMAdmin.bank.set()
    await message.answer('Выберите организацию', reply_markup=kb)

def register_handlers_client(dp: Dispatcher):
    dp.register_message_handler(command_start, commands='start', state='*')
    dp.register_message_handler(command_start, Text(equals='сохранить', ignore_case=True), state=None)
    dp.register_message_handler(fsm_bank, lambda message: message.text in bank_list, state=FSMAdmin.bank)
    dp.register_message_handler(cancel_handler, state='*', commands='отмена')
    dp.register_message_handler(cancel_handler, Text(equals='отмена', ignore_case=True), state='*')
    dp.register_message_handler(fsm_kassa, state=FSMAdmin.kassa)
    dp.register_message_handler(fsm_enterprice, state=FSMAdmin.enterprice)
