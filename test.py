import pygame
import requests
import sys

# --- Настройки ---
API_KEY = "09e1f985fe26bffa28db07db58eaa04d"  # Вставь сюда свой ключ OpenWeatherMap
WIDTH, HEIGHT = 480, 640
CITY = "Nukus"  # Город по умолчанию

# --- Инициализация Pygame ---
pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Weather App")
font = pygame.font.SysFont("Arial", 30)
clock = pygame.time.Clock()


def get_weather(city):
    url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={API_KEY}&units=metric"
    try:
        response = requests.get(url)
        data = response.json()
        if data["cod"] != 200:
            return f"Ошибка: {data['message']}"
        temp = data["main"]["temp"]
        desc = data["weather"][0]["description"]
        return f"{city}\n{temp}°C\n{desc.capitalize()}"
    except Exception as e:
        return f"Ошибка: {e}"


def draw_text(text, x, y):
    lines = text.split("\n")
    for i, line in enumerate(lines):
        rendered = font.render(line, True, (255, 255, 255))
        screen.blit(rendered, (x, y + i * 40))


city_input = ""
weather_info = get_weather(CITY)

# --- Главный цикл ---
running = True
while running:
    screen.fill((0, 100, 200))  # Цвет фона

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RETURN:
                weather_info = get_weather(city_input if city_input else CITY)
                city_input = ""
            elif event.key == pygame.K_BACKSPACE:
                city_input = city_input[:-1]
            else:
                city_input += event.unicode

    # Отрисовка текста
    draw_text(weather_info, 50, 100)
    draw_text("Введите город: " + city_input, 50, 400)

    pygame.display.flip()
    clock.tick(30)

pygame.quit()
sys.exit()