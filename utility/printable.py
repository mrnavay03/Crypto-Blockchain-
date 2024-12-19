"""For accessing another print method."""

class Printable:
    def __repr__(self):
        return str(self.__dict__)