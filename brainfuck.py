class Brainfuck:
    def __init__(self, program, input="", size=50000):
        if not program:
            raise ValueError("Sem programa para interpretar.")
        self.program = program
        self.input = input
        self.size = size
        self.array = [0] * size
        self.p = 0
        self.i = 0
        self.done = False
        self.events = {}
        self.loops = {}
        
    def mod(self, a, b):
        b += 1
        return ((a % b) + b) % b

    def on(self, name, fn):
        if name not in self.events:
            self.events[name] = []
        self.events[name].append(fn)

    def emit(self, name, *args):
        if name not in self.events:
            return
        for event_fn in self.events[name]:
            event_fn(*args)

    def step(self):
        program = self.program
        invalid = False

        if self.done or self.i >= len(program):
            if not self.done:
                self.emit("done")
            self.done = True
            return

        instruction = program[self.i]

        if instruction == ">":
            self.p += 1
            self.p = self.mod(self.p, self.size)
        elif instruction == "<":
            self.p -= 1
            self.p = self.mod(self.p, self.size)
        elif instruction == "+":
            self.array[self.p] = (self.array[self.p] + 1) & 255
        elif instruction == "-":
            self.array[self.p] = (self.array[self.p] - 1) & 255
        elif instruction == ".":
            if self.array[self.p] != 0:
                self.emit("out", chr(self.array[self.p]))
        elif instruction == ",":
            self.emit("in")
            if self.i >= len(self.input):
                self.array[self.p] = 0
            else:
                self.array[self.p] = ord(self.input[self.i])
                self.i += 1
        elif instruction == "[":
            temp_i = self.i
            ignore = 0

            while True:
                temp_i += 1
                if temp_i >= len(program):
                    raise ValueError("Fora dos limites.")
                if program[temp_i] == "[":
                    ignore += 1
                if program[temp_i] == "]":
                    if ignore == 0:
                        if self.array[self.p] == 0:
                            self.i = temp_i
                        else:
                            self.loops[temp_i] = self.i
                        break
                    else:
                        ignore -= 1
        elif instruction == "]":
            if self.array[self.p] != 0:
                self.i = self.loops[self.i]
            else:
                self.loops[self.i]

        else:
            invalid = True

        if not invalid:
            self.emit("tick")
        self.i += 1

    def init(self, speed=1000):
        def fn():
            for _ in range(speed):
                self.step()
            if not self.done:
                fn()
        fn()

def main():
    program = "++++++++++[>+>+++>+++++++>++++++++++<<<<-]>>>>+++++++++.------------.+++.+.<<++.>>---.+++++++++++++++++++++++.<<.>------.>----------------.+++++.++++++.---------------.++++.+++++++++.---.++++.<<.>>----.-.<<.>>-------.++.+++++++++++.------------.+++++++++++++.-------------------."
    bf = Brainfuck(program)
    out = ""

    def on_out(o):
        nonlocal out
        out += o

    def on_done():
        print(out)

    bf.on("out", on_out)
    bf.on("done", on_done)
    bf.init()

if __name__ == "__main__":
    main()
