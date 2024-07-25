import datetime
from time import sleep
from decouple import config
import telebot
from telebot.types import Message
from telebot.types import InlineQueryResultArticle, InputTextMessageContent, InlineQuery

TK = config('token')
bot = telebot.TeleBot(TK)


def is_admin(message: Message, user_id: int):
    if user_id in [admin.user.id for admin in bot.get_chat_administrators(message.chat.id)]:
        return True
    else:
        return False


@bot.message_handler(chat_types=["private"], commands=['start'])
def send_hi(message: Message):
    bot.reply_to(message, "به ربات خوش آمدید")


@bot.message_handler(chat_types=['supergroup'], func=lambda message: message.text == "لینک")
def link_sender(message: Message):
    expire_date = datetime.datetime.now() + datetime.timedelta(hours=1)
    expire_date = int(expire_date.timestamp())
    link = bot.create_chat_invite_link(
        message.chat.id,
        name="لینک دعوت",
        expire_date=expire_date,
        creates_join_request=True,
    )
    bot.send_message(message.chat.id, link.invite_link)


@bot.chat_join_request_handler(chat_types=['supergroup'], func=lambda request: True)
def accept_join_members(message: Message):
    bot.approve_chat_join_request(message.chat.id, message.from_user.id)


@bot.message_handler(chat_types=['supergroup'], content_types=['new_chat_members'])
def welcome_new_chat_members(message: Message):
    bot.reply_to(message, f" به گروه خوش امدید{message.from_user.first_name}")


@bot.message_handler(chat_types=['supergroup'], func=lambda message: message.text == "بن" or message.text == "حذف بن")
def ban_unban(message: Message):
    if is_admin(message, message.from_user.id):
        try:
            if message.text == "بن":
                if message.reply_to_message:
                    if not message.from_user.id == message.reply_to_message.from_user.id:
                        if not is_admin(message, message.reply_to_message.from_user.id):
                            bot.ban_chat_member(message.chat.id, message.reply_to_message.from_user.id)
                            bot.reply_to(message, f" بن شد {message.reply_to_message.from_user.first_name}")
                        else:
                            bot.reply_to(message, "شما ادمین ها را نمیتوانید بن کنید")
                    else:
                        bot.reply_to(message, "شما خودتان را نمیتوانید بن کنید")
                else:
                    bot.reply_to(message,
                                 "لطفا روی یکی از پیام های فردی ک میخواهید بن شود ریپلای کنید سپس بن را ارسال کنید")
            elif message.text == "حذف بن":
                if message.reply_to_message:
                    bot.unban_chat_member(message.chat.id, message.reply_to_message.from_user.id)
                    bot.reply_to(message, f" حذف بن شد {message.reply_to_message.from_user.first_name}")
                else:
                    bot.reply_to(message,
                                 "لطفا روی یکی از پیام های فردی ک میخواهید حذف بن شود ریپلای کنید سپس حذف بن را ارسال کنید")
        except:
            bot.reply_to(message, "مشکلی پیش آمده است. ")

    else:
        return


@bot.message_handler(chat_types=['supergroup'], func=lambda message: message.text == "پین" or message.text == "حذف پین")
def pin_unpin(message: Message):
    if is_admin(message, message.from_user.id):
        try:
            if message.text == "پین":
                if message.reply_to_message:
                    bot.pin_chat_message(message.chat.id, message.reply_to_message.id)
                    bot.reply_to(message, "پیام پین شد")
                else:
                    bot.reply_to(message, "لطفا پیام مورد نظر را ریپلای کنید و سپس پین را ارسال کنید ")
            elif message.text == "حذف پین":
                if message.reply_to_message:
                    bot.unpin_chat_message(message.chat.id, message.reply_to_message.id)
                    bot.reply_to(message, "پیام حذف پین شد")
                else:
                    bot.reply_to(message, "لطفا پیام مورد نظر را ریپلای کنید و سپس پین را ارسال کنید ")
        except:
            bot.reply_to(message, "مشکلی پیش آمده است. ")
    else:
        return


@bot.message_handler(chat_types=['supergroup'],
                     func=lambda message: message.text.startswith("سکوت") or message.text == "حذف سکوت")
def silence_r_silence(message: Message):
    if is_admin(message, message.from_user.id):
        try:
            if message.text.startswith("سکوت"):
                if message.reply_to_message:
                    if not message.from_user.id == message.reply_to_message.from_user.id:
                        if not is_admin(message, message.reply_to_message.from_user.id):
                            until_date = None
                            if message.text.split().__len__() > 1:
                                duration = message.text.split()[-1]
                                if duration.isnumeric():
                                    duration = int(duration)
                                    date = datetime.datetime.now() + datetime.timedelta(minutes=duration)
                                    until_date = int(date.timestamp())
                                else:
                                    bot.reply_to(message, "لطفا متن را درست بنویسد \n مثال: (سکوت 10)")
                                    return

                            bot.restrict_chat_member(
                                message.chat.id,
                                message.reply_to_message.from_user.id,
                                can_send_messages=False,
                                can_send_media_messages=False,
                                can_send_polls=False,
                                can_send_other_messages=False,
                                can_invite_users=False,
                                can_change_info=False,
                                can_pin_messages=False,
                                can_add_web_page_previews=False,
                                until_date=until_date,
                            )
                            bot.reply_to(message, f" {message.reply_to_message.from_user.first_name} سکوت شد ")
                        else:
                            bot.reply_to(message, "شما ادمین ها را نمیتوانید سکوت کنید")
                    else:
                        bot.reply_to(message, "شما خودتان را نمیتوانید سکوت کنید")
                else:
                    bot.reply_to(message,
                                 "لطفا روی یکی از پیام های فردی ک میخواهید سکوت شود ریپلای کنید سپس سکوت را ارسال کنید")
            elif message.text == "حذف سکوت":
                if message.reply_to_message:
                    bot.restrict_chat_member(
                        message.chat.id,
                        message.reply_to_message.from_user.id,
                        can_send_messages=True,
                        can_send_media_messages=True,
                        can_send_polls=True,
                        can_send_other_messages=True,
                        can_invite_users=True,
                        can_change_info=True,
                        can_pin_messages=True,
                        can_add_web_page_previews=True,
                    )
                    bot.reply_to(message, f" {message.reply_to_message.from_user.first_name} حذف سکوت شد ")
                else:
                    bot.reply_to(message,
                                 "لطفا روی یکی از پیام های فردی ک میخواهید حذف سکوت شود ریپلای کنید سپس حذف سکوت را ارسال کنید")
        except:
            bot.reply_to(message, "مشکلی پیش آمده است. ")
    else:
        return


