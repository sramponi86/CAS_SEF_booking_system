import unittest
import datetime as dt
from rental.rentals import Rental, Rentals
from rental.exceptions import RentalException
from rental.company import Company
from rental import controller

class RentalTests(unittest.TestCase):
  def setUp(self):
    company = Company('Šmertz')
    car = company.cars.add('D12')
    customer = company.customers.add('Random House')
    self.booking = company.bookings.add(customer.id, dt.date(2024, 3, 7), dt.date(2024, 3, 14), car.id)

  def test_constructor(self):
    rental = Rental(1, self.booking, self.booking.car)
    self.assertEqual(rental.id, 1, "incorrect id after construction")
    self.assertEqual(rental.booking, self.booking, "incorrect booking after construction")
    self.assertEqual(rental.car, self.booking.car, "incorrect car after construction")
  
class RentalsTests(unittest.TestCase):
  def setUp(self):
    company = Company('Šmertz')
    self.rentals = company.rentals
    self.company = company

  def fill_rentals(self):
    cust1 = self.company.customers.add('Random House')
    cust2 = self.company.customers.add('Mega Corp')
    car1 = self.company.cars.add('D12')
    car2 = self.company.cars.add('VW Jetta')
    booking1 = self.company.bookings.add(cust1.id, controller.today, controller.today + dt.timedelta(days=10), car1.id)
    booking2 = self.company.bookings.add(cust2.id, controller.today, controller.today + dt.timedelta(days=10), car2.id)
    rental1 = self.rentals.add(booking1.id)
    rental2 = self.rentals.add(booking2.id)
    return rental1, rental2

  def test_add(self):
    customer = self.company.customers.add('Random House')
    car = self.company.cars.add('D12')
    booking = self.company.bookings.add(customer.id, controller.today, controller.today + dt.timedelta(days=10), car.id)
    rental = self.rentals.add(booking.id)
    self.assertCountEqual([rental], self.rentals.rentals, "rental not added")

  def test_add_exception_start_date(self):
    # Raise RentalException if the start date of the booking does not concide with today's date.
    customer = self.company.customers.add('Monty Python')
    car = self.company.cars.add('D12')
    not_today_booking = self.company.bookings.add(customer.id, dt.date(2021, 3, 7), dt.date(2024, 3, 14), car.id)
    with self.assertRaises(RentalException):
      self.rentals.add(not_today_booking.id)

  def test_add_exception_already_rented(self):
    # Raise RentalException if a booking is for a specific car and that car is already rented.
    customer1 = self.company.customers.add('Random House')
    customer2 = self.company.customers.add('Mega Corp')
    car = self.company.cars.add('VW Jetta')
    booking1 = self.company.bookings.add(customer1.id, controller.today, controller.today + dt.timedelta(days=10), car.id)
    booking2 = self.company.bookings.add(customer2.id, controller.today, controller.today + dt.timedelta(days=10), car.id)
    self.rentals.add(booking1.id)
    with self.assertRaises(RentalException):
      self.rentals.add(booking2.id)

  def test_get_empty(self):
    self.assertEqual(self.rentals.get(), [], "rentals not retrieved")

  def test_get_not_empty(self):
    rental1, rental2 = self.fill_rentals()
    self.assertCountEqual(self.rentals.get(), [rental1, rental2], "rentals not retrieved")               

  def test_delete(self):
    rental1, rental2 = self.fill_rentals()
    self.rentals.delete(rental1.id)
    self.assertNotIn(rental1, self.rentals.rentals, "rental not deleted")

  def test_find_by_id(self):
    rental1, rental2 = self.fill_rentals()
    self.assertEqual(self.rentals.find_by_id(rental1.id), rental1, "rental not found by id")
    self.assertEqual(self.rentals.find_by_id(rental2.id), rental2, "rental not found by id")

  def test_find_by_id_exception(self):
    with self.assertRaises(RentalException):
      self.rentals.find_by_id(0)

  def test_find_by_booking_id(self):
    rental1, rental2 = self.fill_rentals()
    self.assertEqual(self.rentals.find_by_booking_id(rental1.booking.id), rental1, "rental not found by booking id")
    self.assertEqual(self.rentals.find_by_booking_id(rental2.booking.id), rental2, "rental not found by booking id")

  def test_find_by_customer_id(self):
    rental1, rental2 = self.fill_rentals()
    self.assertEqual(self.rentals.find_by_customer_id(rental1.booking.customer.id), [rental1], "rental not found by customer id")
    self.assertEqual(self.rentals.find_by_customer_id(rental2.booking.customer.id), [rental2], "rental not found by customer id")

if __name__ == '__main__':
  unittest.main()
