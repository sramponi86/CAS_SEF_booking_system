class Company:
  """
  Represents a rental company.

  Attributes:
      name (str): The name of the company.
      customers (Customers): The customers of the company.
      categories (Categories): The categories of cars a company offers.
      cars (Cars): The cars in the company's fleet.
      bookings (Bookings): The bookings made with the company.
      rentals (Rentals): The rentals of the company.
  """

  def __init__(self, name: str):
    """
    Creates a new Company instance.

    Args:
        name (str): The name of the company.
    """

    # Lazy import to avoid circular imports
    from rental import customers, cars, bookings, rentals, statistics, categories
    self.name = name
    self.customers = customers.Customers(self)
    self.cars = cars.Cars(self)
    self.bookings = bookings.Bookings(self)
    self.rentals = rentals.Rentals(self)
    self.categories = categories.Categories(self)
  
    statistics.attachTo(self)
