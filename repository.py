from abc import ABC, abstractmethod


class AbstractRepository(ABC):
    def __init__(self, model):
        self.model = model

    @abstractmethod
    def add(self, item):
        pass

    @abstractmethod
    def update(self, item):
        pass

    @abstractmethod
    def get(self, query):
        pass

    @abstractmethod
    def delete(self, id):
        pass

    @abstractmethod
    def get_all(self) -> list:
        pass


class PostgresRepository(AbstractRepository):
    def __init__(self, model):
        super().__init__(model)

    def add(self, item):
        item.save()

    def update(self, item):
        item.save()

    def get(self, query):
        results = self.model.select().where(query).limit(1).execute()
        return results[0] if len(results) > 0 else None

    def delete(self, id):
        item = self.get(self.model.id == id)
        item.delete_instance()

    def get_all(self, query="") -> list:
        if not query:
            results = self.model.select().execute()
            return results

        return self.model.select().execute()

    def exists(self, query=""):
        if query:
            exists = self.model.select().where(query).exists()
            return exists

        return False
