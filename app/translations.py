# app/translations.py - v1.0 HYBRID (Gemini's structure + Claude's logging)
"""
Translation system with DB-first approach and three-tier fallback.
In-memory cache loaded on startup for synchronous access.
"""
import logging
from typing import Dict, Optional

# ============================================================================
# IN-MEMORY CACHE (loaded from DB on startup)
# ============================================================================
_TRANSLATION_CACHE: Dict[str, Dict[str, str]] = {}

# ============================================================================
# FALLBACK DEFAULTS (hardcoded safety net from v0.8)
# ============================================================================
TEXTS_DEFAULTS = {
    "ru": {
        "welcome": "Добро пожаловать. Пожалуйста, выберите язык.",
        "menu_consultation": "Запись на консультацию",
        "menu_terms": "Условия работы",
        "menu_qual": "Квалификация",
        "menu_about": "О психотерапии",
        "btn_online": "Онлайн-консультация",
        "btn_onsite": "Очная консультация",
        "btn_individual": "Индивидуальная консультация — 60 минут ({price})",
        "btn_couple": "Консультация для пар — 90 минут ({price})",
        "ask_timezone": "Пожалуйста, укажите ваш часовой пояс (например, UTC+3, Москва).",
        "ask_time": "Консультации проходят по ереванскому времени (GMT+4).\nПриём возможен по пятницам и субботам в первой половине дня.\n\nЕсли эти условия вам подходят, пожалуйста, продолжите —\nспециалист предложит доступные варианты времени.",
        "ask_problem": "Если хотите, кратко опишите то, с чем вы хотели бы обратиться.",
        "ask_address": "Как к вам обращаться?",
        "ask_comm": "Какой способ связи для вас предпочтительнее?\n(Telegram, WhatsApp, Viber, Zoom)?",
        "skip": "Пропустить",
        "confirm_sent": "Спасибо.\nВаш запрос отправлен. Я свяжусь с вами в ближайшее время.",
        "waitlist_intro": "К сожалению, сейчас нет свободных мест. Вы можете оставить заявку в лист ожидания.",
        "waitlist_contacts": "Пожалуйста, оставьте ваши контакты для связи.",
        "error_generic": "Произошла ошибка. Пожалуйста, попробуйте позже.",
        "negotiation_new": "Новое предложение от терапевта:\n\n{msg}",
        "btn_agree": "Согласиться",
        "btn_counter": "Предложить другое время",
        "negotiation_agreed": "Время согласовано: {time}",
        "negotiation_rejected": "Заявка отклонена.",
        "status_confirmed": "Встреча подтверждена!",
        "file_not_found": "Информация пока не добавлена.",
        "menu_home": "🏠 Домой",
        "welcome_back": "Вы вернулись в главное меню.",
        "booking_cancelled": "Запись отменена. Вы вернулись в главное меню.",
        # v1.0.3: Reminder translations
        "reminder_24h": "🔔 Напоминание: Ваша консультация завтра!\n\n📅 Время: {time}\n\nДо встречи!",
        "reminder_1h": "🔔 Напоминание: Ваша консультация начнётся через 1 час!\n\n📅 Время: {time}\n\nПожалуйста, будьте готовы!",
        # v1.0.5: Therapist in the loop
        "booking_pending_review": (
            "✅ <b>Заявка принята!</b>\n\n"
            "📅 Выбранное время: {time}\n"
            "🆔 Номер: {request_id}\n\n"
            "⏳ Ожидайте подтверждения от психотерапевта."
        ),
        "booking_approved": (
            "✅ <b>Запись подтверждена!</b>\n\n"
            "📅 {time}\n\n"
            "Я свяжусь с вами для уточнения деталей."
        ),
        "booking_rejected": (
            "К сожалению, выбранное время недоступно.\n\n"
            "Пожалуйста, выберите другое время или свяжитесь со мной напрямую."
        ),
        "slot_unavailable": "❌ К сожалению, это время уже занято. Пожалуйста, выберите другое.",
    },
    "am": {
        "welcome": "Բարի գալուստ: Խնդրում ենք ընտրել լեզուն:",
        "menu_consultation": "Գրանցվել խորհրդատվության",
        "menu_terms": "Աշխատանքի պայմաններ",
        "menu_qual": "Մասնագետի որակավորում",
        "menu_about": "Հոգեթերապիայի մասին",
        "btn_online": "Առցանց խորհրդատվություն",
        "btn_onsite": "Առկա խորհրդատվություն",
        "btn_individual": "Անհատական խորհրդատվություն — 60 րոպե ({price})",
        "btn_couple": "Զույգերի խորհրդատվություն — 90 րոպե ({price})",
        "ask_timezone": "Նշեք ձեր ժամային գոտին:",
        "ask_time": "Խորհրդատվությունները անցկացվում են Երևանի ժամանակով (GMT+4)։\nԳրանցումը հնարավոր է ուրբաթ և շաբաթ օրերին՝ օրվա առաջին կեսին։\n\nԵթե այս պայմանները ձեզ հարմար են, խնդրում ենք շարունակել —\nմասնագետը կառաջարկի հասանելի ժամերը։",
        "ask_problem": "Եթե ցանկանաք, կարող եք կարճ նկարագրել այն հարցը, որով ցանկանում եք դիմել։",
        "ask_address": "Ինչպե՞ս կարելի է ձեզ դիմել։",
        "ask_comm": "Ո՞ր կապի եղանակն է ձեզ համար նախընտրելի։\n(Telegram, WhatsApp, Viber, Zoom)?",
        "skip": "Բաց թողնել",
        "confirm_sent": "Ձեր հայտը ուղարկված է: Ես կկապնվեմ ձեզ հետ:",
        "waitlist_intro": "Ցավոք, այս պահին ազատ տեղեր չկան: Կարող եք գրանցվել սպասման ցուցակում:",
        "waitlist_contacts": "Թողեք ձեր կոնտակտային տվյալները:",
        "error_generic": "Տեղի է ունեցել սխալ:",
        "negotiation_new": "Նոր առաջարկ թերապևտից:\n\n{msg}",
        "btn_agree": "Համաձայնվել",
        "btn_counter": "Առաջարկել այլ ժամանակ",
        "negotiation_agreed": "Ժամանակը հաստատված է: {time}",
        "negotiation_rejected": "Հայտը մերժված է:",
        "status_confirmed": "Հանդիպումը հաստատված է!",
        "file_not_found": "Տեղեկատվությունը դեռ ավելացված չէ:",
        "menu_home": "🏠 Գլխավոր",
        "welcome_back": "Դուք վերադարձել եք գլխավոր մենյու:",
        "booking_cancelled": "Ամրագրումը չեղարկվեց: Դուք վերադարձել եք գլխավոր մենյու:",
        # v1.0.3: Reminder translations (Armenian)
        "reminder_24h": "🔔 Հիշեցում՝ Ձեր խորհրդատվությունը վաղն է։\n\n📅 Ժամը՝ {time}\n\nՀաջող հանդիպում։",
        "reminder_1h": "🔔 Հիշեցում՝ Ձեր խորհրդատվությունը սկսվում է 1 ժամից։\n\n📅 Ժամը՝ {time}\n\nԽնդրում ենք պատրաստ լինել։",
        'booking_pending_review': (
            "✅ <b>Հայտն ընդունված է:</b>\n\n"
            "📅 Ընտրված ժամանակը: {time}\n"
            "🆔 Համար: {request_id}\n\n"
            "⏳ Սպասեք հաստատմանը հոգեթերապևտից:"
        ),
        'booking_approved': (
            "✅ <b>Գրանցումը հաստատված է:</b>\n\n"
            "📅 {time}\n\n"
            "Ես կապ կհաստատեմ Ձեզ հետ մանրամասները ճշտելու համար:"
        ),
        'booking_rejected': (
            "Ցավոք, ընտրված ժամանակը հասանելի չէ:\n\n"
            "Խնդրում ենք ընտրել այլ ժամանակ կամ կապվել ինձ հետ անմիջապես:"
        ),
        'slot_unavailable': "❌ Ցավոք, այդ ժամանակը արդեն զբաղված է: Խնդրում ենք ընտրել այլ ժամանակ:",
    },
}

