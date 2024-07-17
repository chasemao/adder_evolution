import argparse
from adder_evolution.world import world

desc = '''Adder evolution is an approach to generate adder with evolutionary algorithms.

It provides two modes, "run world" or "draw adder".

1) Use --run_world to run a world and within it there will be adders evolving.
    Use -o to decide the output path for saving world, it default output to "save" directory in project.
    Use -i to resume world from world saving file.
    The priority of config is: input > file > default.

2) Alternatively, use --draw_adder to draw a adder from a world save file, you can see clearly how adder organize its gates inside it.
    Use -i to decide which world saving file to use.
    Use --index to decide which adder to draw.
    Use -o to decide the output path for drawing adder file.'''

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=desc, formatter_class=argparse.RawTextHelpFormatter)
    parser.add_argument('--run_world', action='store_true', help='Run a world to adders.')
    parser.add_argument('-d', '--digits', type=int, help='The input digits of adder, must gt 0, default 2.')
    parser.add_argument('-b', '--birth_rate', type=float, help='The base birth rate of adder, must gt 1, deafult 2.')
    parser.add_argument('-m', '--mutation_rate', type=float, help='The base mutation rate of adder, must gt 0 and lt 1, default 0.9.')
    parser.add_argument('-max', '--max_number', type=int, help='The max number of adder existed. When number of adder excced it, adders which have disadvantage in addition task will be eliminated, must gt 0, default 10000.')
    parser.add_argument('-s', '--save_interval', type=float, help='The save interval of world in generation, le 0 means no save, default 1.')
    parser.add_argument('-r', '--run_generation', type=int, help='How many generation will the world run, deafult endless.')
    
    parser.add_argument('--draw_adder', action='store_true', help='Draw adder from save file of world')
    parser.add_argument('--index', type=int, default=0, help='The index of adder in world to draw.')
    
    parser.add_argument('-i', '--input_path', type=str, default="", help='The input path of saving world. Resume world or draw adder from it.')
    parser.add_argument('-o', '--output_path', type=str, default="", help='The output path of saving world.')

    # Parse the arguments
    args = parser.parse_args()
    inp = args.input_path
    out = args.output_path
    # Run world mode
    if args.run_world:
        digits = args.digits
        max_number = args.max_number
        birth_rate = args.birth_rate
        mutation_rate = args.mutation_rate
        save_interval = args.save_interval
        run_generation = args.run_generation
        if not inp or inp == "":
            digits = 2 if digits is None else digits
            max_number = 10000 if max_number is None else max_number
            birth_rate = 2 if birth_rate is None else birth_rate
            mutation_rate = 0.9 if mutation_rate is None else mutation_rate
            save_interval = 1 if save_interval is None else save_interval
            run_generation = 0 if run_generation is None else run_generation
        w = world(digits, max_number, birth_rate, mutation_rate, save_interval, inp, out, run_generation).run()
    # Draw adder mode
    elif args.draw_adder:
        if inp == "":
            raise ValueError("invalid input path")
        try:
            adders = world(input_path=inp).get_adders()
        except:
            raise SystemError("parse world from input path failed")
        index = args.index
        if index < 0 or index >= len(adders):
            raise ValueError("invalid index")
        adders[index].draw(out)
    else:
        print(parser.description)