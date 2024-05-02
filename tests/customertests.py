import unittest
from rental.company import Company
from rental.customers import Customer, Customers
from rental.exceptions import RentalException
from contextlib import suppress

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

  def test_get_empty(self):
    self.assertEqual(self.customers.get(), [], 'customers not retrieved')

  def test_get_not_empty(self):
    self.customers.add('Gabi Gaspedal')
    self.customers.add('Keith Elam')
    self.assertEqual(len(self.customers.get()), 2, 'customers not retrieved')

  def test_get_copy(self):
    customers = self.customers.get()
    customers.append(Customer(1, 'Random House'))
    self.assertEqual(len(self.customers.get()), 0, 'customers not retrieved')

  def test_delete(self):
    c1 = self.customers.add('Gabi Gaspedal')
    c2 = self.customers.add('Keith Elam')
    self.customers.delete(c1.id)
    self.assertEqual(self.customers.get(), [c2], 'customer not deleted')

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

  def test_default_points(self):
    test = self.customers.add('Test Customer')
    self.assertEqual(self.customers.get_points(test.id), 0)

  def test_add_points(self):
    test = self.customers.add('Test Customer')
    self.customers.add_points(test.id, 10)
    self.assertEqual(self.customers.get_points(test.id), 10)

  def test_negative_points(self):
    test = self.customers.add('Test Customer')

    with self.assertRaises(RentalException):
      self.customers.add_points(test.id, -10)

  def test_add_string_as_points(self):
    test = self.customers.add('Test Customer')

    with self.assertRaises(Exception):
      self.customers.add_points(test.id, "test")

  def test_add_points_incorrect_id(self):
    self.customers.add('Test Customer')

    with self.assertRaises(RentalException):
      self.customers.add_points("testid", 10)

  def test_get_points_incorrect_id(self):
    with self.assertRaises(RentalException):
      self.customers.get_points("testid")

  def test_get_status(self):
    test = self.customers.add('Test Customer')
    self.assertEqual(self.customers.get_status(test.id), "Basic")

  def test_get_status_incorrect_id(self):
    with self.assertRaises(RentalException):
      self.customers.get_status("testid")

  def test_update_status(self):
    test = self.customers.add('Test Customer')
    with self.assertRaisesRegex(RentalException, "You reached the Newbie status"):
      self.customers.add_points(test.id, 200)

  def test_update_status_expert(self):
    test = self.customers.add('Test Customer')
    with self.assertRaisesRegex(RentalException, "You reached the Expert status"):
      self.customers.add_points(test.id, 300)

  def test_update_status_prof(self):
    test = self.customers.add('Test Customer')
    with self.assertRaisesRegex(RentalException, "You reached the Professional status"):
      self.customers.add_points(test.id, 501)

  def test_update_status_serial(self):
    test = self.customers.add('Test Customer')
    with self.assertRaisesRegex(RentalException, "You reached the Serial Renter status"):
      self.customers.add_points(test.id, 1000)

  def test_subtract(self):
    test = self.customers.add('Test Customer')
    with suppress(RentalException):
      self.customers.add_points(test.id, 1000)
    with self.assertRaisesRegex(RentalException, "You reached the Basic status"):
      self.customers.subtract_points(test.id, 1000)

  def test_subtract_negative(self):
    test = self.customers.add('Test Customer')
    with suppress(RentalException):
      self.customers.add_points(test.id, 1000)
    with self.assertRaisesRegex(RentalException, "You reached the Basic status"):
      self.customers.subtract_points(test.id, 1001)

if __name__ == '__main__':
  unittest.main()
