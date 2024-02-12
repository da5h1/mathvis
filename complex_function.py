from manim import *
import numpy as np
import cmath

def f(a):
    return cmath.exp(a)**0.5

class ComplexFunction(Scene):
    def construct(self):
        dots = []
        lines = []
        for x in np.linspace(-7,8,15):
            for y in np.linspace(-4,5,15):
                dots.append(Dot(np.array([x,y,0])))
        gradient = color_gradient((RED, BLUE), len(dots))
        for i,dot in enumerate(dots):
            dot.set_color(gradient[i])
            self.add(dot)
            number = complex(dot.get_x(), dot.get_y())
            new_number = f(number)
            new_number_c = np.array([new_number.real, new_number.imag, 0])
            lines.append(Line(dot.get_center(), new_number_c))
        
        arr = [MoveAlongPath(dots[i], lines[i]) for i in range(len(dots))]
        self.play(*arr, rate_func=there_and_back, run_time=6)