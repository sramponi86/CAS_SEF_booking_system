import unittest
from rental import controller
from datetime import date

class ControllerTests(unittest.TestCase):
  def setUp(self):
    pass

class BookingsTests(unittest.TestCase):
  def setUp(self):
    pass

  def test_next_id(self):
    controller.setId(1)
    self.assertEqual(controller.nextId(), 2)

  def test_set_id(self):
    controller.setId(1)
    self.assertEqual(controller.current_id, 1)

  def test_set_today(self):
    controller.setToday(date.today())
    self.assertEqual(controller.today, date.today())
