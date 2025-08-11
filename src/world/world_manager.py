class World:
    def __init__(self, name, world_data):
        self.name = name
        self.entities = []
        self.world_loaded = self.load_world_data(world_data)
        
    def load_world_data(self, world_data):
        """Carga los datos del mundo desde un archivo o fuente de datos"""
        with open(world_data, 'r') as file:
            data = file.read()
        return data.splitlines()
        
    def get_world_data(self):
        """Devuelve los datos del mundo"""
        return self.world_loaded

    def add_entity(self, entity):
        self.entities.append(entity)

    def remove_entity(self, entity):
        if entity in self.entities:
            self.entities.remove(entity)

    def get_entities(self):
        return self.entities

    def __str__(self):
        return f"World: {self.name}, Entities: {len(self.entities)}"