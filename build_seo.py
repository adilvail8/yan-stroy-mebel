# -*- coding: utf-8 -*-
"""SEO-сборка сайта YanStroyMebel. Запуск: python build_seo.py
Генерирует страницы услуг, JSON-LD на главной, sitemap.xml и robots.txt."""
import io, json, os, re, datetime, urllib.parse

ROOT = os.path.dirname(os.path.abspath(__file__))
BASE = "https://yan-stroy-mebel.kz/"
WA = "77089249883"
PHONE = "+7 708 924 98 83"
TODAY = datetime.date.today().isoformat()


def wa(text):
    return "https://wa.me/%s?text=%s" % (WA, urllib.parse.quote(text))


BIZ = {
    "@type": ["LocalBusiness", "FurnitureStore"],
    "@id": BASE + "#business",
    "name": "YanStroyMebel",
    "description": "Производство корпусной мебели на заказ в Алматы: кухни, шкафы-купе, гардеробные, мебель для ванной и офиса. Материалы и работу цеха финансирует компания, первый платёж после осмотра готовой мебели.",
    "url": BASE,
    "telephone": "+77089249883",
    "image": BASE + "assets/og.jpg",
    "logo": BASE + "assets/logo.png",
    "priceRange": "$$",
    "currenciesAccepted": "KZT",
    "areaServed": {"@type": "City", "name": "Алматы"},
    "address": {"@type": "PostalAddress", "streetAddress": "улица Жарокова, 128",
                "addressLocality": "Алматы", "addressRegion": "Алматы", "addressCountry": "KZ"},
    "geo": {"@type": "GeoCoordinates", "latitude": 43.236824, "longitude": 76.900146},
    "openingHoursSpecification": [{
        "@type": "OpeningHoursSpecification",
        "dayOfWeek": ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday"],
        "opens": "09:00", "closes": "18:00"}],
    "sameAs": ["https://www.instagram.com/yan.stroy.mebel/"],
    "department": [{
        "@type": "LocalBusiness", "name": "YanStroyMebel, цех",
        "address": {"@type": "PostalAddress", "streetAddress": "улица Бокейханова, 37/1",
                    "addressLocality": "Алматы", "addressCountry": "KZ"},
        "telephone": "+77089249883"}],
}

STEPS = [
    ("01", "Замер и проект", "Замерщик приезжает по Алматы бесплатно. Рисуем чертёж, подбираем материалы, считаем в трёх комплектациях.", "0 ₸"),
    ("02", "Договор и производство", "Подписываем договор ТОО и спецификацию, где прописаны материал, цвет, фурнитура и схема. Материалы закупаем за свой счёт.", "0 ₸"),
    ("03", "Осмотр в цеху и монтаж", "Вы осматриваете готовый заказ до установки и вносите 50%. Вторая половина после монтажа и подписания акта.", "50 / 50"),
]

COMMON_FAQ = [
    ("Правда без предоплаты?", "Вперёд вы не платите ничего. Материалы, фурнитуру и работу цеха финансируем мы. Первый платёж 50% вносится после того, как вы осмотрели готовый заказ в цеху перед установкой, вторые 50% после монтажа и подписания акта выполненных работ."),
    ("Сколько стоит замер?", "По Алматы бесплатно и ни к чему не обязывает. После замера вы получаете чертёж и смету, дальше решаете сами."),
    ("Что фиксируется в договоре?", "Договор ТОО и приложение к нему, спецификация: материал, цвет, фурнитура, схема и размеры каждого модуля. Сдаём заказ строго по спецификации."),
]

