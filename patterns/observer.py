from __future__ import annotations 
from abc import ABC, abstractmethod  

class Subject:
  """
  The Subject declares a set of methods for managing observers.
  """

  def __init__(self):
    self.observers: list[Observer] = []

  def attach(self, observer: Observer) -> None:
    """
    Attach an observer to the subject.
    """
    self.observers.append(observer)

  def detach(self, observer: Observer) -> None:
    """
    Detach an observer from the subject.
    """
    self.observers.remove(observer)

  def notify(self) -> None:
    """
    Notify all observers about an event. 
    This method must be called at apropriate places in the Subject
    """
    for observer in self.observers:  
        observer.update(self)

class Observer(ABC): 
  """
  The Observer interface declares the update method, called by subjects.
  """

  @abstractmethod 
  def update(self, subject: Subject) -> None:
    """
    Receive update from subject.
    """
    pass