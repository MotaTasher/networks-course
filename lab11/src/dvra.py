import threading
import queue
import time

class Router(threading.Thread):
    def __init__(self, name):
        super().__init__()
        self.name = name
        self.routes = {name: (name, 0)}
        self.neighbors = {}
        self.queue = queue.Queue()
        self.stop_event = threading.Event()

    def set_neighbor(self, neighbor, cost):
        self.neighbors[neighbor] = cost
        self.routes[neighbor.name] = (neighbor.name, cost)

    def run(self):
        while not self.stop_event.set():
            time.sleep(0.03)
            self.send_updates()
            try:
                message = self.queue.get(timeout=0.01)
                self.process_message(message)    
                self.queue.task_done()
            except queue.Empty:
                continue

    def process_message(self, message):
        sender, data = message
        updated = False
        for dest, (hop, cost) in self.routes.items():
            if hop == sender.name:
                if dest in data.keys():
                    new_cost = data[dest][1] + self.routes[sender.name][1]
                    self.routes[dest] = (hop, new_cost)
                else:
                    self.routes.pop(dest)

        for dest, (hop, cost) in data.items():
            new_cost = cost + self.routes[sender.name][1]
            if dest not in self.routes or self.routes[dest][1] > new_cost:
                self.routes[dest] = (sender.name, new_cost)
                updated = True

        return updated

    def send_updates(self):
        for neighbor in self.neighbors:
            neighbor.queue.put((self, self.routes.copy()))

    def stop(self):
        self.stop_event.set()

    def __str__(self):
        return f"Router {self.name}: {self.routes}"

def simulate_routing():
    r0 = Router('0')
    r1 = Router('1')
    r2 = Router('2')
    r3 = Router('3')

    r0.set_neighbor(r1, 1)
    r0.set_neighbor(r3, 7)
    r1.set_neighbor(r0, 1)
    r1.set_neighbor(r2, 1)
    r1.set_neighbor(r3, 3)
    r2.set_neighbor(r1, 1)
    r2.set_neighbor(r3, 2)
    r3.set_neighbor(r0, 7)
    r3.set_neighbor(r1, 3)
    r3.set_neighbor(r2, 2)

    routers = [r0, r1, r2, r3]

    for router in routers:
        router.start()

    print("Initial routing tables:")
    for router in routers:
        print(router)

    print("\nChanging cost of the link between Router 0 and Router 3 to 2...")
    time.sleep(0.5)
    r0.set_neighbor(r3, 2)
    r3.set_neighbor(r0, 2)

    for router in routers:
        print(router)
        router.stop()
    time.sleep(0.5)


    print("\nUpdated routing tables after changing the link cost:")
    for router in routers:
        print(router)
        router.stop()


if __name__ == "__main__":
    simulate_routing()
