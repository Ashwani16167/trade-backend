import csv
from django.core.management.base import BaseCommand
from trades.models import Stock
from pathlib import Path
from decimal import Decimal, InvalidOperation

class Command(BaseCommand):
    help = 'Import stocks data from CSV into the database'

    def handle(self, *args, **kwargs):
        csv_file_path = Path(__file__).resolve().parent.parent.parent.parent / 'stocks.csv'

        with open(csv_file_path, mode='r') as file:
            reader = csv.DictReader(file)
            for row in reader:
                stock_symbol = row['stock_symbol']
                stock_name = row['stock_name']
                stock_price = row['stock_price']

                # Validate stock_price
                try:
                    stock_price = Decimal(stock_price)
                except (InvalidOperation, ValueError):
                    self.stdout.write(self.style.WARNING(
                        f"Skipping row due to invalid stock_price: {row}"
                    ))
                    continue  # Skip this row and continue with the next

                # Create Stock entry
                Stock.objects.create(
                    stock_code=stock_symbol,
                    stock_name=stock_name,
                    stock_price=stock_price
                )

        self.stdout.write(self.style.SUCCESS("Data imported successfully"))