PAGES = [
    dict(slug="kuhni-na-zakaz", name="Кухни на заказ",
         h1="Кухни на заказ в Алматы",
         title="Кухни на заказ в Алматы без предоплаты | YanStroyMebel",
         desc="Кухни на заказ в Алматы по индивидуальному проекту: прямые, угловые, П-образные и с островом. Оплата после осмотра готовой кухни в цеху. Фурнитура Blum, Hafele, бесплатный замер.",
         lead="Проектируем кухню под вашу планировку, технику и привычки. Считаем в трёх комплектациях, показываем чертёж до договора, а платить вы начинаете, когда кухня уже готова и вы осмотрели её в цеху.",
         hero=("assets/work/p01-kitchen-island.webp", "Кухня с островом на заказ в Алматы, шалфейные фасады и кварцевый остров"),
         gallery=[("assets/work/p06-oak-kitchen.webp", "Кухня в светлом дубе без ручек со столешницей терраццо"),
                  ("assets/work/drawing-kitchen.webp", "Рабочий чертёж кухни с размерами каждого модуля")],
         feats=[("Проект под технику", "Закладываем размеры под вашу духовку, посудомойку, варочную панель и вытяжку. Если техника ещё не куплена, подскажем габариты."),
                ("Любая конфигурация", "Прямая, угловая, П-образная, с островом или барной стойкой. Форму подбираем по планировке, а не по каталогу."),
                ("Влагостойкий корпус", "В зоне мойки ставим влагостойкую плиту, торцы закрываем кромкой ПВХ."),
                ("Столешницы", "Постформинг, акриловый камень или кварцевый агломерат, в зависимости от комплектации."),
                ("Фурнитура", "Blum, Hafele, Boyard: доводчики, полное выдвижение, подъёмные механизмы."),
                ("Подрезка на месте", "Столешницу подрезаем под мойку и варочную при монтаже, стыки подгоняем по факту.")],
         faq=[("Сколько делается кухня?", "Срок зависит от фасадов: плёночный МДФ и ЛДСП быстрее, эмаль и шпон дольше из-за покраски и сушки. Точный срок ставим в договор после утверждения проекта."),
              ("Можно ли заказать кухню, если ремонт ещё не закончен?", "Да. На черновой отделке делаем предварительный замер и проект, контрольный замер снимаем, когда стены и выводы готовы.")],
         wa="Здравствуйте! Хочу рассчитать кухню на заказ"),
    dict(slug="shkafy-kupe", name="Шкафы-купе",
         h1="Шкафы-купе на заказ в Алматы",
         title="Шкафы-купе на заказ в Алматы по размерам | YanStroyMebel",
         desc="Шкафы-купе на заказ в Алматы: до потолка, встроенные в нишу, с зеркалом и подсветкой. Изготовление в своём цехе, оплата после осмотра готового шкафа. Бесплатный замер.",
         lead="Делаем шкафы-купе под точные размеры стены или ниши: без зазора у потолка, с наполнением под ваши вещи. Внутреннюю схему согласуем на замере и фиксируем в спецификации к договору.",
         hero=("assets/work/p03-sliding-wardrobe.webp", "Шкаф-купе на заказ в прихожую, эмаль и бронзовое зеркало"),
         gallery=[("assets/work/p02-walk-in.webp", "Система хранения с полками, штангами и подсветкой"),
                  ("assets/work/p07-tv-wall.webp", "Шкаф и ТВ-зона в одной стене, реечные панели из ореха")],
         feats=[("До потолка", "Без антресольного зазора: сверху не собирается пыль, места для хранения больше."),
                ("Под нишу любой формы", "Работаем со скошенными стенами, откосами и перепадами потолка."),
                ("Наполнение под вещи", "Штанги, полки, ящики, обувные секции и антресоли по вашему списку."),
                ("Двери", "Зеркало, стекло в алюминиевой рамке, комбинированные полотна."),
                ("Подсветка", "Встроенный свет внутри шкафа и по контуру."),
                ("Фурнитура", "Направляющие с доводчиком, двери едут мягко и не хлопают.")],
         faq=[("Чем шкаф-купе отличается от распашного?", "Купе не требует места для открывания дверей, поэтому подходит для узких прихожих и спален. В распашном удобнее видеть всё содержимое сразу, выбираем по планировке."),
              ("Можно ли встроить шкаф в нишу с кривыми стенами?", "Да. Мебель делается по факту замера, неровности закрываем доборными планками.")],
         wa="Здравствуйте! Хочу рассчитать шкаф-купе"),
    dict(slug="garderobnye", name="Гардеробные",
         h1="Гардеробные комнаты на заказ в Алматы",
         title="Гардеробные на заказ в Алматы: проект и изготовление | YanStroyMebel",
         desc="Гардеробные комнаты и системы хранения на заказ в Алматы. Проект под ваш гардероб, подсветка полок, фурнитура Blum и Hafele. Первый платёж после осмотра готовой гардеробной.",
         lead="Гардеробная собирает вещи в одном месте и разгружает остальную квартиру. Считаем длину штанг и количество полок по вашему гардеробу, а не по типовой схеме.",
         hero=("assets/work/p02-walk-in.webp", "Гардеробная на заказ, копчёный дуб, стекло и подсветка полок"),
         gallery=[("assets/work/p03-sliding-wardrobe.webp", "Шкаф с зеркальными дверями в прихожей"),
                  ("assets/work/p10-kids.webp", "Система хранения и рабочее место вдоль окна")],
         feats=[("Проект под гардероб", "Считаем, сколько нужно длинного и короткого хранения, ящиков и полок под обувь."),
                ("Подсветка", "Свет внутри секций и по контуру, датчики на открывание по желанию."),
                ("Стекло и витрины", "Секции со стеклом для сумок и аксессуаров."),
                ("Ящики с доводчиком", "С органайзерами под бельё и мелочи."),
                ("Антресоли", "Под чемоданы и сезонные вещи, с удобной высотой полок."),
                ("Открытая или закрытая", "Отдельная комната без дверей или ниша с фасадами.")],
         faq=[("Сколько места нужно под гардеробную?", "Рабочая гардеробная получается даже из ниши шириной от полутора метров. Конкретный вариант подбираем на замере по вашей планировке."),
              ("Делаете ли гардеробную вместе со шкафом в спальне?", "Да, можем закрыть всю квартиру одним договором и одной спецификацией.")],
         wa="Здравствуйте! Хочу рассчитать гардеробную"),
    dict(slug="gostinye-tv-zony", name="Гостиные и ТВ-зоны",
         h1="Мебель для гостиной и ТВ-зоны на заказ в Алматы",
         title="Гостиные и ТВ-зоны на заказ в Алматы | YanStroyMebel",
         desc="Мебель для гостиной на заказ в Алматы: ТВ-зоны, стеллажи, реечные панели, закрытое и открытое хранение. Оплата после осмотра готовой мебели в цеху. Бесплатный замер.",
         lead="Собираем стену гостиной целиком: ТВ-зона, закрытое хранение, открытые полки и декоративные панели в одном проекте, без сборной мебели из разных коллекций.",
         hero=("assets/work/p07-tv-wall.webp", "Гостиная и ТВ-зона на заказ, реечные панели из ореха"),
         gallery=[("assets/work/p05-study.webp", "Стеллаж и рабочая зона в тонированном ясене"),
                  ("assets/work/p06-oak-kitchen.webp", "Кухня-гостиная в светлом дубе")],
         feats=[("ТВ-зона", "Ниша под диагональ вашего телевизора, кабели спрятаны в каналы."),
                ("Реечные панели", "Шпон или крашеный МДФ, задают ритм стене."),
                ("Открытые полки", "Под книги и декор, с подсветкой по желанию."),
                ("Закрытое хранение", "Фасады с Tip-On без ручек, чтобы стена читалась цельной."),
                ("Подсветка", "Контурная подсветка ниши и полок."),
                ("Единый проект", "Гостиная, кухня и прихожая в одном материале и цвете.")],
         faq=[("Можно ли спрятать провода от техники?", "Да, закладываем кабель-каналы и вентиляционные отверстия на этапе чертежа, до производства."),
              ("Делаете ли мебель под уже купленный телевизор?", "Да, нишу проектируем под конкретную модель и высоту посадки.")],
         wa="Здравствуйте! Хочу рассчитать мебель для гостиной"),
    dict(slug="detskaya-mebel", name="Детская мебель",
         h1="Детская мебель на заказ в Алматы",
         title="Детская мебель на заказ в Алматы: шкаф, стол, стеллажи | YanStroyMebel",
         desc="Мебель для детской на заказ в Алматы: шкаф до потолка, стол у окна, стеллажи и хранение. Безопасная фурнитура с доводчиками, оплата после осмотра готовой мебели.",
         lead="В детской нужно уместить сон, учёбу, игры и хранение в одной комнате. Проектируем мебель так, чтобы она подошла ребёнку и сейчас, и через несколько лет.",
         hero=("assets/work/p10-kids.webp", "Детская на заказ, шкаф и рабочий стол вдоль окна"),
         gallery=[("assets/work/p05-study.webp", "Стеллаж и стол в тонированном ясене"),
                  ("assets/work/p03-sliding-wardrobe.webp", "Шкаф с зеркальной дверью")],
         feats=[("Стол у окна", "Рабочая поверхность во всю стену, ящики под тетради и канцелярию."),
                ("Шкаф до потолка", "Одежда, игрушки и сезонные вещи в одном месте."),
                ("Стеллажи", "Открытые полки под книги и то, что ребёнок хочет держать на виду."),
                ("Доводчики", "Двери и ящики закрываются мягко, без прищемленных пальцев."),
                ("Материалы", "ЛДСП с кромкой ПВХ по всем торцам, без открытых срезов."),
                ("На вырост", "Переставляемые полки и стол с запасом по высоте.")],
         faq=[("Делаете ли комнату для двоих детей?", "Да: два рабочих места, раздельное хранение и спальные места в одном проекте."),
              ("Насколько безопасны материалы?", "Используем ЛДСП с кромкой по всем торцам и фурнитуру с доводчиками. Состав плиты и все комплектующие указываем в спецификации к договору.")],
         wa="Здравствуйте! Хочу рассчитать мебель в детскую"),
    dict(slug="mebel-dlya-vannoy", name="Мебель для ванной",
         h1="Мебель для ванной на заказ в Алматы",
         title="Мебель для ванной на заказ в Алматы: тумбы и пеналы | YanStroyMebel",
         desc="Влагостойкая мебель для ванной на заказ в Алматы: тумбы под раковину, пеналы, зеркальные шкафы. Влагостойкая плита, кромка по всем торцам, оплата после осмотра.",
         lead="В санузле мебель работает в постоянной влажности, поэтому ставим влагостойкую плиту и закрываем кромкой все торцы. Тумбу проектируем под вашу раковину и разводку.",
         hero=("assets/work/p04-vanity.webp", "Тумба под раковину на заказ, рифлёный орех и травертин"),
         gallery=[("assets/work/p03-sliding-wardrobe.webp", "Пенал с зеркальным фасадом"),
                  ("assets/work/p01-kitchen-island.webp", "Столешница из камня, тот же подход к влажным зонам")],
         feats=[("Влагостойкая плита", "В зоне мойки и в санузле используем влагостойкий корпус."),
                ("Под вашу раковину", "Вырез и подрезку делаем по факту, с учётом сифона и разводки."),
                ("Кромка по всем торцам", "Открытых срезов, которые разбухают от воды, не остаётся."),
                ("Пеналы и зеркала", "Дополнительное хранение и зеркальные шкафы с подсветкой."),
                ("Столешница", "Акриловый камень или кварцевый агломерат под раковину."),
                ("Фурнитура", "Направляющие и петли с доводчиком, стойкие к влаге.")],
         faq=[("Подходит ли обычная мебель в ванную?", "Нет. Обычная плита без влагостойкой пропитки и открытые торцы разбухают за пару лет. Поэтому в санузле ставим влагостойкий корпус и закрываем все торцы кромкой."),
              ("Можно ли сделать тумбу под накладную раковину?", "Да, проектируем и под накладную, и под встраиваемую, и под подвесную.")],
         wa="Здравствуйте! Хочу рассчитать мебель для ванной"),
    dict(slug="ofisnaya-mebel", name="Офисная мебель",
         h1="Офисная мебель и кабинеты на заказ в Алматы",
         title="Офисная мебель на заказ в Алматы: столы, стеллажи, кабинеты | YanStroyMebel",
         desc="Офисная мебель на заказ в Алматы: рабочие столы, стеллажи, шкафы для документов, домашние кабинеты. Договор ТОО, оплата после осмотра и монтажа.",
         lead="Оборудуем кабинет дома и рабочие места в офисе: столы под количество сотрудников, закрытое хранение документов, стеллажи и ресепшен в одном материале.",
         hero=("assets/work/p05-study.webp", "Кабинет и стеллаж на заказ, тонированный ясень"),
         gallery=[("assets/work/p07-tv-wall.webp", "Стеновые панели и встроенное хранение"),
                  ("assets/work/p10-kids.webp", "Рабочее место вдоль окна")],
         feats=[("Рабочие места", "Столы под нужное число сотрудников, с выводами под технику."),
                ("Хранение документов", "Закрытые шкафы и картотеки, запираемые секции по запросу."),
                ("Стеллажи", "Открытые конструкции под архив, образцы или библиотеку."),
                ("Домашний кабинет", "Стол, полки и шкаф в одном материале с остальной квартирой."),
                ("Договор ТОО", "Полный пакет документов для юридических лиц."),
                ("Сроки", "Фиксируем в договоре, о ходе производства присылаем фото.")],
         faq=[("Работаете с юридическими лицами?", "Да, мы ТОО. Заключаем договор, выставляем счёт и закрываем сделку актом выполненных работ."),
              ("Можно ли оборудовать офис поэтапно?", "Да, разбиваем проект на очереди и ставим сроки по каждой в договоре.")],
         wa="Здравствуйте! Хочу рассчитать офисную мебель"),
]

