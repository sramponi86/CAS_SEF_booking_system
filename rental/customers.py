from dataclasses import dataclass
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
    
  def getLabel(self):
    """
    Creates a human readable Label of the Car-Entity (used in the Webapp)

    Returns:
        str: The human readable label.
    """
    return f'{self.name}'
  
class Customers:
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

  def contains(self, name: str):
    """
    Checks if a customer with the specified name exists in the collection.

    Args:
        name (str): The name of the customer to check for.

    Returns:
        bool: True if a customer with the given name exists, False otherwise.
    """

    return False # TODO: Replace by proper implementation

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

    return self.customers[0] # TODO: Replace by proper implementation
