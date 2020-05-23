import os
import logging
from datetime import datetime
from telegram import Bot
from telegram import ParseMode
from telegram import Update
from telegram import KeyboardButton
from telegram import InlineKeyboardButton
from telegram import InlineKeyboardMarkup
from telegram.ext import CallbackContext
from telegram.ext import CallbackQueryHandler
from telegram.ext import CommandHandler
from telegram.ext import MessageHandler
from telegram.ext import Filters
from telegram.ext import Updater
from telegram.utils.request import Request
from config_teleg import TG_FB_USER_ID, TG_API_URL, reply_keyboard_start, reply_keyboard, reply_keyboard_goods, reply_keyboard_goods_1, reply_markup_start, reply_markup, reply_markup_goods, reply_markup_goods_1
from src_goods import goods_preview, goods_name, goods_description, goods_price, goods_link
#logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)

def info(update, context):
    print("<!----------!>\nПрисоединился(-ась): {0}\nid пользователя: {1}\n<!----------!>".format(update.effective_user.first_name, str(update.effective_user.id)))

#команда выполняется при нажатии 'Старт'
def do_start(update, context):
    update.message.reply_text(
            text='<i>    Добро пожаловать</i> в студию печати «Дарики»!\n    Рады видеть тебя, {0}!'.format(update.effective_user.first_name),
            reply_markup=reply_markup_start,
            parse_mode=ParseMode.HTML,
            )
    info(update, context)

#кнопка 'На главную'
def btn_go_main(update, context):
    update.message.reply_text(
            text='Вы вернулись на главную📌',
            reply_markup=reply_markup_start,
            )

#кнопка 'Адрес и контакты‘
def btn_adress(update, context):
    update.message.reply_text(
            text='Наш адрес:\n<code>Республика Татарстан, с.Большая Атня, ул.Карла Маркса, д.26</code>\n\nНаши контакты:\n<a href="https://vk.com/dariki_116">Зульфат Хабибуллин</a>\n<code>+7 (953) 492-23-45</code> (WhatsApp)\n<code>zulfat.1998@mail.ru</code>\n\n<a href="https://vk.com/id181841864">Гулия Саляхова</a>\n<code>+7 (953) 408-15-62</code> (WhatsApp)\n',
            reply_markup=reply_markup,
            parse_mode=ParseMode.HTML,
            disable_web_page_preview=True,
            )

#кнопка 'Условия оплаты и получения'
def btn_conditions(update, context):
    update.message.reply_text(
            text='<b>    Оплата</b>\n    Опыт показывает что нужно застраховать Вас и себя от необдуманных покупок, поэтому мы иногда можем попросить предоплату, но большинство наших клиентов становятся постоянными и освобождаются от предоплат.'+' Каждый заказ обговаривается индивидуально.\n— Одними из первых принимаем оплату в Вконтакте VK Pay\n— Оплата наличными\n— Перевод на банковскую карту\n— Qiwi, Яндекс.Деньги.'+'\n\n<b>    Получение</b>\n    Самовывоз доступен как с нашего адреса, так и в г.Казани по будням с ул.Н.Ершова.\n    Отправляем по:\n— Почте России\n— Курьерской экспресс-службе\n— Международной доставке\n    Так же можем доставить по г.Казани от 150руб.',
            reply_markup=reply_markup,
            parse_mode=ParseMode.HTML,
            )

#инлайн кнопки с ссылками
def inline_keyboard():
    keyboard_links = [
            [InlineKeyboardButton(
                text='Наша группа в 𝕍𝕂',
                url='https://vk.com/dariki116')],
            [InlineKeyboardButton(
                text='Наш профиль в 𝕀𝕟𝕤𝕥𝕒𝕘𝕣𝕒𝕞',
                url='https://instagram.com/dariki116')]
            ]

    return InlineKeyboardMarkup(keyboard_links)

#кнопка 'Наша группа в ВК...'
def btn_links(update, context):
    update.message.reply_text(
            text='⬇⬇⬇Присоединяйтесь к нам!⬇⬇⬇',
            reply_markup=inline_keyboard()
            )
    update.message.reply_text(
            text='⬆⬆⬆Присоединяйтесь к нам!⬆⬆⬆',
            reply_markup=reply_markup)

#кнопка 'Обратная связь'
def feedback(update, context):
    update.message.reply_text(
            text='<b>    «Дарики»</b> - креативная студия индивидуальных товаров. Работаем только на качественном оборудовании и с качественными материалами. Множество товаров в наличии и под заказ.\n    Отправьте нам свои жалобы; отзывы; замечания; пожелания, и мы обязательно увидим их😊 Нам действительно важно Ваше мнение!\n\n<i>Bot created by </i>@netTatarin<i> with ❤ and ☕</i>',
            reply_markup=reply_markup,
            parse_mode=ParseMode.HTML,
            )