HEAD = """<!DOCTYPE html>
<html lang="ru">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{title}</title>
<meta name="description" content="{desc}">
<link rel="canonical" href="{url}">
<meta name="robots" content="index,follow,max-image-preview:large">
<meta name="geo.region" content="KZ-ALA">
<meta name="geo.placename" content="Алматы">
<meta property="og:site_name" content="YanStroyMebel">
<meta property="og:locale" content="ru_RU">
<meta property="og:type" content="article">
<meta property="og:url" content="{url}">
<meta property="og:title" content="{title}">
<meta property="og:description" content="{desc}">
<meta property="og:image" content="{base}assets/og.jpg">
<meta name="twitter:card" content="summary_large_image">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Golos+Text:wght@400;500;600;700;800&family=Manrope:wght@200;300;400;500&display=swap" rel="stylesheet">
<link rel="icon" href="/assets/logo-mark.png">
<link rel="stylesheet" href="/styles.css?v=11">
<link rel="stylesheet" href="/pages.css?v=1">
</head>
<body>
"""


def esc(t):
    return t.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;").replace('"', "&quot;")


def build_page(pg, others):
    url = BASE + pg["slug"] + "/"
    out = [HEAD.format(title=esc(pg["title"]), desc=esc(pg["desc"]), url=url, base=BASE)]
    a = out.append
    a('<header class="pg-hdr"><div class="wrap pg-hdr__in">')
    a('<a class="pg-hdr__mark" href="%s" aria-label="YanStroyMebel, на главную"><img src="%sassets/logo-mark.png" alt="YanStroyMebel" width="449" height="250"></a>' % ("/", "/"))
    a('<div class="pg-hdr__act"><a class="btn btn--sm" href="%s" target="_blank" rel="noopener">WhatsApp</a>'
      '<a class="btn btn--sm btn--ghost" href="%s">На главную</a></div>' % (wa(pg["wa"]), "/"))
    a('</div></header>')
    a('<main>')
    a('<nav class="crumbs wrap" aria-label="Хлебные крошки"><a href="/">Главная</a><span>/</span>%s</nav>' % esc(pg["name"]))

    a('<section class="pg-hero"><div class="wrap">')
    a('<p class="eyebrow eyebrow--brass">%s</p>' % esc(pg["name"]))
    a('<h1>%s</h1>' % esc(pg["h1"]))
    a('<p class="pg-hero__lead">%s</p>' % esc(pg["lead"]))
    a('<div class="pg-hero__cta"><a class="btn btn--wa btn--lg" href="%s" target="_blank" rel="noopener">Рассчитать в WhatsApp</a>'
      '<a class="btn btn--ghost btn--lg" href="/#quiz">Пройти расчёт на сайте</a></div>' % wa(pg["wa"]))
    src, alt = pg["hero"]
    a('<figure class="pg-hero__img"><img src="%s%s" alt="%s" width="2560" height="1280" fetchpriority="high" decoding="async"></figure>' % ("/", src, esc(alt)))
    a('</div></section>')

    a('<section class="pg-sec"><div class="wrap">')
    a('<div class="sec-head"><p class="eyebrow eyebrow--brass">Что входит</p><h2 class="h2">Из чего складывается проект</h2></div>')
    a('<div class="pg-feats">')
    for h, p in pg["feats"]:
        a('<article><h3>%s</h3><p>%s</p></article>' % (esc(h), esc(p)))
    a('</div></div></section>')

    a('<section class="pg-sec pg-sec--dark"><div class="wrap">')
    a('<div class="sec-head"><p class="eyebrow eyebrow--light">Оплата</p><h2 class="h2 h2--light">Вы платите, когда мебель уже готова</h2>'
      '<p class="lead" style="color:rgba(246,243,236,.72)">Материалы, фурнитуру и работу цеха финансируем мы. Первый платёж наступает после того, как вы осмотрели заказ в цеху.</p></div>')
    a('<div class="pg-steps">')
    for num, h, p, sum_ in STEPS:
        a('<article><i>%s</i><h3>%s</h3><p>%s</p><b>%s</b></article>' % (num, esc(h), esc(p), esc(sum_)))
    a('</div></div></section>')

    a('<section class="pg-sec"><div class="wrap">')
    a('<div class="sec-head"><p class="eyebrow eyebrow--brass">Работы</p><h2 class="h2">Как это выглядит</h2></div>')
    a('<div class="pg-gal">')
    for src, alt in pg["gallery"]:
        a('<figure><img src="%s%s" alt="%s" width="1400" height="1050" loading="lazy" decoding="async"></figure>' % ("/", src, esc(alt)))
    a('</div>')
    a('<div class="pg-links">')
    for o in others:
        a('<a href="/%s/">%s</a>' % (o["slug"], esc(o["name"])))
    a('</div></div></section>')

    faq = pg["faq"] + COMMON_FAQ
    a('<section class="pg-sec"><div class="wrap">')
    a('<div class="sec-head"><p class="eyebrow eyebrow--brass">Вопросы</p><h2 class="h2">Отвечаем прямо</h2></div>')
    a('<div class="acc">')
    for q, ans in faq:
        a('<details><summary>%s</summary><div><p>%s</p></div></details>' % (esc(q), esc(ans)))
    a('</div></div></section>')

    a('<section class="pg-cta"><div class="wrap">')
    a('<h2 class="h2">Рассчитаем ваш проект за один день</h2>')
    a('<p>Пришлите размеры, фото помещения или дизайн-проект. Ответим сметой в трёх комплектациях и сроком производства.</p>')
    a('<div class="pg-cta__row"><a class="btn btn--wa btn--lg" href="%s" target="_blank" rel="noopener">Написать в WhatsApp</a>'
      '<a class="plain" href="tel:+%s">%s</a></div>' % (wa(pg["wa"]), WA, PHONE))
    a('<p style="margin-top:26px;font-size:14px">Пн – Пт, 9:00 – 18:00. Офис: Алматы, Жарокова 128. Цех: Бокейханова 37/1.</p>')
    a('</div></section>')
    a('</main>')
    a('<footer class="ftr"><div class="wrap ftr__in"><p>YanStroyMebel, Алматы. Мебель на заказ без предоплаты.</p>'
      '<nav><a href="/">Главная</a><a href="/#pay">Оплата</a><a href="/#faq">Вопросы</a></nav></div></footer>')

    ld = {"@context": "https://schema.org", "@graph": [
        BIZ,
        {"@type": "Service", "name": pg["name"], "serviceType": pg["h1"],
         "description": pg["desc"], "url": url,
         "provider": {"@id": BASE + "#business"},
         "areaServed": {"@type": "City", "name": "Алматы"}},
        {"@type": "BreadcrumbList", "itemListElement": [
            {"@type": "ListItem", "position": 1, "name": "Главная", "item": BASE},
            {"@type": "ListItem", "position": 2, "name": pg["name"], "item": url}]},
        {"@type": "FAQPage", "mainEntity": [
            {"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": ans}} for q, ans in faq]},
    ]}
    a('<script type="application/ld+json">%s</script>' % json.dumps(ld, ensure_ascii=False))
    a('<a class="fab" href="%s" target="_blank" rel="noopener" aria-label="Написать в WhatsApp">'
      '<svg viewBox="0 0 24 24" width="22" height="22" fill="currentColor" aria-hidden="true"><path d="M12.04 2C6.58 2 2.13 6.45 2.13 11.91c0 1.75.46 3.45 1.32 4.95L2 22l5.25-1.38a9.9 9.9 0 0 0 4.79 1.22h.01c5.46 0 9.91-4.45 9.91-9.91 0-2.65-1.03-5.14-2.9-7.01A9.86 9.86 0 0 0 12.04 2Z"/></svg></a>' % wa(pg["wa"]))
    a('</body>\n</html>')
    return "\n".join(out)


