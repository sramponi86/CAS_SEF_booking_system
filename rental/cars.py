from dataclasses import dataclass, field
from rental import controller
from rental.exceptions import RentalException
from rental.company import Company

@dataclass
class Car:
  """
  Represents a rental car.

  Attributes:
      id (int): ID of the car.
      model (str): The model name of the car.
  """
  id: int
  model: str
  
  def getLabel(self):
    """
    Creates a human readable Label of the Car-Entity (used in the Webapp)

    Returns:
        str: The human readable label.
    """
    return f'{self.model} ({self.id})'

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

  def add(self, model: str) -> Car:
    """
    Add a new car to the fleet.

    Creates a new Car instance based on the provided model name 
    and adds it to the internal list of cars.

    Args:
        model (str): The model name of the new car.

    Returns:
        Car: The newly created Car instance.
    """
    car = Car(controller.nextId(), model)
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