#исполнительная функция обратной связи
def do_feedback(update, context):
    chat_id = update.message.chat_id
    if chat_id == TG_FB_USER_ID:
        error_message = None
        reply = update.message.reply_to_message
        if reply:
            forward_from = reply.forward_from
            if forward_from:
                text = 'Сообщение от автора канала:\n\n' + update.message.text
                context.bot.send_message(
                        chat_id=forward_from.id,
                        text=text,
                )
                update.message.reply_text(
                        text='Сообщение было отправлено',
                        reply_markup=reply_markup,
                        )
            else:
                error_message = 'Нельзя ответить самому себе'
        else:
            error_message = 'Сделайте reply чтобы ответить автору сообщения'

        if error_message is not None:
            update.message.reply_text(
                    text=error_message,
            )
    else:
        update.message.forward(
                chat_id=TG_FB_USER_ID,
                )
        update.message.reply_text(
                text='Сообщение было отправлено',
                reply_markup=reply_markup,
                )

#каталог товаров
def goods(update, context):
    update.message.reply_text(
            text='Выберите категорию товаров:',
            reply_markup=reply_markup_goods,
            )

#раздел сувениры
def goods_suveniry(update, context):
    update.message.reply_text(
            text='Категория товаров\n— Сувениры🔮:'
            )

    goods_suv_1 = [
            '<a href="{0}">&#8205;</a><i>    ⚜Товар</i>:\n📦 {1}\n\n<i>    ⚜Описание</i>:\n📄 {2}\n\n<i>    ⚜Цена</i>:\n<b>💰 {3}</b>\n\n<i>    ⚜Заказать</i>:\n📋 по <a href="{4}">𝕎𝕙𝕒𝕥𝕤𝔸𝕡𝕡</a>’у'.format(goods_preview['prev_suv_1'], goods_name['name_suv_1'], goods_description['desc_suv_1'], goods_price['price_suv_1'], goods_link['link_suv_1'])
    ]

    goods_suv_2 = [
            '<a href="{0}">&#8205;</a><i>    ⚜Товар</i>:\n📦 {1}\n\n<i>    ⚜Описание</i>:\n📄 {2}\n\n<i>    ⚜Цена</i>:\n<b>💰 {3}</b>\n\n<i>    ⚜Заказать</i>:\n📋 по <a href="{4}">𝕎𝕙𝕒𝕥𝕤𝔸𝕡𝕡</a>’у'.format(goods_preview['prev_suv_2'], goods_name['name_suv_2'], goods_description['desc_suv_2'], goods_price['price_suv_2'], goods_link['link_suv_2'])
    ]

    goods_suv_3 = [
            '<a href="{0}">&#8205;</a><i>    ⚜Товар</i>:\n📦 {1}\n\n<i>    ⚜Описание</i>:\n📄 {2}\n\n<i>    ⚜Цена</i>:\n<b>💰 {3}</b>\n\n<i>    ⚜Заказать</i>:\n📋 по <a href="{4}">𝕎𝕙𝕒𝕥𝕤𝔸𝕡𝕡</a>’у'.format(goods_preview['prev_suv_3'], goods_name['name_suv_3'], goods_description['desc_suv_3'], goods_price['price_suv_3'], goods_link['link_suv_3'])
    ]

    goods_suv_4 = [
            '<a href="{0}">&#8205;</a><i>    ⚜Товар</i>:\n📦 {1}\n\n<i>    ⚜Описание</i>:\n📄 {2}\n\n<i>    ⚜Цена</i>:\n<b>💰 {3}</b>\n\n<i>    ⚜Заказать</i>:\n📋 по <a href="{4}">𝕎𝕙𝕒𝕥𝕤𝔸𝕡𝕡</a>’у'.format(goods_preview['prev_suv_4'], goods_name['name_suv_4'], goods_description['desc_suv_4'], goods_price['price_suv_4'], goods_link['link_suv_4'])
    ]

    goods_suv_5 = [
            '<a href="{0}">&#8205;</a><i>    ⚜Товар</i>:\n📦 {1}\n\n<i>    ⚜Описание</i>:\n📄 {2}\n\n<i>    ⚜Цена</i>:\n<b>💰 {3}</b>\n\n<i>    ⚜Заказать</i>:\n📋 по <a href="{4}">𝕎𝕙𝕒𝕥𝕤𝔸𝕡𝕡</a>’у'.format(goods_preview['prev_suv_5'], goods_name['name_suv_5'], goods_description['desc_suv_5'], goods_price['price_suv_5'], goods_link['link_suv_5'])
    ]

    goods_suv_6 = [
            '<a href="{0}">&#8205;</a><i>    ⚜Товар</i>:\n📦 {1}\n\n<i>    ⚜Описание</i>:\n📄 {2}\n\n<i>    ⚜Цена</i>:\n<b>💰 {3}</b>\n\n<i>    ⚜Заказать</i>:\n📋 по <a href="{4}">𝕎𝕙𝕒𝕥𝕤𝔸𝕡𝕡</a>’у'.format(goods_preview['prev_suv_6'], goods_name['name_suv_6'], goods_description['desc_suv_6'], goods_price['price_suv_6'], goods_link['link_suv_6'])
    ]

    goods_suv_7 = [                                          '<a href="{0}">&#8205;</a><i>    ⚜Товар</i>:\n📦 {1}\n\n<i>    ⚜Описание</i>:\n📄 {2}\n\n<i>    ⚜Цена</i>:\n<b>💰 {3}</b>\n\n<i>    ⚜Заказать</i>:\n📋 по <a href="{4}">𝕎𝕙𝕒𝕥𝕤𝔸𝕡𝕡</a>’у'.format(goods_preview['prev_suv_7'], goods_name['name_suv_7'], goods_description['desc_suv_7'], goods_price['price_suv_7'], goods_link['link_suv_7'])
    ]

    goods_suv_8 = [                                          '<a href="{0}">&#8205;</a><i>    ⚜Товар</i>:\n📦 {1}\n\n<i>    ⚜Описание</i>:\n📄 {2}\n\n<i>    ⚜Цена</i>:\n<b>💰 {3}</b>\n\n<i>    ⚜Заказать</i>:\n📋 по <a href="{4}">𝕎𝕙𝕒𝕥𝕤𝔸𝕡𝕡</a>’у'.format(goods_preview['prev_suv_8'], goods_name['name_suv_8'], goods_description['desc_suv_8'], goods_price['price_suv_8'], goods_link['link_suv_8'])
    ]

    goods_suv_9 = [
            '<a href="{0}">&#8205;</a><i>    ⚜Товар</i>:\n📦 {1}\n\n<i>    ⚜Описание</i>:\n📄 {2}\n\n<i>    ⚜Цена</i>:\n<b>💰 {3}</b>\n\n<i>    ⚜Заказать</i>:\n📋 по <a href="{4}">𝕎𝕙𝕒𝕥𝕤𝔸𝕡𝕡</a>’у'.format(goods_preview['prev_suv_9'], goods_name['name_suv_9'], goods_description['desc_suv_9'], goods_price['price_suv_9'], goods_link['link_suv_9'])
    ]

    goods_suv_10 = [
            '<a href="{0}">&#8205;</a><i>    ⚜Товар</i>:\n📦 {1}\n\n<i>    ⚜Описание</i>:\n📄 {2}\n\n<i>    ⚜Цена</i>:\n<b>💰 {3}</b>\n\n<i>    ⚜Заказать</i>:\n📋 по <a href="{4}">𝕎𝕙𝕒𝕥𝕤𝔸𝕡𝕡</a>’у'.format(goods_preview['prev_suv_10'], goods_name['name_suv_10'], goods_description['desc_suv_10'], goods_price['price_suv_10'], goods_link['link_suv_10'])
    ]

    goods_suv_11 = [
            '<a href="{0}">&#8205;</a><i>    ⚜Товар</i>:\n📦 {1}\n\n<i>    ⚜Описание</i>:\n📄 {2}\n\n<i>    ⚜Цена</i>:\n<b>💰 {3}</b>\n\n<i>    ⚜Заказать</i>:\n📋 по <a href="{4}">𝕎𝕙𝕒𝕥𝕤𝔸𝕡𝕡</a>’у'.format(goods_preview['prev_suv_11'], goods_name['name_suv_11'], goods_description['desc_suv_11'], goods_price['price_suv_11'], goods_link['link_suv_11'])
    ]

    update.message.reply_text(
            text='\n'.join(goods_suv_1),
            parse_mode=ParseMode.HTML,
            disable_web_page_preview=False,
            reply_markup=None
            )

    update.message.reply_text(
            text='\n'.join(goods_suv_2),
            parse_mode=ParseMode.HTML,
            disable_web_page_preview=False,
            reply_markup=None
            )

    update.message.reply_text(
            text='\n'.join(goods_suv_3),
            parse_mode=ParseMode.HTML,
            disable_web_page_preview=False,
            reply_markup=None
            )

    update.message.reply_text(
            text='\n'.join(goods_suv_4),
            parse_mode=ParseMode.HTML,
            disable_web_page_preview=False,
            reply_markup=None
            )

    update.message.reply_text(
            text='\n'.join(goods_suv_5),
            parse_mode=ParseMode.HTML,
            disable_web_page_preview=False,
            reply_markup=None
            )

    update.message.reply_text(
            text='\n'.join(goods_suv_6),
            parse_mode=ParseMode.HTML,
            disable_web_page_preview=False,
            reply_markup=None
            )

    update.message.reply_text(
            text='\n'.join(goods_suv_7),
            parse_mode=ParseMode.HTML,
            disable_web_page_preview=False,
            reply_markup=None
            )

    update.message.reply_text(
            text='\n'.join(goods_suv_8),
            parse_mode=ParseMode.HTML,
            disable_web_page_preview=False,
            reply_markup=None
            )

    update.message.reply_text(
            text='\n'.join(goods_suv_9),
            parse_mode=ParseMode.HTML,
            disable_web_page_preview=False,
            reply_markup=None
            )

    update.message.reply_text(
            text='\n'.join(goods_suv_10),
            parse_mode=ParseMode.HTML,
            disable_web_page_preview=False,
            reply_markup=None
            )

    update.message.reply_text(
            text='\n'.join(goods_suv_11),
            parse_mode=ParseMode.HTML,
            disable_web_page_preview=False,
            reply_markup=reply_markup_goods_1
            )

