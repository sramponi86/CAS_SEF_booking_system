import unittest
import datetime as dt
from rental.company import Company
from rental.exceptions import RentalException
from rental import controller
from contextlib import suppress

class CompanyTests(unittest.TestCase):
  def setUp(self):
    company = Company('Šmertz')
    
    company.cars.add('D12', 'blue')
    company.cars.add('VW Jetta', 'red')
    company.cars.add('Bon Voyage', 'green')
    
    company.customers.add('Random House')
    company.customers.add('Mega Corp')
    
    self.company = company

  def test_all_car_ids_differ(self):
    ids = [car.id for car in self.company.cars.get()]
    duplicates = [id for id in ids if ids.count(id) > 1]
    self.assertEqual(duplicates, [], 'car ids not unique')

  def test_find_car_by_id(self):
    source_car = self.company.cars.get()[0] # Any car would do
    car = self.company.cars.find_by_id(source_car.id)
    self.assertEqual(car.id, source_car.id)
    self.assertEqual(car.model, source_car.model)

  def test_find_car_by_nonexisting_id(self):
    with self.assertRaises(RentalException):
      self.company.cars.find_by_id(-1) # Assumes that all ids are non-negative

  def test_add_rental_by_car_booking(self):
    with suppress(RentalException):
      customer = self.company.customers.get()[0] # Any customer ...
      car = self.company.cars.get()[0] # ... and car would do

      booking = self.company.bookings.add(customer.id, dt.date(2024, 3, 7), dt.date(2024, 3, 14), car.id)
      controller.setToday(dt.date(2024, 3, 7))
      rental = self.company.rentals.add(booking.id)

      self.assertEqual(rental.car, booking.car)
      self.assertEqual(rental.booking, booking)

      booking = self.company.bookings.add(customer.id, dt.date(2024, 3, 5), dt.date(2024, 3, 6), car.id)
      controller.setToday(dt.date(2024, 3, 5))
      rental = self.company.rentals.add(booking.id)

      booking = self.company.bookings.add(customer.id, dt.date(2024, 3, 10), dt.date(2024, 3, 16), car.id)
      controller.setToday(dt.date(2024, 3, 10))
      with self.assertRaises(RentalException):
        self.company.rentals.add(booking.id)    


if __name__ == '__main__':
  unittest.main()
