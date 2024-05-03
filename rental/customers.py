from dataclasses import dataclass
from patterns.observer import Subject
from rental import controller
from rental.exceptions import RentalException
from rental.company import Company

@dataclass
class Customer:
  """
  Represents a customer.

  Attributes:
      id (int): ID of the customer.
      name (str): Name of the customer.
  """
  id: int
  name: str
  points: int = 0
  status: str = "Basic"
    
  def getLabel(self):
    """
    Creates a human readable Label of the Car-Entity (used in the Webapp)

    Returns:
        str: The human readable label.
    """
    return f'{self.name}'
  
class Customers(Subject):
  """
  Manages a collection of customers.

  Attributes:
      customers (list[Customer]): List that stores the Customer instances.
      company (Company): The rental company associated with the customers.
  """

  def __init__(self, company: Company):
    """
    Creates a new Customers instance for a given company.
    The list of customers is initially empty.

    Args:
        company (Company): The rental company associated with the customers.
    """
    super().__init__()
    self.customers: list[Customer] = []
    self.company = company

  def get(self):
    """
    Retrieves all customers in the collection.

    Returns a copy of the internal list of customers to prevent modifications to the original list.

    Returns:
        list[Customer]: Copy of the list of all customers.
    """
    return self.customers.copy()
  
  def add(self, name: str):
    """
    Add a new customer to the collection.

    Creates a new Customer instance based on the provided name and adds it to the internal list of customers.

    Args:
        name (str): The name of the new customer.

    Returns:
        Customer: The newly created Customer instance, added to the list.
    """
    customer = Customer(controller.nextId(), name)
    print(f'Adding {customer}')
    self.customers.append(customer)
    self.notify()
    return customer
   

  def delete(self, id: int):
    """
    Delete the customer from the collection by its ID.

    Also removes any associated bookings and rentals before deleting the customer.

    Raises:
        RentalException: If no customer with the given ID is found.

    Args:
        id (int): The ID of the customer to delete.
    """
    customer = self.find_by_id(id)
       
    for booking in self.company.bookings.get():
      if booking.customer == customer:
        self.company.bookings.delete(booking.id)
    
    print(f'Deleting {customer}')
    self.customers.remove(customer)
    self.notify()

  def contains(self, name: str):
    """
    Checks if a customer with the specified name exists in the collection.

    Args:
        name (str): The name of the customer to check for.

    Returns:
        bool: True if a customer with the given name exists, False otherwise.
    """
    match = False
    for client in self.customers:
      if(client.name == name):
        match = True

    return match

  def find_by_id(self, id: int):
    """
    Find a customer by its ID.

    Searches the collection for a customer with the specified ID.

    Args:
        id (int): The ID of the customer to find.

    Raises:
        RentalException: If no customer with the given ID is found.

    Returns:
        Customer: The Customer instance with the specified ID.
    """
    retrieved_customer = None
    for customer in self.customers:
      if customer.id == id:
        retrieved_customer = customer
        break

    if retrieved_customer == None:
      raise RentalException(f"Couldn't find customer with id {id}")
    
    return retrieved_customer

  def add_points(self, id: int, points: int):
    if points < 0:
      raise RentalException(f"Points cannot be negative")
    
    customer = self.find_by_id(id)
    customer.points += points
    self.update_status(id)
    self.notify_points()

  def subtract_points(self, id: int, points: int):
    if points < 0:
      raise RentalException(f"Points cannot be negative")
    
    customer = self.find_by_id(id)
    if customer.points-points < 0:
      customer.points = 0
    else:
      customer.points -= points

    self.update_status(id)
    self.notify_points()

  def get_points(self, id: int):
    customer = self.find_by_id(id)
    return customer.points

  def get_status(self, id: int):
    customer = self.find_by_id(id)
    
    return customer.status
  
  def update_status(self, id: int):
    customer = self.find_by_id(id)
    current_points = self.get_points(id)
    if (current_points <= 100):
      if(customer.status != "Basic"):
        customer.status = "Basic"
        raise RentalException(f"You reached the Basic status")
    elif (current_points > 100) & (current_points <= 200):
      if(customer.status != "Newbie"):
        customer.status = "Newbie"
        raise RentalException(f"You reached the Newbie status")
    elif (current_points > 200) & (current_points <= 500):
      if(customer.status != "Expert"):
        customer.status = "Expert"
        raise RentalException(f"You reached the Expert status")
    elif (current_points > 500) & (current_points <= 800):
      if(customer.status != "Professional"):
        customer.status = "Professional"
        raise RentalException(f"You reached the Professional status")
    elif (current_points > 800):
      if(customer.status != "Serial Renter"):
        customer.status = "Serial Renter"
        raise RentalException(f"You reached the Serial Renter status")
      
    self.notify_points()