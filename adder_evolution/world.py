from typing import List, Tuple
import json
import math
import random
from adder_evolution.gate import gate
from adder_evolution.adder import adder

class world:
    generation_field_name = "generation"
    digits_field_name = "digits"
    max_adders_field_name = "max_adders"
    birth_rate_field_name = "birth_rate"
    involute_rate_field_name = "involute_rate"
    adders_field_name = "adders"
    
    def __init__(self, digits: int, max_adders: int, birth_rate: float, invloute_rate: float, save_file: str = ""):
        generation = 0
        adders = [adder(digits,[],[])]
        if save_file != "":
            with open(save_file, 'r') as file:
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

    def give_birth(self, index: int, total: int) -> int:
        bonus = 1 - index / total
        bonus = bonus * bonus
        rate = self.birth_rate + bonus
        base = math.floor(rate)
        base_rate = base + 1 - rate
        return random.choices([base, base + 1], [base_rate, 1 - base_rate])[0]
    
    def run(self):
        while True:
            # Give birth and involute
            total = len(self.adders)
            for i in range(total):
                childs = self.give_birth(i, total)
                for _ in range(childs):
                    self.adders.append(self.adders[i].involute(self.involute_rate))
                    
            # Some die
            challenge_results = []
            for one_adder in self.adders:
                one_adder.challenge(self.challanges)
            self.adders = sorted(self.adders, key=lambda x: x.get_score(), reverse=True)
            if len(self.adders) > self.max_adders:
                self.adders = self.adders[:self.max_adders]
                challenge_results = challenge_results[:self.max_adders]
            
            # save to file
            self.generation += 1
            data = {
                self.generation_field_name: self.generation,
                self.digits_field_name: self.digits,
                self.max_adders_field_name: self.max_adders,self.birth_rate_field_name: self.birth_rate,
                self.involute_rate_field_name: self.involute_rate,
                "adder_len": len(self.adders),
                self.adders_field_name: [],                
            }
            for one_adder in self.adders:
                data[self.adders_field_name].append(one_adder.packJSON())
            file_path = 'save/' + str(self.generation) + ".json"
            # Write JSON data to the file
            with open(file_path, 'w') as json_file:
                json.dump(data, json_file, indent=4)
            print("Finish generation=",self.generation)