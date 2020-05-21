from telegram import ReplyKeyboardMarkup

#токен
TG_TOKEN = '1098855461:AAGByMnk_vhig8RweeE95G3OkqHtzph7Nyc'

#юзер айди пользователя для обратной связи
TG_FB_USER_ID = '881375721'

#редирект телеграм айпи
TG_API_URL = 'http://telegg.ru/orig/bot'

#кнопки
reply_keyboard_start = [
        ['Товары🎁', 'Адрес и контакты👤'],
        ['Условия оплаты💳 и получения📦'],
        ['Наша группа в 𝕍𝕂 и профиль в 𝕀𝕟𝕤𝕥𝕒𝕘𝕣𝕒𝕞'],
        ['О нас и обратная связь✉']
        ]

reply_keyboard = [
        ['На главную📌']
        ]

reply_keyboard_goods = [
        ['Сувениры🔮', 'Текстиль🎀'],
        ['Мужская одежда👕', 'Женская одежда👚'],
        ['Детская одежда🧣  ', 'Аксессуары для телефона📲'],
        ['На главную📌']
        ]

reply_keyboard_goods_1 = [
        ['Назад🔙', 'На главную📌']
        ]

#свойства кнопок
reply_markup_start = ReplyKeyboardMarkup(
        reply_keyboard_start,
        resize_keyboard=True,
        one_time_keyboard=True)

reply_markup = ReplyKeyboardMarkup(
        reply_keyboard,
        resize_keyboard=True,
        one_time_keyboard=True)

reply_markup_goods = ReplyKeyboardMarkup(
        reply_keyboard_goods,
        resize_keyboard=True,
        one_time_keyboard=True)

reply_markup_goods_1 = ReplyKeyboardMarkup(
        reply_keyboard_goods_1,
        resize_keyboard=True,
        one_time_keyboard=True)
