import datetime
import asyncio
import aiohttp
import json

API_URL = "https://api.privatbank.ua/p24api/pubinfo?json&exchange&coursid=5"


async def get_rates(days):
    """
    Отримати курси валют за останні `days` днів.

    Args:
        days: Кількість днів (не більше 10).

    Returns:
        Список курсів валют.
    """
    if days > 10:
        raise ValueError("Кількість днів не може бути більше 10")

    today = str(datetime.date.today())
    start_date = str(datetime.date.today() - datetime.timedelta(days=days))

    params = {"date": f"{start_date}-{today}"}

    async with aiohttp.ClientSession() as session:
        async with session.get(API_URL, params=params) as response:
            response_data = await response.json()

    return response_data


async def main():

    days = int(input("Введіть кількість днів (не більше 10): "))

    try:
        rates = await get_rates(days)
    except ValueError as e:
        print(e)
    except Exception as e:
        print(f"Помилка при отриманні даних: {e}")
    else:
        print(json.dumps(rates, indent=2))


if __name__ == "__main__":
    asyncio.run(main())

