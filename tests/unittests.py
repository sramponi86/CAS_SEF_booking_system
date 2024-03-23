import unittest
import datetime as dt
from rental.company import Company
from rental.categories import Category
from rental.cars import Car
from rental.customers import Customer
from rental.exceptions import RentalException
from rental import controller

class CarTests(unittest.TestCase):
  def setUp(self):
    pass

  def test_constructor(self):
    category = Category(1, 'Medium')
    car = Car(1, 'Opel Kadett', category)
    self.assertEqual(car.id, 1, 'incorrect id after construction')
    self.assertEqual(car.model, 'Opel Kadett', 'incorrect model after construction')
    self.assertEqual(car.category, category)

class CustomerTests(unittest.TestCase):
  def setUp(self):
    pass

  def test_constructor(self):
    customer = Customer(77, 'Dandy McDuck')
    self.assertEqual(customer.id, 77, 'incorrect id after construction')    
    self.assertEqual(customer.name, 'Dandy McDuck', 'incorrect name after construction')

class CustomersTests(unittest.TestCase):
  def setUp(self):
    self.customers = Company('Šmertz').customers

  def test_add(self):
    customer = self.customers.add('Özhan Oktan')
    self.assertEqual(customer.name, 'Özhan Oktan', 'incorrect name after construction')

  def test_contains(self):
    self.customers.add('Gabi Gaspedal')
    self.customers.add('Keith Elam')

    self.assertTrue(self.customers.contains('Gabi Gaspedal'))
    self.assertTrue(self.customers.contains('Keith Elam'))

  def test_not_contains(self):
    self.customers.add('Phillip')

    self.assertFalse(self.customers.contains('Philip'))

  def test_find_by_id(self):
    jack = self.customers.add('Jack Rabbit')
    jane = self.customers.add('Jane Rabbit')

    self.assertEqual(self.customers.find_by_id(jack.id), jack)
    self.assertEqual(self.customers.find_by_id(jane.id), jane)

  def test_find_by_id_exception(self):
    telsa = self.customers.add('Telsa')

    with self.assertRaises(RentalException):
      self.customers.find_by_id(telsa.id + 100)

class CompanyTests(unittest.TestCase):
  def setUp(self):
    company = Company('Šmertz')
    
    category_small = company.categories.add('Small')
    category_medium = company.categories.add('Medium')
    
    company.cars.add('D12', category_small.id)
    company.cars.add('VW Jetta', category_medium.id)
    company.cars.add('Bon Voyage', category_medium.id)
    
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
    customer = self.company.customers.get()[0] # Any customer ...
    car = self.company.cars.get()[0] # ... and car would do

    booking = self.company.bookings.add(customer.id, dt.date(2024, 3, 7), dt.date(2024, 3, 14), car_id=car.id)
    controller.setToday(dt.date(2024, 3, 7))
    rental = self.company.rentals.add(booking.id)

    self.assertEqual(rental.car, booking.car)
    self.assertEqual(rental.booking, booking)

    booking = self.company.bookings.add(customer.id, dt.date(2024, 3, 5), dt.date(2024, 3, 6), car_id=car.id)
    controller.setToday(dt.date(2024, 3, 5))
    rental = self.company.rentals.add(booking.id)

    booking = self.company.bookings.add(customer.id, dt.date(2024, 3, 10), dt.date(2024, 3, 16), car_id=car.id)
    controller.setToday(dt.date(2024, 3, 10))
    with self.assertRaises(RentalException):
      self.company.rentals.add(booking.id)

  def test_add_rental_by_car_category_unique(self):
    customer = self.company.customers.get()[1] # Any customer ...
    category = self.company.categories.get()[1] # ... and category would do

    booking = self.company.bookings.add(customer.id, dt.date(2024, 3, 7), dt.date(2024, 3, 14), category_id=category.id)
    controller.setToday(dt.date(2024, 3, 7))
    rental = self.company.rentals.add(booking.id)

    self.assertIn(rental.car, self.company.cars.find_by_category_id(category.id))

  def test_add_rental_by_car_category_2(self):
    customer = self.company.customers.get()[0]
    category = self.company.categories.find_by_name('Medium')

    available_cars_in_category = self.company.cars.find_by_category_id(category.id)

    booking = self.company.bookings.add(customer.id, dt.date(2024, 3, 7), dt.date(2024, 3, 14), category_id=category.id)
    controller.setToday(dt.date(2024, 3, 7))
    rental_1 = self.company.rentals.add(booking.id)

    self.assertIn(rental_1.car, available_cars_in_category)

    booking = self.company.bookings.add(customer.id, dt.date(2024, 3, 6), dt.date(2024, 3, 8), category_id=category.id)
    controller.setToday(dt.date(2024, 3, 6))
    rental_2 = self.company.rentals.add(booking.id)

    available_cars_in_category.remove(rental_1.car)
    self.assertIn(rental_2.car, available_cars_in_category)    

if __name__ == '__main__':
  unittest.main()
