from abc import ABC, abstractmethod
from repository import PostgresRepository


class AbstractFactory(ABC):
    @abstractmethod
    def create(self):
        pass


class RepositoryFactory(AbstractFactory):
    def __init__(self, model):
        self.model = model

    def create(self):
        return PostgresRepository(self.model)