# ============================================================================
# CACHE MANAGEMENT
# ============================================================================

async def load_translations_cache():
    """
    Load all translations from database into memory cache.
    Called on application startup. Falls back to TEXTS_DEFAULTS if DB unavailable.
    """
    global _TRANSLATION_CACHE
    
    try:
        from app.db import AsyncSessionLocal
        from app.models import Translation
        from sqlalchemy import select
        
        async with AsyncSessionLocal() as session:
            result = await session.execute(select(Translation))
            translations = result.scalars().all()
            
            # Build cache structure: {lang: {key: value}}
            cache = {}
            for t in translations:
                if t.lang not in cache:
                    cache[t.lang] = {}
                cache[t.lang][t.key] = t.value
            
            _TRANSLATION_CACHE = cache
            logging.info(f"✅ Loaded {len(translations)} translations from database into cache")
            
    except Exception as e:
        logging.error(f"⚠️  Failed to load translations from database: {e}")
        logging.info("   Using fallback hardcoded translations from TEXTS_DEFAULTS")
        # Cache remains empty, get_text() will use TEXTS_DEFAULTS fallback


async def refresh_translations_cache():
    """
    Reload translations from database into cache.
    Call this after web admin updates translations.
    """
    await load_translations_cache()
    logging.info("🔄 Translation cache refreshed from database")


# ============================================================================
# TEXT RETRIEVAL (synchronous for use in handlers)
# ============================================================================

def get_text(lang: str, key: str, **kwargs) -> str:
    """
    Get translated text with three-tier fallback:
    1. Try cache (loaded from DB on startup)
    2. Try hardcoded TEXTS_DEFAULTS dictionary
    3. Return empty string + log warning
    
    Args:
        lang: Language code ('ru', 'am', etc.)
        key: Translation key
        **kwargs: Format parameters for string interpolation
    
    Returns:
        Translated and formatted text
    """
    # Tier 1: Try cache (from DB)
    val = _TRANSLATION_CACHE.get(lang, {}).get(key)
    
    # Tier 2: Fallback to hardcoded TEXTS_DEFAULTS
    if not val:
        val = TEXTS_DEFAULTS.get(lang, {}).get(key)
        
    # Tier 3: Log warning and return empty (silent to user)
    if not val:
        logging.warning(f"Translation missing: {lang}.{key}")
        return ""
        
    # Format if kwargs provided
    if kwargs:
        try:
            return val.format(**kwargs)
        except KeyError as e:
            logging.error(f"Translation format error for {lang}.{key}: {e}")
            return val
            
    return val


def get_cached_languages() -> list:
    """
    Return list of available languages from cache or TEXTS_DEFAULTS.
    Useful for language selection UI.
    """
    if _TRANSLATION_CACHE:
        return list(_TRANSLATION_CACHE.keys())
    return list(TEXTS_DEFAULTS.keys())