def faq_from_index():
    s = io.open(os.path.join(ROOT, "index.html"), encoding="utf-8").read()
    pairs = re.findall(r"<summary>(.*?)</summary><div><p>(.*?)</p>", s, re.S)
    return [(re.sub("<[^>]+>", "", q).strip(), re.sub("<[^>]+>", "", a).strip()) for q, a in pairs]


def inject_home_ld():
    path = os.path.join(ROOT, "index.html")
    s = io.open(path, encoding="utf-8").read()
    faq = faq_from_index()
    ld = {"@context": "https://schema.org", "@graph": [
        BIZ,
        {"@type": "WebSite", "@id": BASE + "#website", "url": BASE, "name": "YanStroyMebel",
         "inLanguage": "ru-RU", "publisher": {"@id": BASE + "#business"}},
        {"@type": "FAQPage", "mainEntity": [
            {"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": a}} for q, a in faq]},
        {"@type": "ItemList", "name": "Услуги", "itemListElement": [
            {"@type": "ListItem", "position": i + 1, "name": p["name"], "url": BASE + p["slug"] + "/"}
            for i, p in enumerate(PAGES)]},
    ]}
    block = '<script type="application/ld+json">%s</script>' % json.dumps(ld, ensure_ascii=False)
    s = re.sub(r'<script type="application/ld\+json">.*?</script>\s*', "", s, flags=re.S)
    s = s.replace("</body>", block + "\n</body>")
    io.open(path, "w", encoding="utf-8").write(s)


