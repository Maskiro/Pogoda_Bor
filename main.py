import weather

from weather import get_weather, get_temp

weather = get_weather()
temperature, precipitation, current_time = get_temp(weather)

print(f'Погода на {current_time}')
print(f'Температура: {temperature}°C')
print(f'Осадки {precipitation}мм')