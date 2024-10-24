import logging
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, ContextTypes, filters
import random

# Enable logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO
)

logger = logging.getLogger(__name__)

# List of repressed words and their modern equivalents
repressed_words = [
    ("абонемент", "передплата"), ("авангард", "передовий загін"), ("агітатор", "пропагандист"),
    ("акціонер", "пайовик"), ("альманах", "збірник"), ("анкетування", "опитування"),
    ("апаратура", "устаткування"), ("артикул", "стаття"), ("асигнування", "виділення коштів"),
    ("аудиторія", "слухачі"), ("балотування", "голосування"), ("бюлетень", "відомість"),
    ("валюта", "грошова одиниця"), ("вендета", "помста"), ("вексель", "боргове зобов'язання"),
    ("виставка", "показ"), ("галантерея", "дрібниці"), ("гарантія", "забезпечення"),
    ("гімназія", "середня школа"), ("гумореска", "жарт"), ("декларація", "заява"),
    ("департамент", "відділ"), ("депозит", "вклад"), ("директива", "наказ"),
    ("дискримінація", "утиск"), ("довідка", "інформація"), ("документ", "папір"),
    ("друкарня", "типографія"), ("економіка", "господарство"), ("експеримент", "дослід"),
    ("експозиція", "виставка"), ("експорт", "вивезення"), ("енциклопедія", "довідник"),
    ("ефект", "вплив"), ("журнал", "періодика"), ("залізниця", "шлях"),
    ("заповідник", "охоронювана територія"), ("засідання", "зустріч"), ("змагання", "конкурс"),
    ("інвестиція", "вкладення"), ("індустрія", "промисловість"), ("інформація", "відомості"),
    ("каталог", "перелік"), ("категорія", "клас"), ("кваліфікація", "фах"),
    ("колекція", "зібрання"), ("комісія", "комітет"), ("конкуренція", "змагання"),
    ("консультація", "радництво"), ("контроль", "нагляд"), ("кооперація", "співпраця"),
    ("кореспондент", "журналіст"), ("критерій", "мірило"), ("література", "писемність"),
    ("магазин", "крамниця"), ("майстерня", "цех"), ("маніфест", "заява"),
    ("маршрут", "шлях"), ("матеріал", "речовина"), ("медаль", "нагорода"),
    ("міграція", "переселення"), ("міністерство", "відомство"), ("модернізація", "оновлення"),
    ("монастир", "обитель"), ("наклад", "видання"), ("науковець", "дослідник"),
    ("об'єктив", "ціль"), ("оголошення", "повідомлення"), ("оригінал", "первинник"),
    ("паралель", "відповідник"), ("паспорт", "посвідчення"), ("переписка", "листування"),
    ("петиція", "звернення"), ("підприємство", "фірма"), ("плакат", "афіша"),
    ("планета", "світ"), ("премія", "нагорода"), ("преса", "видання"),
    ("професія", "фах"), ("регіон", "область"), ("резолюція", "постанова"),
    ("республіка", "держава"), ("реклама", "оголошення"), ("секретар", "писар"),
    ("сенсація", "подія"), ("соціологія", "суспільствознавство"), ("спеціаліст", "фахівець"),
    ("стипендія", "допомога"), ("технологія", "метод"), ("транспорт", "перевезення"),
    ("університет", "виш"), ("факультет", "відділ"), ("федерація", "спілка"),
    ("фестиваль", "свято"), ("філософія", "мудрість"), ("фонд", "засіб"),
    ("фундамент", "основа"), ("хроніка", "літопис"), ("цивілізація", "культура"),
    ("центр", "осередок"), ("цитата", "вислів")
]


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text(
        'Привіт! Я словник репресованих слів. Використовуйте /random для випадкового слова, /repress для репресованого слова до введеного та /modern для перевірки сучасної версії репресованого слова. І секретна команда тільки для адмінів /IamITStepAdmin не вводити нормальним людям'
    )


async def random_word(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    word, modern = random.choice(repressed_words)
    await update.message.reply_text(f'Випадкове репресоване слово: {word} - {modern}')


async def repress_word(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    user_word = ' '.join(context.args)
    if not user_word:
        await update.message.reply_text('Будь ласка, введіть слово після команди /repress.')
        return

    for repressed, modern in repressed_words:
        if modern == user_word:
            await update.message.reply_text(f'Репресоване слово для "{user_word}": {repressed}')
            return

    await update.message.reply_text(f'Не знайдено репресованого слова для "{user_word}".')


async def modern_word(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    repressed_word, modern_word = random.choice(repressed_words)
    await update.message.reply_text(f'Введіть сучасну версію репресованого слова "{repressed_word}":')

    context.user_data['repressed_word'] = repressed_word


async def check_modern_word(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    modern_word = update.message.text
    repressed_word = context.user_data.get('repressed_word')

    if not repressed_word:
        await update.message.reply_text('Будь ласка, спочатку виконайте команду /modern.')
        return

    for repressed, modern in repressed_words:
        if repressed == repressed_word and modern == modern_word:
            await update.message.reply_text(
                f'Правильно! Сучасна версія репресованого слова "{repressed_word}" є "{modern_word}".')
            return

    await update.message.reply_text(
        f'Неправильно. Сучасна версія репресованого слова "{repressed_word}" не є "{modern_word}".')

async def adminit(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text(
        'Адміни ви ЧМИРІ ідіть помийтися досить в камери глядіти'
    )


def main() -> None:
    # Create the Application and pass it your bot's token.
    application = Application.builder().token(
        "7714391246:AAEZL-r6RosWVJYzRd87o2nW0rxI4bGghnI").build()  # Замість 'YOUR_TELEGRAM_BOT_TOKEN' використайте свій токен Telegram бота

    # on different commands - answer in Telegram
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("random", random_word))
    application.add_handler(CommandHandler("repress", repress_word))
    application.add_handler(CommandHandler("modern", modern_word))
    application.add_handler(CommandHandler("IamITStepadmin", adminit))

    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, check_modern_word))

    # Start the Bot
    application.run_polling()


if __name__ == '__main__':
    main()