#раздел текстиль
def goods_textil(update, context):

    update.message.reply_text(
            text='Категория товаров\n— Текстиль🎀:',
            )

    goods_tex_1 = [
            '<a href="{0}">&#8205;</a><i>    ⚜Товар</i>:\n📦 {1}\n\n<i>    ⚜Описание</i>:\n📄 {2}\n\n<i>    ⚜Цена</i>:\n<b>💰 {3}</b>\n\n<i>    ⚜Заказать</i>:\n📋 по <a href="{4}">𝕎𝕙𝕒𝕥𝕤𝔸𝕡𝕡</a>’у'.format(goods_preview['prev_tex_1'], goods_name['name_tex_1'], goods_description['desc_tex_1'], goods_price['price_tex_1'], goods_link['link_tex_1'])
    ]

    update.message.reply_text(
            text='\n'.join(goods_tex_1),
            parse_mode=ParseMode.HTML,
            disable_web_page_preview=False,
            reply_markup=reply_markup_goods_1
            )

#раздел мужской одежды
def goods_muzhskaya_odezhda(update, context):
    update.message.reply_text(
            text='Категория товаров\n— Мужская одежда👕:',
            )

    goods_muzh_1 = [
            '<a href="{0}">&#8205;</a><i>    ⚜Товар</i>:\n📦 {1}\n\n<i>    ⚜Описание</i>:\n📄 {2}\n\n<i>⚜Цена</i>:\n<b>💰 {3}</b>\n\n<i>    ⚜Заказать</i>:\n📋 по <a href="{4}">𝕎𝕙𝕒𝕥𝕤𝔸𝕡𝕡</a>’у'.format(goods_preview['prev_muzh_1'], goods_name['name_muzh_1'], goods_description['desc_muzh_1'], goods_price['price_muzh_1'], goods_link['link_muzh_1'])
    ]

    goods_muzh_2 = [
            '<a href="{0}">&#8205;</a><i>    ⚜Товар</i>:\n📦 {1}\n\n<i>    ⚜Описание</i>:\n📄 {2}\n\n<i>⚜Цена</i>:\n<b>💰 {3}</b>\n\n<i>    ⚜Заказать</i>:\n📋 по <a href="{4}">𝕎𝕙𝕒𝕥𝕤𝔸𝕡𝕡</a>’у'.format(goods_preview['prev_muzh_2'], goods_name['name_muzh_2'], goods_description['desc_muzh_2'], goods_price['price_muzh_2'], goods_link['link_muzh_2'])
    ]

    goods_muzh_3 = [
            '<a href="{0}">&#8205;</a><i>    ⚜Товар</i>:\n📦 {1}\n\n<i>    ⚜Описание</i>:\n📄 {2}\n\n<i>⚜Цена</i>:\n<b>💰 {3}</b>\n\n<i>    ⚜Заказать</i>:\n📋 по <a href="{4}">𝕎𝕙𝕒𝕥𝕤𝔸𝕡𝕡</a>’у'.format(goods_preview['prev_muzh_3'], goods_name['name_muzh_3'], goods_description['desc_muzh_3'], goods_price['price_muzh_3'], goods_link['link_muzh_3'])
    ]

    goods_gen_1 = [
            '<a href="{0}">&#8205;</a><i>    ⚜Товар</i>:\n📦 {1}\n\n<i>    ⚜Описание</i>:\n📄 {2}\n\n<i>⚜Цена</i>:\n<b>💰 {3}</b>\n\n<i>    ⚜Заказать</i>:\n📋 по <a href="{4}">𝕎𝕙𝕒𝕥𝕤𝔸𝕡𝕡</a>’у'.format(goods_preview['prev_gen_1'], goods_name['name_gen_1'], goods_description['desc_gen_1'], goods_price['price_gen_1'], goods_link['link_gen_1'])
    ]

    goods_gen_2 = [
            '<a href="{0}">&#8205;</a><i>    ⚜Товар</i>:\n📦 {1}\n\n<i>    ⚜Описание</i>:\n📄 {2}\n\n<i>⚜Цена</i>:\n<b>💰 {3}</b>\n\n<i>    ⚜Заказать</i>:\n📋 по <a href="{4}">𝕎𝕙𝕒𝕥𝕤𝔸𝕡𝕡</a>’у'.format(goods_preview['prev_gen_2'], goods_name['name_gen_2'], goods_description['desc_gen_2'], goods_price['price_gen_2'], goods_link['link_gen_2'])
    ]

    goods_gen_3 = [
            '<a href="{0}">&#8205;</a><i>    ⚜Товар</i>:\n📦 {1}\n\n<i>    ⚜Описание</i>:\n📄 {2}\n\n<i>⚜Цена</i>:\n<b>💰 {3}</b>\n\n<i>    ⚜Заказать</i>:\n📋 по <a href="{4}">𝕎𝕙𝕒𝕥𝕤𝔸𝕡𝕡</a>’у'.format(goods_preview['prev_gen_3'], goods_name['name_gen_3'], goods_description['desc_gen_3'], goods_price['price_gen_3'], goods_link['link_gen_3'])
    ]

    goods_gen_4 = [
            '<a href="{0}">&#8205;</a><i>    ⚜Товар</i>:\n📦 {1}\n\n<i>    ⚜Описание</i>:\n📄 {2}\n\n<i>⚜Цена</i>:\n<b>💰 {3}</b>\n\n<i>    ⚜Заказать</i>:\n📋 по <a href="{4}">𝕎𝕙𝕒𝕥𝕤𝔸𝕡𝕡</a>’у'.format(goods_preview['prev_gen_4'], goods_name['name_gen_4'], goods_description['desc_gen_4'], goods_price['price_gen_4'], goods_link['link_gen_4'])
    ]

    goods_gen_5 = [
            '<a href="{0}">&#8205;</a><i>    ⚜Товар</i>:\n📦 {1}\n\n<i>    ⚜Описание</i>:\n📄 {2}\n\n<i>⚜Цена</i>:\n<b>💰 {3}</b>\n\n<i>    ⚜Заказать</i>:\n📋 по <a href="{4}">𝕎𝕙𝕒𝕥𝕤𝔸𝕡𝕡</a>’у'.format(goods_preview['prev_gen_5'], goods_name['name_gen_5'], goods_description['desc_gen_5'], goods_price['price_gen_5'], goods_link['link_gen_5'])
    ]

    update.message.reply_text(
            text='\n'.join(goods_muzh_1),
            parse_mode=ParseMode.HTML,
            disable_web_page_preview=False,
            reply_markup=None
            )

    update.message.reply_text(
            text='\n'.join(goods_muzh_2),
            parse_mode=ParseMode.HTML,
            disable_web_page_preview=False,
            reply_markup=None
            )

    update.message.reply_text(
            text='\n'.join(goods_muzh_3),
            parse_mode=ParseMode.HTML,
            disable_web_page_preview=False,
            reply_markup=None
            )

    update.message.reply_text(
            text='\n'.join(goods_gen_1),
            parse_mode=ParseMode.HTML,
            disable_web_page_preview=False,
            reply_markup=None
            )

    update.message.reply_text(
            text='\n'.join(goods_gen_2),
            parse_mode=ParseMode.HTML,
            disable_web_page_preview=False,
            reply_markup=None
            )

    update.message.reply_text(
            text='\n'.join(goods_gen_3),
            parse_mode=ParseMode.HTML,
            disable_web_page_preview=False,
            reply_markup=None
            )

    update.message.reply_text(
            text='\n'.join(goods_gen_4),
            parse_mode=ParseMode.HTML,
            disable_web_page_preview=False,
            reply_markup=None
            )

    update.message.reply_text(
            text='\n'.join(goods_gen_5),
            parse_mode=ParseMode.HTML,
            disable_web_page_preview=False,
            reply_markup=reply_markup_goods_1
            )

