import unittest
from rental.company import Company
from rental.cars import Car, Cars
from rental.exceptions import RentalException

class CarTests(unittest.TestCase):
  def setUp(self):
    pass

  def test_constructor(self):
    car = Car(1, 'Opel Kadett')
    self.assertEqual(car.id, 1, 'incorrect id after construction')
    self.assertEqual(car.model, 'Opel Kadett', 'incorrect model after construction')

class CarsTests(unittest.TestCase):
  def setUp(self):
    company = Company('Šmertz')
    self.cars = company.cars

  def test_add(self):
    car1 = self.cars.add('Bon Voyage')
    car2 = self.cars.add('VW Jetta')
    self.assertCountEqual([car1, car2], self.cars.cars, "cars not added")

  def test_get_empty(self):
    self.assertEqual(self.cars.get(), [], "cars not retrieved")

  def test_get_not_empty(self):
    self.cars.add('Bon Voyage')
    self.cars.add('VW Jetta')
    self.assertEqual(len(self.cars.get()), 2, "cars not retrieved")
  
  def test_get_copy(self):
    cars = self.cars.get()
    cars.append(Car(1, 'Random House'))
    self.assertEqual(len(self.cars.get()), 0, "cars not retrieved")

  def test_delete(self):
    car = self.cars.add('Bon Voyage')
    self.cars.add('VW Jetta')
    self.cars.delete(car.id)
    self.assertNotIn(car, self.cars.cars, "car not deleted")

  def test_find_by_id(self):
    car1 = self.cars.add('Bon Voyage')
    self.cars.add('VW Jetta')
    self.assertEqual(self.cars.find_by_id(car1.id), car1, "car not found by id")

  def test_find_by_id_exception(self):
    with self.assertRaises(RentalException):
      self.cars.find_by_id(0)


if __name__ == '__main__':
  unittest.main()
