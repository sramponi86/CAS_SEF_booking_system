from datetime import date

today: date = date.today()
current_id: int = 0

def setToday(date: date):
  """
  Sets the `today` variable to a specified date.

  Use this to simulate days passing. Initially set to the real-world current date.

  Args:
      date (date): The new date which is `today`.
  """
  global today
  print(f'Set "today" to {date}')
  today = date

def nextId():
  """
  Generates and returns the next unique identifier (ID).

  Returns:
      int: The generated ID.
  """
  global current_id
  current_id += 1
  return current_id

def setId(id: int):
  """
  Sets the current unique id for entities. 
  This is used to reestablish id's after a restart from persistence.

  Args:
      id (int): The current id to be used when providing unique ids
  """
  global current_id
  current_id = id




