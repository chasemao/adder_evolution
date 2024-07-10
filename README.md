# adder_evolution
An approach to generate adder with evolutionary algorithms. 

* It define a adder consist of some gates, and a world consist of one default adder. 
* Each time world run, adders in world will give birth to new adders, and new adders will involute and become bit of different from old ones. The birth rate is controled by the performance in which adder will answer add questions, the more it answer corrently, the more birth rate. 
* If number of adders hit the limit, world will get rid of bad performance ones.

## Demo

The main.py is a demo world. The input of question is 2 bits (11, 10, 01, 00), so number of questions is `4 * 4 = 16`.

When I run demo world, in 107 generation, I got a adder crack all 16 questions.

You can run the demo world like below.

```sh
# Install dependancy
pip install -r requirements.txt

# Run main.py
python main.py
```

It will show information of each generation like below and save detail into save/*.

```sh
Finish generation: 1 max advantage: 2.0 min advantage: 1.0
Finish generation: 2 max advantage: 4.0 min advantage: 1.0
Finish generation: 3 max advantage: 4.0 min advantage: 0.0
Finish generation: 4 max advantage: 4.0 min advantage: 0.0
Finish generation: 5 max advantage: 4.0 min advantage: 0.0
```
