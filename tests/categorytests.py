import unittest
from rental.company import Company
from rental.categories import Category, Categories
from rental.cars import Car, Cars
from rental.exceptions import RentalException

class CategoryTests(unittest.TestCase):
  def setUp(self):
    pass

  def test_get_empty(self):
    self.assertEqual(self.categories.get(), [], 'categories not retrieved')

  def test_get_not_empty(self):
    self.categories.add("A")
    self.categories.add("B")
    self.assertEqual(len(self.categories.get()), 2, 'categories not retrieved')
    

