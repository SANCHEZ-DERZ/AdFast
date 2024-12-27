from dataclasses import dataclass

@dataclass
class Pages:
    page_category: int
    max_page_category: int
    page_result: int
    max_page_result: int
    page_socnet: int
    max_page_socnet: int
    page_count: int
    max_page_count: int

# Создаем экземпляр Pages
pages_instance = Pages(
    page_category=1,
    max_page_category=2,
    page_result=1,
    max_page_result=0,
    max_page_count=2,
    max_page_socnet=2,
    page_count=1,
    page_socnet=1
)

@dataclass
class Button:
    text: str
    callback_data: str

@dataclass
class Lists:
    category: list
    socnet: list
    count: list
    result: list

# Создаем экземпляр Lists с предопределенными значениями
lst = Lists(
    category=["Fashion", "IT", "Travel", "Business", "Beauty"],
    count=['10.000-', '10.000-50.000', '50.000-100.000', '100.000-500.000', '500.000-1.000.000', '1.000.000+'],
    socnet=['Instagram', 'Telegram', 'TikTok', 'VK', 'YouTube', 'Yandex Dzen'],
    result=[]
)
