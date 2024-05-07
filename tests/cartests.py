import unittest
from rental.company import Company
from rental.cars import Car, Cars
from rental.exceptions import RentalException

class CarTests(unittest.TestCase):
  def setUp(self):
    pass

  def test_constructor(self):
    car = Car(1, 'Opel Kadett', 'orange', "B")
    self.assertEqual(car.id, 1, 'incorrect id after construction')
    self.assertEqual(car.model, 'Opel Kadett', 'incorrect model after construction')

class CarsTests(unittest.TestCase):
  def setUp(self):
    company = Company('Šmertz')
    self.cars = company.cars

  def test_add(self):
    car1 = self.cars.add('Bon Voyage', 'red', "A")
    car2 = self.cars.add('VW Jetta', 'green', "B")
    self.assertCountEqual([car1, car2], self.cars.cars, "cars not added")

  def test_get_empty(self):
    self.assertEqual(self.cars.get(), [], "cars not retrieved")

  def test_get_not_empty(self):
    self.cars.add('Bon Voyage', 'red', "A")
    self.cars.add('VW Jetta', 'green', "B")
    self.assertEqual(len(self.cars.get()), 2, "cars not retrieved")
  
  def test_get_copy(self):
    cars = self.cars.get()
    cars.append(Car(1, 'Random House', 'strange color', "A"))
    self.assertEqual(len(self.cars.get()), 0, "cars not retrieved")

  def test_delete(self):
    car = self.cars.add('Bon Voyage', 'red', "A")
    self.cars.add('VW Jetta', 'green', "B")
    self.cars.delete(car.id)
    self.assertNotIn(car, self.cars.cars, "car not deleted")

  def test_find_by_id(self):
    car1 = self.cars.add('Bon Voyage', 'red', "A")
    self.cars.add('VW Jetta', 'green', "B")
    self.assertEqual(self.cars.find_by_id(car1.id), car1, "car not found by id")

  def test_find_by_id_exception(self):
    with self.assertRaises(RentalException):
      self.cars.find_by_id(0)

  def test_delete_car_id_with_false_id_exception(self):
    with self.assertRaises(Exception):
      self.cars.delete("unexisting")

if __name__ == '__main__':
  unittest.main()
