import unittest
from rental.company import Company
from rental.categories import Category, Categories
from rental.cars import Car, Cars
from rental.exceptions import RentalException

class CategoryTests(unittest.TestCase):
  def setUp(self):
    self.company = Company(name="TestComp")
    self.categories = Categories(self.company)
    self.cars = Cars(self.company)
           
  def test_get_label(self):
    category = Category(1, "A")
    self.assertEqual(category.getLabel(), "A (1)", "wrong label delivered")
  
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

  def test_delete(self):
    category = self.categories.add("A")
    self.categories.add("B")
    self.categories.delete(category.id)
    self.assertNotIn(category, self.categories.categories, "category not deleted")

  def test_delete_with_cars(self):
    category = self.categories.add("A")
    car = self.cars.add('Bon Voyage', 'red', "A")
    self.categories.delete(category.id)
    with self.assertRaises(RentalException):
      self.company.cars.find_by_id(car.id)

  def test_contains(self):
    cat1 = self.categories.add("A")
    cat2 = self.categories.add("B")
    self.assertTrue(self.categories.contains("B"), "wrong negative results")
    self.assertFalse(self.categories.contains("C"), "wrong positive results")

  def test_find_by_id(self):
    cat1 = self.categories.add("A")
    cat2 = self.categories.add("B")
    self.assertEqual(self.categories.find_by_id(cat1.id), cat1, "category not found by id")
  
  def test_find_by_id_error(self):
    with self.assertRaises(RentalException):
      self.categories.find_by_id(999999)

  def test_find_by_name(self):
    cat1 = self.categories.add("A")
    cat2 = self.categories.add("B")
    self.assertEqual(self.categories.find_by_name(cat1.name), cat1, "category not found by id")

  def test_find_by_name_error(self):
    with self.assertRaises(RentalException):
      self.categories.find_by_name("Nonexistent") 