import unittest
import datetime as dt
from rental.company import Company
from rental.bookings import Booking, Bookings
from rental.exceptions import RentalException
from rental.customers import Customer
from rental.cars import Car

class BookingTests(unittest.TestCase):
  def setUp(self):
    pass

  def test_constructor(self):
    customer = Customer(1, 'Dandy McDuck')
    car = Car(1, 'Opel Kadett')
    booking = Booking(1, customer, car, dt.date(2024, 3, 7), dt.date(2024, 3, 14))

    self.assertEqual(booking.id, 1, 'incorrect id after construction')
    self.assertEqual(booking.customer, customer, 'incorrect customer after construction')
    self.assertEqual(booking.car, car, 'incorrect car after construction')
    self.assertEqual(booking.period_start, dt.date(2024, 3, 7), 'incorrect period_start after construction')
    self.assertEqual(booking.period_end, dt.date(2024, 3, 14), 'incorrect period_end after construction')

class BookingsTests(unittest.TestCase):
  def setUp(self):
    company = Company('Šmertz')
    self.car = company.cars.add('D12')
    self.customer = company.customers.add('Dandy McDuck')
    self.bookings = company.bookings

  def test_add_car_id(self):
    booking = self.bookings.add(self.customer.id, dt.date(2024, 3, 7), dt.date(2024, 4, 7), self.car.id)
    self.assertEqual(booking, self.bookings.bookings[0], "booking not added")

  def test_add_incorrect_period_exception(self):
    customer = self.customer
    car = self.car

    with self.assertRaises(RentalException):
      self.bookings.add(customer.id, dt.date(2000, 11, 11), dt.date(2000, 11, 10), car.id)

  def test_add_nonexisting_car(self):
    customer = self.customer
    car = self.cars

    with self.assertRaises(RentalException):
      self.bookings.add(customer.id, dt.date(2048, 8, 4), dt.date(2048, 8, 16), car.id)

  def test_get_empty(self):
    self.assertEqual(self.bookings.get(), [], "bookings not retrieved")

  def test_get_not_empty(self):
    booking1 = self.bookings.add(self.customer.id, dt.date(2024, 3, 7), dt.date(2024, 4, 7), self.car.id)
    booking2 = self.bookings.add(self.customer.id, dt.date(2024, 3, 7), dt.date(2024, 4, 7), self.car.id)
    self.assertCountEqual(self.bookings.get(), [booking1, booking2], "bookings not retrieved")

  def test_get_copy(self):
    bookings = self.bookings.get()
    bookings.append(Booking(1, self.customer, self.car, dt.date(2024, 3, 7), dt.date(2024, 4, 7)))
    self.assertEqual(len(self.bookings.get()), 0, "bookings not retrieved")

  def test_delete(self):
    booking = self.bookings.add(self.customer.id, dt.date(2024, 3, 7), dt.date(2024, 4, 7), self.car.id)
    self.bookings.delete(booking.id)
    self.assertEqual(self.bookings.bookings, [], "booking not deleted")
  
  def test_find_by_id(self):
    booking = self.bookings.add(self.customer.id, dt.date(2024, 3, 7), dt.date(2024, 4, 7), self.car.id)
    self.assertEqual(self.bookings.find_by_id(booking.id), booking, "booking not found by id")

  def test_find_by_id_exception(self):
    with self.assertRaises(RentalException):
      self.bookings.find_by_id(0)

  def test_find_by_customer_id(self):
    booking1 = self.bookings.add(self.customer.id, dt.date(2024, 3, 7), dt.date(2024, 4, 7), self.car.id)
    booking2 = self.bookings.add(self.customer.id, dt.date(2024, 3, 7), dt.date(2024, 4, 7), self.car.id)
    self.assertCountEqual(self.bookings.find_by_customer_id(self.customer.id), [booking1, booking2], "booking not found by customer id")

if __name__ == '__main__':
  unittest.main()
