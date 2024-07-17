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
    mutation_rate_field_name = "mutation_rate"
    adders_field_name = "adders"
    save_interval_field_name = "save_interval"
    
    # If set input_path, will read from file and fetch config, others arg will override config in input file
    def __init__(self, digits: int = None, max_adders: int = None, birth_rate: float = None, mutation_rate: float = None,
                 save_interval: int = None, input_path: str = None, output_path: str = None, run_generation: int = 0):
        generation = 0
        adders = [adder([],[],[])]
        if input_path and input_path != "":
            print(f"Resuming from {input_path}...")
            with open(input_path, 'r') as file:
                data = json.load(file)
            generation = data[self.generation_field_name]
            if digits is None:
                digits = data[self.digits_field_name]
            if max_adders is None:
                max_adders = data[self.max_adders_field_name]
            if birth_rate is None:
                birth_rate = data[self.birth_rate_field_name]
            if mutation_rate is None:
                mutation_rate = data[self.mutation_rate_field_name]
            if save_interval is None:
                save_interval = data[self.save_interval_field_name]
            adders = []
            for adder_data in data[self.adders_field_name]:
                adders.append(adder.unpackJSON(adder_data))
        
        self.generation = generation
        if digits is None or digits <= 0:
            raise ValueError("invalid digits")
        self.digits = digits
        if max_adders is None or max_adders <= 0:
            raise ValueError("invalid max_adders")
        self.max_adders = max_adders
        if birth_rate is None or birth_rate < 1:
            raise ValueError("invalid birth_rate")
        self.birth_rate = birth_rate
        if mutation_rate is None or ( mutation_rate <= 0 or mutation_rate >= 1):
            raise ValueError("invalid mutation_rate")
        self.mutation_rate = mutation_rate
        if save_interval is None:
            raise ValueError("invalid save_interval")
        self.save_interval = save_interval
        for one_adder in adders:
            one_adder.ensure_digits(digits)
        self.adders = adders
        self.challanges = self.genChallages()
        self.save_index = 0
        if output_path and output_path != "":
            self.output_path = output_path
        else:
            current_dir = os.path.dirname(os.path.abspath(__file__))
            self.output_path = os.path.join(current_dir, '../save')
        os.makedirs(self.output_path, exist_ok=True)
        if run_generation is None:
            run_generation = 0
        self.run_generation = run_generation
        
    def get_adders(self) -> List[adder]:
        return self.adders
        
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
        if self.run_generation > 0:
            while self.run_generation:
                self.run_generation -= 1
                self.round()
        else:
            while True:
                self.round()
        print("world run finish")

    def round(self):
        # Give birth and mutate
        for i in range(len(self.adders)):
            one_adder = self.adders[i]
            adv = self.advantage(one_adder)
            childs = self.give_birth(adv)
            for _ in range(childs):
                self.adders.append(one_adder.mutate(self.mutation_rate))
                
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
            return
        self.save_index += 1
        if self.save_index < self.save_interval:
            return
        self.save_index = 0
        data = {
            self.generation_field_name: self.generation,
            self.digits_field_name: self.digits,
            self.max_adders_field_name: self.max_adders,
            self.birth_rate_field_name: self.birth_rate,
            self.mutation_rate_field_name: self.mutation_rate,
            self.save_interval_field_name: self.save_interval,
            "adder_len": len(self.adders),
            self.adders_field_name: [],                
        }
        for one_adder in self.adders:
            data[self.adders_field_name].append(one_adder.packJSON())
        file_path = os.path.join(self.output_path, str(self.generation) + ".json")
        with open(file_path, 'w') as json_file:
            json.dump(data, json_file, indent=4)