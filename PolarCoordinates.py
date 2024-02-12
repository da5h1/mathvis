from manim import *
import numpy as np
import random

class PolarCoordinates(Scene):
    def construct(self):
        time = ValueTracker(0)
        
        n = 15
        speed = 0.5
        diff = 15
        
        def get_line(x1,y1,x2,y2,color):
            return Line(x1*2*RIGHT+y1*2*UP, x2*2*RIGHT+y2*2*UP, color=color)
        
        c = [2*random.random() for _ in range(8)]
        
        def updater(mob, i):
            r1 = np.cos(c[4]*time.get_value()+i/diff)
            phi1 = 2*PI*np.sin(c[5]*time.get_value()+i/diff)
            r2 = np.cos(c[6]*time.get_value()+i/diff)
            phi2 = 2*PI*np.sin(c[7]*time.get_value()+i/diff)
            x1 = r1*np.cos(phi1)
            y1 = r1*np.sin(phi1)
            x2 = r2*np.cos(phi2)
            y2 = r2*np.sin(phi2)
            return mob.become(get_line(x1,y1,x2,y2,mob.get_color()))
        
        gradient = color_gradient((RED, BLUE), n)
        lines = [updater(Line(color=gradient[i]),i) for i in range(n)]
        
        for i in range(n):
            lines[i].add_updater(lambda mob,i=i: updater(mob,i))
            
        self.add(time)  
        self.add(*lines)
        self.play(time.animate.set_value(6), rate_func=lambda t: speed * there_and_back(t,2), run_time=18)