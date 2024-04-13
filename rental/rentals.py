from dataclasses import dataclass, field
from rental import controller
from rental.exceptions import RentalException
from rental.company import Company
from rental.cars import Car
from rental.bookings import Booking

@dataclass
class Rental:
  """
  Represents an ongoing rental associated with a booking and a car.

  Attributes:
      id (int): ID of the rental.
      booking (Booking): The booking associated with the rental.
      car (Car): The car associated with the rental.
  """
  id: int
  booking: Booking = field(repr=False)
  car: Car

class Rentals:
  """
  Manages a collection of rentals.

  Attributes:
      rentals (list[Rental]): List that stores the Rental instances.
      company (Company): The rental company associated with the rentals.
  """

  def __init__(self, company: Company):
    """
    Creates a new Rentals instance for a given company.
    The list of rentals is initially empty.

    Args:
        company (Company): The rental company associated with the rentals.
    """
    self.rentals: list[Rental] = []
    self.company = company

  def get(self):
    """
    Retrieves all rentals in the collection.

    Returns a copy of the internal list of rentals to prevent modifications to the original list.

    Returns:
        list[Rental]: Copy of the list of all rentals.
    """
    return self.rentals.copy()

  def add(self, booking_id: int):
    """
    Add a rental to the collection.

    Creates a new Rental instance based on the ID of the booking and adds it to the internal list of rentals. 
    This represents a customer trying to pick up a car for the given booking.

    Args:
        booking_id (int): The ID of the booking.

    Raises:
        RentalException: If the start date of the booking does not concide with today's date.
        RentalException: If a booking is for a specific car and that car is already rented.

    Returns:
        Rental: The newly created Rental instance, added to the list.
    """
    # NOTE: Could allow
    #         * a different period_start and period_end, e.g. if a sub-period of the original one
    booking = self.company.bookings.find_by_id(booking_id)
    car = booking.car
    period_start = booking.period_start
    period_end = booking.period_end
    rental = None
    if controller.today != period_start:
      raise RentalException(f'A car can only be picked up on the start-date of the booking ({period_start}). But today is {controller.today}')
    rentals_for_car = [r for r in self.rentals if r.car.id == car.id]
    for r in rentals_for_car:
      if (max(period_start, period_end) >= min(r.booking.period_start, r.booking.period_end) and 
          min(period_start, period_end) <= max(r.booking.period_start, r.booking.period_end)):
        raise RentalException(f'Car {car.getLabel()} cannot be rented for period {period_start} - {period_end}, because it has already been rented.')
    rental = Rental(controller.nextId(), booking, car)
    assert(rental != None) # Should always hold
    print(f'Adding {rental}')
    self.rentals.append(rental)
    return rental
  
  def delete(self, id: int):
    """
    Delete a rental from the collection by its ID.

    Args:
        id (int): The ID of the rental to delete.

    Raises:
        RentalException: If no rental with the given ID is found.
    """
    rental = self.find_by_id(id)
    print(f'Deleting {rental}')
    self.rentals.remove(rental)

  def find_by_id(self, id: int):
    """
    Find a rental by its ID.

    Searches the collection for a rental with the specified ID.

    Args:
        id (int): The ID of the rental to find.

    Raises:
        RentalException: If no rental with the given ID is found.

    Returns:
        Rental: The Rental instance with the specified ID.
    """
    rentals = [r for r in self.rentals if r.id == id]
    assert len(rentals) <= 1, 'Unexpectedly found multiple bookings with id {id}'
    if rentals == []:
      raise RentalException(f"Couldn't find rental with id {id}")    
    return rentals[0]
  
  def find_by_booking_id(self, booking_id: int):
    """
    Find a rental by its booking ID.

    Searches the collection for a rental associated with a booking with the specified ID.

    Args:
        booking_id (int): The ID of the booking associated with the rental to find.

    Raises:
        AssertionError: If more than one rental is found with the same booking ID.

    Returns:
        Rental | None: Returns the Rental instance that is associated with the specified booking ID. 
        If no rental is found that matches the booking ID, None is returned. 
    """
    rentals = [r for r in self.rentals if r.booking.id == booking_id]
    assert len(rentals) <= 1, 'Unexpectedly found multiple bookings with id {id}'
    if rentals == []:
      return None
    return rentals[0]

  def find_by_customer_id(self, customer_id: int):
    """
    Find a rental by its customer ID.

    Searches the collection for a rental made by a customer with the specified ID.

    Args:
        customer_id (int): The ID of the customer that made the rental to find.

    Returns:
        list[Rental]: Returns the Rental instance made by the specified customer ID.
    """
    return [r for r in self.rentals if r.booking.customer.id == customer_id]
