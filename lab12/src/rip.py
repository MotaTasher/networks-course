import json
import random
import ipaddress

class Router:
    cnt_routers = 0
    
    def __init__(self, ip):
        self.id = Router.cnt_routers
        Router.cnt_routers += 1
        self.ip = ip
        self.neighbors = {}
        self.routing_table = {ip: (ip, 0)}  # Initial route to itself with metric 0

    def add_neighbor(self, neighbor_ip, metric):
        self.neighbors[neighbor_ip] = metric
        self.routing_table[neighbor_ip] = (neighbor_ip, metric)


    def update_routing_table(self, updates):
        for dest_ip, (next_hop, metric) in updates.items():
            real_metric = metric + self.routing_table[next_hop][1]
            if dest_ip not in self.routing_table or self.routing_table[dest_ip][1] > real_metric:
                self.routing_table[dest_ip] = (next_hop, real_metric)

    def get_routing_updates(self):
        updates = {}
        for dest_ip, (next_hop, metric) in self.routing_table.items():
            updates[dest_ip] = (self.ip, metric)
        return updates
    
    def to_dict(self):
        return {
            'ip': self.ip,
            'neighbors': self.neighbors
        }

def generate_random_network(num_routers=5):
    routers = {}
    for i in range(num_routers):
        ip = str(ipaddress.IPv4Address(random.randint(0, 2**32 - 1)))
        routers[ip] = Router(ip)
    
    for router in routers.values():
        neighbors = random.sample(list(routers.keys()), random.randint(1, num_routers - 1))
        for neighbor in neighbors:
            if neighbor != router.ip:
                metric = random.randint(1, 127)
                router.add_neighbor(neighbor, metric)
                routers[neighbor].add_neighbor(router.ip, metric)
    
    return routers

def load_network_from_file(filename):
    with open(filename, 'r') as f:
        data = json.load(f)
    
    routers = {ip: Router(ip) for ip in data.keys()}
    for ip, neighbors in data.items():
        for neighbor_ip, metric in neighbors.items():
            routers[ip].add_neighbor(neighbor_ip, metric)
    
    return routers

def save_network_to_file(routers, filename):
    network_data = {ip: router.to_dict()['neighbors'] for ip, router in routers.items()}
    with open(filename, 'w') as f:
        json.dump(network_data, f, indent=4)

def run_rip_protocol(routers, iterations=5):
    for i in range(iterations):
        print(f"Iteration {i + 1}")
        updates = {ip: router.get_routing_updates() for ip, router in routers.items()}
        for ip, router in routers.items():
            for neighbor_ip in router.neighbors.keys():
                router.update_routing_table(updates[neighbor_ip])
        print_intermediate_routing_tables(routers)
        print('\n\n')

def print_intermediate_routing_tables(routers):
    for ip, router in routers.items():
        print(f"Router {routers[ip].id:} {ip} routing table:")
        print("[ID] [Destination IP]    [Next Hop]       [Metric]")
        for dest_ip, (next_hop, metric) in router.routing_table.items():
            print(f"{routers[dest_ip].id:<4} {dest_ip:<18}  {next_hop:<15}  {metric}")
        print()

def print_routing_tables(routers):
    for ip, router in routers.items():
        print(f"Final state of router {routers[ip].id:} {ip} table:")
        print("[ID] [Destination IP]    [Next Hop]       [Metric]")
        for dest_ip, (next_hop, metric) in router.routing_table.items():
            print(f"{routers[dest_ip].id:<4} {dest_ip:<18}  {next_hop:<15}  {metric}")
        print()

if __name__ == "__main__":
    routers = generate_random_network(num_routers=3)
    
    # routers = load_network_from_file('network_output.json')
    save_network_to_file(routers, 'network_output.json')
    
    run_rip_protocol(routers)
    print_routing_tables(routers)
