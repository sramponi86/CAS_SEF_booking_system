from patterns.observer import Observer
from rental.bookings import Bookings
from rental.company import Company

class BookingStats(Observer):
  def update(self, b: Bookings) -> None:
    print(f'*** STATISTICS ***: Number of Bookings: {len(b.bookings)}')

# TODO Add more observer classes here ...

def attachTo(company: Company):
  company.bookings.attach(BookingStats())
  # TODO Register more observer classes here ...