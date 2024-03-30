from dataclasses import dataclass, field
from rental import controller
from rental.exceptions import RentalException
from rental.company import Company
from rental.customers import Customer
from rental.cars import Car
from datetime import date

@dataclass
class Booking:
  """
  Represents a booking for a rental car.

  Attributes:
      id (int): ID of the booking.
      customer (Customer): The Customer making the booking.
      car (Car, optional): The specific Car requested (see note).
      period_start (date): The start date of the booking.
      period_end (date): The end date of the booking.
  """
  id: int
  customer: Customer
  car: Car
  period_start: date = field(repr=False)
  period_end: date = field(repr=False)

class Bookings:
  """
  Manages a collection of bookings.

  Attributes:
      bookings (list[Booking]): List that stores the Booking instances.
      company (Company): The rental company associated with the bookings.
  """

  def __init__(self, company: Company):
    """
    Creates a new Bookings instance for a given company.
    The list of bookings is initially empty.

    Args:
        company (Company): The rental company associated with the bookings.
    """
    self.bookings: list[Booking] = []
    self.company = company

  def get(self):
    """
    Retrieves all current bookings.

    This method provides a safe way to access a copy of the list of all bookings, ensuring the original list is not
    altered inadvertently.

    Returns:
        list[Booking]: Copy of the list of all the bookings.
    """
    return self.bookings.copy()

  def add(self, customer_id:int , period_start: date, period_end: date, car_id: int = None) -> Booking:
    """
    Create a booking and add it to the collection.

    Creates a new booking based on the provided details and adds it to the internal list of bookings.
    It requires the customer's ID and the start and end dates of the rental period. A specific car must
    be specified for the booking.

    Args:
        customer_id (int): The ID of the customer making the booking.
        period_start (date): The start date of the booking.
        period_end (date): The end date of the booking.
        car_id (int, optional): The ID of the specific car requested. Defaults to None.

    Returns:
        Booking: The newly create Booking instance, added to the list of bookings.
    """
    # TODO: Check that period_start < period_end
    customer = self.company.customers.find_by_id(customer_id)
    car = self.company.cars.find_by_id(car_id)
    booking = Booking(controller.nextId(), customer, car, period_start, period_end)
    print(f'Adding {booking}')
    self.bookings.append(booking)
    return booking

  def delete(self, id: int):
    """
    Delete a booking based on its ID. 
    
    Also deletes any associated rentals with the booking.

    Raises:
        RentalException: If no booking with the given ID is found.

    Args:
        id (int): The ID of the booking to delete.
    """
    booking = self.find_by_id(id)

    for rental in self.company.rentals.get():
      if rental.booking == booking:
        self.company.rentals.delete(rental.id)
        
    print(f'Deleting {booking}')
    self.bookings.remove(booking)

  def find_by_id(self, id: int):
    """
    Find a booking by its ID.

    Searches through the list of bookings to find a booking with the specified ID.

    Args:
        id (int): The ID of the booking to find.

    Raises:
        RentalException: If no booking with the given ID is found.

    Returns:
        Booking: The booking with the specified ID.
    """
    bookings = [b for b in self.bookings if b.id == id]
    assert len(bookings) <= 1, 'Unexpectedly found multiple bookings with id {id}'
    if bookings == []:
      raise RentalException(f"Couldn't find booking with id {id}")
    return bookings[0]
  
  def find_by_customer_id(self, customer_id: int):
    """
    Find bookings by customer ID.

    Args:
        customer_id (int): The ID of the customer whose bookings to find.

    Returns:
        list[Booking]: A list of bookings made by the specified customer.
    """
    return [b for b in self.bookings if b.customer.id == customer_id]
