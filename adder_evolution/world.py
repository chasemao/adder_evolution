from typing import List
import os
import json
import math
import random
import time
from adder_evolution.adder import adder, connect

class world:
    generation_field_name = "generation"
    digits_field_name = "digits"
    max_adders_field_name = "max_adders"
    birth_rate_field_name = "birth_rate"
    involute_rate_field_name = "involute_rate"
    adders_field_name = "adders"
    
    def __init__(self, digits: int, max_adders: int, birth_rate: float, invloute_rate: float, save_interval: int, save_file: str = ""):
        generation = 0
        output_connections = []
        for _ in range(digits+1):
            output_connections.append(connect(connect.type_none, 0))
        adders = [adder([],[],output_connections)]
        if save_file != "":
            current_dir = os.path.dirname(os.path.abspath(__file__))
            f = os.path.join(current_dir, save_file)
            with open(f, 'r') as file:
                data = json.load(file)
            generation = data[self.generation_field_name]
            digits = data[self.digits_field_name]
            max_adders = data[self.max_adders_field_name]
            birth_rate = data[self.birth_rate_field_name]
            invloute_rate = data[self.involute_rate_field_name]
            adders = []
            for adder_data in data[self.adders_field_name]:
                adders.append(adder.unpackJSON(adder_data))
        
        self.generation = generation
        self.digits = digits
        self.max_adders = max_adders
        self.birth_rate = birth_rate
        self.involute_rate = invloute_rate
        self.adders = adders
        self.challanges = self.genChallages()
        self.save_interval = save_interval
        self.save_index = 0
        
    # generate challage for adder, for exapmle [[1,1,2], [2,2,4], [1,2,3]]
    def genChallages(self) -> List[List[int]]: 
        res = []
        num_str = "1" * self.digits
        num = int(num_str, 2)
        for i in range(num+1):
            for j in range(num+1):
                o = i + j
                res.append([i,j,o])
        return res

    def give_birth(self, advantage: int) -> int:
        rate = self.birth_rate + 0.2 * float(advantage)
        base = math.floor(rate)
        base_rate = base + 1 - rate
        return random.choices([base, base + 1], [base_rate, 1 - base_rate])[0]
    
    def advantage(self, one: adder) -> float:
        sc =  one.get_score()
        if sc == 2 ** (2 * self.digits):
            sc -= 0.01 * one.count_gates()
        return sc

    def run(self):
        random.seed(time.time())
        while True:
            # Give birth and involute
            for i in range(len(self.adders)):
                one_adder = self.adders[i]
                adv = self.advantage(one_adder)
                childs = self.give_birth(adv)
                for _ in range(childs):
                    self.adders.append(one_adder.involute(self.involute_rate))
                    
            # Some die
            for one_adder in self.adders:
                one_adder.challenge(self.challanges)
            self.adders = sorted(self.adders,
                                 key=lambda x: (self.advantage(x), x.get_generation()), reverse=True)
            if len(self.adders) > self.max_adders:
                self.adders = self.adders[:self.max_adders]
            
            # Print log
            self.generation += 1
            print("Finish generation:",self.generation, 
                  "max advantage:", self.advantage(self.adders[0]),
                  "min advantage:", self.advantage(self.adders[-1]))
            
            # Save to file
            if self.save_interval <= 0:
                continue
            self.save_index += 1
            if self.save_index < self.save_interval:
                continue
            self.save_index = 0
            data = {
                self.generation_field_name: self.generation,
                self.digits_field_name: self.digits,
                self.max_adders_field_name: self.max_adders,
                self.birth_rate_field_name: self.birth_rate,
                self.involute_rate_field_name: self.involute_rate,
                "adder_len": len(self.adders),
                self.adders_field_name: [],                
            }
            for one_adder in self.adders:
                data[self.adders_field_name].append(one_adder.packJSON())
            current_dir = os.path.dirname(os.path.abspath(__file__))
            directory = os.path.join(current_dir, '../save')
            os.makedirs(directory, exist_ok=True)
            file_path = os.path.join(directory, str(self.generation) + ".json")
            with open(file_path, 'w') as json_file:
                json.dump(data, json_file, indent=4)