#раздел женской одежды
def goods_zhenskaya_odezhda(update, context):
    update.message.reply_text(
            text='Категория товаров\n— Женская одежда👚:',
            )

    goods_zhen_1 = [
            '<a href="{0}">&#8205;</a><i>    ⚜Товар</i>:\n📦 {1}\n\n<i>    ⚜Описание</i>:\n📄 {2}\n\n<i>⚜Цена</i>:\n<b>💰 {3}</b>\n\n<i>    ⚜Заказать</i>:\n📋 по <a href="{4}">𝕎𝕙𝕒𝕥𝕤𝔸𝕡𝕡</a>’у'.format(goods_preview['prev_zhen_1'], goods_name['name_zhen_1'], goods_description['desc_zhen_1'], goods_price['price_zhen_1'], goods_link['link_zhen_1'])
    ]

    goods_zhen_2 = [
            '<a href="{0}">&#8205;</a><i>    ⚜Товар</i>:\n📦 {1}\n\n<i>    ⚜Описание</i>:\n📄 {2}\n\n<i>⚜Цена</i>:\n<b>💰 {3}</b>\n\n<i>    ⚜Заказать</i>:\n📋 по <a href="{4}">𝕎𝕙𝕒𝕥𝕤𝔸𝕡𝕡</a>’у'.format(goods_preview['prev_zhen_2'], goods_name['name_zhen_2'], goods_description['desc_zhen_2'], goods_price['price_zhen_2'], goods_link['link_zhen_2'])
    ]

    goods_zhen_3 = [
            '<a href="{0}">&#8205;</a><i>    ⚜Товар</i>:\n📦 {1}\n\n<i>    ⚜Описание</i>:\n📄 {2}\n\n<i>⚜Цена</i>:\n<b>💰 {3}</b>\n\n<i>    ⚜Заказать</i>:\n📋 по <a href="{4}">𝕎𝕙𝕒𝕥𝕤𝔸𝕡𝕡</a>’у'.format(goods_preview['prev_zhen_3'], goods_name['name_zhen_3'], goods_description['desc_zhen_3'], goods_price['price_zhen_3'], goods_link['link_zhen_3'])
    ]

    goods_gen_1 = [
            '<a href="{0}">&#8205;</a><i>    ⚜Товар</i>:\n📦 {1}\n\n<i>    ⚜Описание</i>:\n📄 {2}\n\n<i>⚜Цена</i>:\n<b>💰 {3}</b>\n\n<i>    ⚜Заказать</i>:\n📋 по <a href="{4}">𝕎𝕙𝕒𝕥𝕤𝔸𝕡𝕡</a>’у'.format(goods_preview['prev_gen_1'], goods_name['name_gen_1'], goods_description['desc_gen_1'], goods_price['price_gen_1'], goods_link['link_gen_1'])
    ]

    goods_gen_2 = [
            '<a href="{0}">&#8205;</a><i>    ⚜Товар</i>:\n📦 {1}\n\n<i>    ⚜Описание</i>:\n📄 {2}\n\n<i>⚜Цена</i>:\n<b>💰 {3}</b>\n\n<i>    ⚜Заказать</i>:\n📋 по <a href="{4}">𝕎𝕙𝕒𝕥𝕤𝔸𝕡𝕡</a>’у'.format(goods_preview['prev_gen_2'], goods_name['name_gen_2'], goods_description['desc_gen_2'], goods_price['price_gen_2'], goods_link['link_gen_2'])
    ]

    goods_gen_3 = [
            '<a href="{0}">&#8205;</a><i>    ⚜Товар</i>:\n📦 {1}\n\n<i>    ⚜Описание</i>:\n📄 {2}\n\n<i>⚜Цена</i>:\n<b>💰 {3}</b>\n\n<i>    ⚜Заказать</i>:\n📋 по <a href="{4}">𝕎𝕙𝕒𝕥𝕤𝔸𝕡𝕡</a>’у'.format(goods_preview['prev_gen_3'], goods_name['name_gen_3'], goods_description['desc_gen_3'], goods_price['price_gen_3'], goods_link['link_gen_3'])
    ]

    goods_gen_4 = [
            '<a href="{0}">&#8205;</a><i>    ⚜Товар</i>:\n📦 {1}\n\n<i>    ⚜Описание</i>:\n📄 {2}\n\n<i>⚜Цена</i>:\n<b>💰 {3}</b>\n\n<i>    ⚜Заказать</i>:\n📋 по <a href="{4}">𝕎𝕙𝕒𝕥𝕤𝔸𝕡𝕡</a>’у'.format(goods_preview['prev_gen_4'], goods_name['name_gen_4'], goods_description['desc_gen_4'], goods_price['price_gen_4'], goods_link['link_gen_4'])
    ]

    goods_gen_5 = [
            '<a href="{0}">&#8205;</a><i>    ⚜Товар</i>:\n📦 {1}\n\n<i>    ⚜Описание</i>:\n📄 {2}\n\n<i>⚜Цена</i>:\n<b>💰 {3}</b>\n\n<i>    ⚜Заказать</i>:\n📋 по <a href="{4}">𝕎𝕙𝕒𝕥𝕤𝔸𝕡𝕡</a>’у'.format(goods_preview['prev_gen_5'], goods_name['name_gen_5'], goods_description['desc_gen_5'], goods_price['price_gen_5'], goods_link['link_gen_5'])
    ]

    update.message.reply_text(
            text='\n'.join(goods_zhen_1),
            parse_mode=ParseMode.HTML,
            disable_web_page_preview=False,
            reply_markup=None
            )

    update.message.reply_text(
            text='\n'.join(goods_zhen_2),
            parse_mode=ParseMode.HTML,
            disable_web_page_preview=False,
            reply_markup=None
            )

    update.message.reply_text(
            text='\n'.join(goods_zhen_3),
            parse_mode=ParseMode.HTML,
            disable_web_page_preview=False,
            reply_markup=None
            )

    update.message.reply_text(
            text='\n'.join(goods_gen_1),
            parse_mode=ParseMode.HTML,
            disable_web_page_preview=False,
            reply_markup=None
            )

    update.message.reply_text(
            text='\n'.join(goods_gen_2),
            parse_mode=ParseMode.HTML,
            disable_web_page_preview=False,
            reply_markup=None
            )

    update.message.reply_text(
            text='\n'.join(goods_gen_3),
            parse_mode=ParseMode.HTML,
            disable_web_page_preview=False,
            reply_markup=None
            )

    update.message.reply_text(
            text='\n'.join(goods_gen_4),
            parse_mode=ParseMode.HTML,
            disable_web_page_preview=False,
            reply_markup=None
            )

    update.message.reply_text(
            text='\n'.join(goods_gen_5),
            parse_mode=ParseMode.HTML,
            disable_web_page_preview=False,
            reply_markup=reply_markup_goods_1
            )

