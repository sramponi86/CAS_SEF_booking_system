import unittest
from rental.company import Company
from rental.customers import Customer, Customers
from rental.exceptions import RentalException

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


if __name__ == '__main__':
  unittest.main()
