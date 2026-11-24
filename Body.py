
class Body:
    def __init__(self,mass,heat_capacity,temperature):
        if mass <= 0 or heat_capacity <= 0 or temperature < 0:
            raise ValueError("Invalid physical parameters for Body")
        self.mass= mass
        self.heat_capacity=heat_capacity
        self.temperature=temperature

    def add_heat(self,heat):
        dalta_t= heat/(self.mass* self.heat_capacity)
        self.temperature+=dalta_t
        return self.temperature



if __name__ == "__main__":
    body1= Body(100, 0.15, 200)
    print(f"{body1.add_heat(20)}")
    print(f"{body1.add_heat(-40)}")