#раздел детской одежды
def goods_detskaya_odezhda(update, context):
    update.message.reply_text(
            text='Категория товаров\n— Детская одежда🧣:',
            )

    goods_dets_1 = [
            '<a href="{0}">&#8205;</a><i>    ⚜Товар</i>:\n📦 {1}\n\n<i>    ⚜Описание</i>:\n📄 {2}\n\n<i>⚜Цена</i>:\n<b>💰 {3}</b>\n\n<i>    ⚜Заказать</i>:\n📋 по <a href="{4}">𝕎𝕙𝕒𝕥𝕤𝔸𝕡𝕡</a>’у'.format(goods_preview['prev_dets_1'], goods_name['name_dets_1'], goods_description['desc_dets_1'], goods_price['price_dets_1'], goods_link['link_dets_1'])
    ]

    goods_dets_2 = [
            '<a href="{0}">&#8205;</a><i>    ⚜Товар</i>:\n📦 {1}\n\n<i>    ⚜Описание</i>:\n📄 {2}\n\n<i>⚜Цена</i>:\n<b>💰 {3}</b>\n\n<i>    ⚜Заказать</i>:\n📋 по <a href="{4}">𝕎𝕙𝕒𝕥𝕤𝔸𝕡𝕡</a>’у'.format(goods_preview['prev_dets_2'], goods_name['name_dets_2'], goods_description['desc_dets_2'], goods_price['price_dets_2'], goods_link['link_dets_2'])
    ]

    goods_gen_4 = [
    '<a href="{0}">&#8205;</a><i>    ⚜Товар</i>:\n📦 {1}\n\n<i>    ⚜Описание</i>:\n📄 {2}\n\n<i>⚜Цена</i>:\n<b>💰 {3}</b>\n\n<i>    ⚜Заказать</i>:\n📋 по <a href="{4}">𝕎𝕙𝕒𝕥𝕤𝔸𝕡𝕡</a>’у'.format(goods_preview['prev_gen_4'], goods_name['name_gen_4'], goods_description['desc_gen_4'], goods_price['price_gen_4'], goods_link['link_gen_4'])
    ]

    goods_gen_5 = [
            '<a href="{0}">&#8205;</a><i>    ⚜Товар</i>:\n📦 {1}\n\n<i>    ⚜Описание</i>:\n📄 {2}\n\n<i>⚜Цена</i>:\n<b>💰 {3}</b>\n\n<i>    ⚜Заказать</i>:\n📋 по<a href="{4}">𝕎𝕙𝕒𝕥𝕤𝔸𝕡𝕡</a>’у'.format(goods_preview['prev_gen_5'], goods_name['name_gen_5'], goods_description['desc_gen_5'], goods_price['price_gen_5'], goods_link['link_gen_5'])
    ]

    update.message.reply_text(
            text='\n'.join(goods_dets_1),
            parse_mode=ParseMode.HTML,
            disable_web_page_preview=False,
            reply_markup=None                                     )

    update.message.reply_text(
            text='\n'.join(goods_dets_2),
            parse_mode=ParseMode.HTML,
            disable_web_page_preview=False,
            reply_markup=None
            )

    update.message.reply_text(
            text='\n'.join(goods_gen_4),
            parse_mode=ParseMode.HTML,
            disable_web_page_preview=False,
            reply_markup=None
            )

    update.message.reply_text(
            text='\n'.join(goods_gen_5),
            parse_mode=ParseMode.HTML,
            disable_web_page_preview=False,
            reply_markup=reply_markup_goods_1
            )

