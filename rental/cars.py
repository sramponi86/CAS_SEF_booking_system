from dataclasses import dataclass, field
from rental import controller
from rental.exceptions import RentalException
from rental.company import Company
from rental.categories import Category

@dataclass
class Car:
  """
  Represents a rental car.

  Attributes:
      id (int): ID of the car.
      model (str): The model name of the car.
      category (Category): The category the car belongs to.
  """
  id: int
  model: str
  category: Category = field(repr=False)

class Cars:
  """
  Manages a collection (fleet) of cars.

  Attributes:
      cars (list[Car]): List that stores the Car instances.
      company (Company): The rental company associated with the fleet of cars.
  """

  def __init__(self, company: Company):
    """
    Creates a new Cars instance for a given company.
    The list of cars is initially empty.

    Args:
        company (Company): The rental company associated with the fleet of cars.
    """
    self.cars: list[Car] = []
    self.company = company

  def get(self):
    """
    Retrieve all cars in the fleet.

    Returns a copy of the internal list of cars to ensure the original list is not modified.

    Returns:
        list[Car]: A copy of the list of all cars.
    """
    return self.cars.copy()

  def add(self, model: str, category_id: int) -> Car:
    """
    Add a new car to the fleet.

    Creates a new Car instance based on the provided model name and category ID, 
    and adds it to the internal list of cars.

    Args:
        model (str): The model name of the new car.
        category_id (int): The ID of the category the new car belongs to.

    Returns:
        Car: The newly created Car instance.
    """
    category = self.company.categories.find_by_id(category_id)
    car = Car(controller.nextId(), model, category)
    print(f'Adding {car}')
    self.cars.append(car)
    return car

  def delete(self, id: int):
    """
    Delete a car from the fleet by its ID.

    Also checks and removes any bookings and rentals associated with this car before deleting it.

    Args:
        id (int): The ID of the car to delete.
    """
    car = self.find_by_id(id)

    for booking in self.company.bookings.get():
      if booking.car == car:
        self.company.bookings.delete(booking.id)
        
    print(f'Deleting {car}')
    self.cars.remove(car)

  def find_by_id(self, id: int):
    """
    Find a car by its ID.

    Searches through the list of cars to find a car with the specified ID.

    Args:
        id (int): The ID of the car to find.

    Raises:
        RentalException: If no car with the given ID is found.

    Returns:
        Car: The car with the specified ID.
    """
    car = None
    for c in self.cars:
      if c.id == id:
        car = c
        break
    if car == None:
      raise RentalException(f"Couldn't find car with id {id}")
    return car

  def find_by_category_id(self, category_id: int):
    """
    Find cars by their category ID.

    Returns a list of cars that belong to the specified category.

    Args:
        category_id (int): The ID of the category to find cars in.

    Returns:
        list[Car]: A list of Car instances that belong to the specified category.
    """
    return [car for car in self.cars if car.category.id == category_id]

