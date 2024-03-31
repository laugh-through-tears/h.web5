import aiohttp
import asyncio
from datetime import datetime, timedelta

class CurrencyConverter:
    async def fetch_exchange_rate(self, date):
        async with aiohttp.ClientSession() as session:
            async with session.get(f'https://api.privatbank.ua/p24api/exchange_rates?json&date={date}') as response:
                return await response.json()

    async def fetch_rates_for_last_n_days(self, n):
        today = datetime.today()
        rates = []
        for i in range(n):
            date = (today - timedelta(days=i)).strftime('%d.%m.%Y')
            data = await self.fetch_exchange_rate(date)
            rates.append({date: data})
        return rates

    async def get_currency_rates(self, n_days):
        rates = await self.fetch_rates_for_last_n_days(n_days)

        formatted_rates = []
        for rate_data in rates:
            date, data = rate_data.popitem()
            currencies = data['exchangeRate']
            usd_rate = next((currency for currency in currencies if currency['currency'] == 'USD'), None)
            eur_rate = next((currency for currency in currencies if currency['currency'] == 'EUR'), None)

            if usd_rate and eur_rate:
                formatted_rate = {
                    date: {
                        'USD': {
                            'sale': usd_rate['saleRateNB'],
                            'purchase': usd_rate['purchaseRateNB']
                        },
                        'EUR': {
                            'sale': eur_rate['saleRateNB'],
                            'purchase': eur_rate['purchaseRateNB']
                        }
                    }
                }
                formatted_rates.append(formatted_rate)

        return formatted_rates

async def main():

    try:
        import sys
        n_days = int(sys.argv[1]) if len(sys.argv) > 1 else 10
        if n_days > 10:
            print("Error: Cannot fetch rates for more than the last 10 days")
            return
    except ValueError:
        print("Error: Invalid input")
        return

    converter = CurrencyConverter()
    currency_rates = await converter.get_currency_rates(n_days)
    print(currency_rates)

if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())