#раздел аксессуаров
def goods_aksessuary(update, context):
    update.message.reply_text(
            text='Категория товаров\n— Аксессуары для телефона📲:',
            )

    goods_aks_1 = [
            '<a href="{0}">&#8205;</a><i>    ⚜Товар</i>:\n📦 {1}\n\n<i>    ⚜Описание</i>:\n📄 {2}\n\n<i>⚜Цена</i>:\n<b>💰 {3}</b>\n\n<i>    ⚜Заказать</i>:\n📋 по <a href="{4}">𝕎𝕙𝕒𝕥𝕤𝔸𝕡𝕡</a>’у'.format(goods_preview['prev_aks_1'], goods_name['name_aks_1'], goods_description['desc_aks_1'], goods_price['price_aks_1'], goods_link['link_aks_1'])
    ]

    goods_aks_2 = [
            '<a href="{0}">&#8205;</a><i>    ⚜Товар</i>:\n📦 {1}\n\n<i>    ⚜Описание</i>:\n📄 {2}\n\n<i>⚜Цена</i>:\n<b>💰 {3}</b>\n\n<i>    ⚜Заказать</i>:\n📋 по <a href="{4}">𝕎𝕙𝕒𝕥𝕤𝔸𝕡𝕡</a>’у'.format(goods_preview['prev_aks_2'], goods_name['name_aks_2'], goods_description['desc_aks_2'], goods_price['price_aks_2'], goods_link['link_aks_2'])
    ]

    update.message.reply_text(
            text='\n'.join(goods_aks_1),
            parse_mode=ParseMode.HTML,
            disable_web_page_preview=False,
            reply_markup=None
            )

    update.message.reply_text(
            text='\n'.join(goods_aks_2),
            parse_mode=ParseMode.HTML,
            disable_web_page_preview=False,
            reply_markup=reply_markup_goods_1
            )