@bot.message_handler(chat_types=['supergroup'], func=lambda m: m.text.startswith("پاکسازی"))
def cleaning(message: Message):
    if not is_admin(message, message.from_user.id):
        return
    if message.text.split().__len__() > 1:
        number = message.text.split()[-1]
        if not number.isnumeric():
            help_text = """
            برای پاکسازی تعداد خاصی از پیام ها پیام را به شیوه(مثال : پاکسازی 50) بفرستید.
            """
            bot.reply_to(message, help_text)
        number = int(number)
        messages = []
        for i in range(0, number):
            messages.append(message.id - i)
        bot.delete_messages(message.chat.id, messages)
        m = bot.send_message(message.chat.id, f"{number} پیام حذف شد")
        sleep(10)
        bot.delete_message(message.chat.id, m.id)


@bot.message_handler(chat_types=['supergroup'], func=lambda m: m.text == "ایجاد ادمین" or m.text == "حذف ادمین")
def add_remove_admin(message: Message):
    if not is_admin(message, message.from_user.id):
        return
    if message.text == "ایجاد ادمین":
        if message.reply_to_message:
            if is_admin(message, message.reply_to_message.from_user.id):
                bot.reply_to(message, "کاربر از قبل ادمین است.")
                return
            if message.reply_to_message.from_user == message.from_user:
                return
            try:
                bot.promote_chat_member(
                    message.chat.id,
                    message.reply_to_message.from_user.id,
                    can_pin_messages=True,
                    can_change_info=True,
                    can_invite_users=True,
                    can_edit_messages=True,
                    can_delete_messages=True,
                    can_restrict_members=True,
                    can_manage_voice_chats=True,
                )
                bot.reply_to(message, f"کاربر {message.reply_to_message.from_user.first_name} ارتقا یافت ")
            except:
                bot.reply_to(message, "مشکلی پیش آمده است.\n شاید شما دسترسی برای اضافه یا حذف کردن ادمین را ندارید")
        else:
            bot.reply_to(message, "لطفا روی یکی از پیام های فرد مورد نظر ریپلای کرده و ایجاد ادمین را ارسال کنید")
    if message.text == "حذف ادمین":
        if message.reply_to_message:
            if message.reply_to_message.from_user == message.from_user:
                return
            try:
                bot.promote_chat_member(
                    message.chat.id,
                    message.reply_to_message.from_user.id,
                    can_pin_messages=False,
                    can_change_info=False,
                    can_invite_users=False,
                    can_edit_messages=False,
                    can_delete_messages=False,
                    can_restrict_members=False,
                    can_manage_voice_chats=False,
                )
                bot.reply_to(message, f"کاربر {message.reply_to_message.from_user.first_name} تنزل یافت ")
            except:
                bot.reply_to(message, "مشکلی پیش آمده است.\n شاید شما دسترسی برای اضافه یا حذف کردن ادمین را ندارید")
        else:
            bot.reply_to(message, "لطفا روی یکی از پیام های فرد مورد نظر ریپلای کرده و حذف ادمین را ارسال کنید")


@bot.inline_handler(func=lambda query: len(query.query) == 0)
def inline_query(query: InlineQuery):
    print(query.__class__.__name__)
    items = [
        {
            "id": "1",
            "title": "google",
            "description": "برای لینک گوگل کلیک کنید",
            "thumbnail": "https://i.imgur.com/PFkq3hZ.jpg",
            "message": """کاربر عزیز شما میتوانید با استفاده از لینک زیر وارد شوید
            <a href='google.com'>google</a>""",
        },
        {
            "id": "2",
            "title": "github",
            "description": "برای لینک گیت هاب کلیک کنید",
            "thumbnail": "https://i.imgur.com/EuCNzdP.jpg",
            "message": """کاربر عزیز شما میتوانید با استفاده از لینک زیر وارد شوید
            <a href='github.com'>github</a>""",
        }
    ]
    results = []
    for item in items:
        result = InlineQueryResultArticle(
            id=item["id"],
            description=item["description"],
            title=item["title"],
            thumbnail_url=item["thumbnail"],
            input_message_content=InputTextMessageContent(
                message_text=item["message"],
                parse_mode="HTML",
            )
        )
        results.append(result)
    bot.answer_inline_query(query.id, results)


bot.infinity_polling()
