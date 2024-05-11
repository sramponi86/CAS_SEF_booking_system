from dataclasses import dataclass
from rental import controller
from rental.exceptions import RentalException
from rental.company import Company

@dataclass
class Category:
  """
  Represents a category of cars.

  Attributes:
      id (int): ID of the category.
      name (str): Name of the category.
  """ 
  id: int
  name: str

  def getLabel(self):
    """
    Creates a human readable Label of the Car-Entity (used in the Webapp)

    Returns:
        str: The human readable label.
    """
    return f'{self.name} ({self.id})'

class Categories:
  """
  Manages a collection of categories.

  Attributes:
      categories (list[Category]): List that stores the Category instances.
      company (Company): The rental company associated with the categories.
  """

  def __init__(self, company: Company):
    """
    Creates a new Categories instance for a given company.
    The list of categories is initially empty.

    Args:
        company (Company): The rental company associated with the categories.
    """
    self.categories: list[Category] = []
    self.company = company

  def get(self):
    """
    Retrieves all categories in the collection.

    Returns a copy of the internal list of categories to prevent modifications to the original list.

    Returns:
        list[Category]: Copy of the list of all categories.
    """
    return self.categories.copy()

  def add(self, name: str):
    """
    Add a new category to the collection.

    Creates a new Category instance based on the provided name and adds it to the internal list of categories.

    Args:
        name (str): The name of the new category.

    Returns:
        Category: The newly created Category instance, added to the list.
    """
    category = Category(controller.nextId(), name)
    print(f'Adding {category}')
    self.categories.append(category)
    return category
  
  def delete(self, id: int):
    """
    Delete a category from the collection by its ID.

    Also removes any associated bookings, rentals and cars before deleting the category.

    Raises:
        RentalException: If no category with the given ID is found.

    Args:
        id (int): The ID of the category to delete.
    """
    category = self.find_by_id(id) # Category to be deleted
    cars = self.company.cars.find_by_category_id(category.id) # Cars from the to-be-deleted category
    bookings = self.company.bookings.get()

    for c in cars:
      self.company.cars.delete(c.id)

    for b in bookings:
      if b.car.category == category:
        self.company.bookings.delete(b.id)

    self.categories.remove(category)
  
  def contains(self, name: str):
    """
    Checks if a category with the specified name exists in the collection.

    Args:
        name (str): The name of the category to check for.

    Returns:
        bool: True if a category with the given name exists, False otherwise.
    """
    for c in self.categories:
      if c.name == name:
        return True
    return False

  def find_by_id(self, id: int):
    """
    Find a category by its ID.

    Searches the collection for a category with the specified ID.

    Args:
        id (int): The ID of the category to find.

    Raises:
        RentalException: If no category with the given ID is found.

    Returns:
        Category: The Category instance with the specified ID.
    """
    for c in self.categories:
      if c.id == id:
        return c
    raise RentalException(f"Couldn't find car category with id {id}")

  def find_by_name(self, name: str):
    """
    Find a category by its name.

    Searches the collection for a category with the specified name.

    Args:
        name (str): The name of the category to find.

    Raises:
        RentalException: If no category with the given name is found.

    Returns:
        Category: The Category instance with the specified name.
    """
    for c in self.categories:
      if c.name == name:
        return c
    raise RentalException(f"Couldn't find car category with name {name}")   