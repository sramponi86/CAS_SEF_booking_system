from patterns.observer import Observer
from rental.bookings import Bookings
from rental.cars import Cars
from rental.customers import Customers
from rental.rentals import Rentals
from rental.company import Company

class BookingStats(Observer):
  def update(self, b: Bookings) -> None:
    print(f'*** STATISTICS ***: Number of Bookings: {len(b.bookings)}')

class CarStats(Observer):
  def update(self, c: Cars) -> None:
    print(f'*** STATISTICS ***: Number of Cars: {len(c.cars)}')

class CustomerStats(Observer):
  def update(self, k: Customers) -> None:
    print(f'*** STATISTICS ***: Number of Customers: {len(k.customers)}')

class RentalStats(Observer):
  def update(self, r: Rentals) -> None:
    print(f'*** STATISTICS ***: Number of Rentals: {len(r.rentals)}')

def attachTo(company: Company):
  company.bookings.attach(BookingStats())
  company.cars.attach(CarStats())
  company.customers.attach(CustomerStats())
  company.rentals.attach(RentalStats())
  # TODO Register more observer classes here ...