def write_sitemap():
    urls = [(BASE, "1.0")] + [(BASE + p["slug"] + "/", "0.8") for p in PAGES]
    x = ['<?xml version="1.0" encoding="UTF-8"?>',
         '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">']
    for u, pr in urls:
        x.append("  <url><loc>%s</loc><lastmod>%s</lastmod><priority>%s</priority></url>" % (u, TODAY, pr))
    x.append("</urlset>")
    io.open(os.path.join(ROOT, "sitemap.xml"), "w", encoding="utf-8").write("\n".join(x) + "\n")


def write_robots():
    io.open(os.path.join(ROOT, "robots.txt"), "w", encoding="utf-8").write(
        "User-agent: *\nAllow: /\n\nSitemap: %ssitemap.xml\n" % BASE)


if __name__ == "__main__":
    for pg in PAGES:
        others = [o for o in PAGES if o["slug"] != pg["slug"]]
        d = os.path.join(ROOT, pg["slug"])
        os.makedirs(d, exist_ok=True)
        io.open(os.path.join(d, "index.html"), "w", encoding="utf-8").write(build_page(pg, others))
        print("ok", pg["slug"])
    inject_home_ld()
    write_sitemap()
    write_robots()
    print("home JSON-LD, sitemap.xml, robots.txt")