#основа основ. запуск бота
def main():
    token = os.environ['TG_TOKEN']

    req = Request(
            connect_timeout=0.5,
            read_timeout=1.0,
            )
    bot = Bot(
            token=token,
            request=req,
            base_url=TG_API_URL,
            )
    updater = Updater(
            bot=bot,
            use_context=True,
            )
    print('Бот запускается...')

    start_handler = CommandHandler('start', do_start)
    go_main_handler = MessageHandler(Filters.regex('^(На главную📌)$'), btn_go_main)
    contacts_handler = MessageHandler(Filters.regex('^(Адрес и контакты👤)$'), btn_adress)
    conditions_handler = MessageHandler(Filters.regex('^(Условия оплаты💳 и получения📦)$'), btn_conditions)
    links_handler = MessageHandler(Filters.regex('^(Наша группа в 𝕍𝕂 и профиль в 𝕀𝕟𝕤𝕥𝕒𝕘𝕣𝕒𝕞)$'), btn_links)
    feedback_handler = MessageHandler(Filters.regex('^(О нас и обратная связь✉)$'), feedback)
    goods_handler = MessageHandler(Filters.regex('^(Товары🎁)$'), goods)
    back_to_goods_handler = MessageHandler(Filters.regex('^(Назад🔙)$'), goods)

    goods_1_handler = MessageHandler(Filters.regex('^(Сувениры🔮)$'), goods_suveniry)
    goods_2_handler = MessageHandler(Filters.regex('^(Текстиль🎀)$'), goods_textil)
    goods_3_handler = MessageHandler(Filters.regex('^(Мужская одежда👕)$'), goods_muzhskaya_odezhda)
    goods_4_handler = MessageHandler(Filters.regex('^(Женская одежда👚)$'), goods_zhenskaya_odezhda)
    goods_5_handler = MessageHandler(Filters.regex('^(Детская одежда🧣)$'), goods_detskaya_odezhda)
    goods_6_handler = MessageHandler(Filters.regex('^(Аксессуары для телефона📲)$'), goods_aksessuary)

    do_feedback_handler = MessageHandler(Filters.all, do_feedback)

    dp = updater.dispatcher.add_handler

    dp(start_handler)
    dp(go_main_handler)
    dp(contacts_handler)
    dp(conditions_handler)
    dp(links_handler)
    dp(feedback_handler)
    dp(goods_handler)
    dp(back_to_goods_handler)

    dp(goods_1_handler)
    dp(goods_2_handler)
    dp(goods_3_handler)
    dp(goods_4_handler)
    dp(goods_5_handler)
    dp(goods_6_handler)

    dp(do_feedback_handler)

    updater.start_polling()
    print('Бот запущен!')
    updater.idle()


if __name__ == '__main__':
    main()
