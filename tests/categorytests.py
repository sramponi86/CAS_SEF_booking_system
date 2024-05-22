import unittest
from rental.company import Company
from rental.categories import Category, Categories
from rental.cars import Car, Cars
from rental.exceptions import RentalException

class CategoryTests(unittest.TestCase):
  def setUp(self):
    self.company = Company(name="TestComp")
    self.categories = Categories(self.company)

  def test_get_empty(self):
    self.assertEqual(self.categories.get(), [], 'categories not retrieved')

  def test_get_not_empty(self):
    self.categories.add("A")
    self.categories.add("B")
    self.assertEqual(len(self.categories.get()), 2, 'categories not retrieved')

  def test_add(self):
    cat1 = self.categories.add("A")
    cat2 = self.categories.add("B")
    self.assertCountEqual([cat1, cat2], self.categories.categories, "categories not added")



