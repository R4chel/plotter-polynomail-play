import vsketch
import vpype as vp
import numpy as np
from numpy.polynomial import Polynomial
from shapely.geometry import Point, LineString


class PlotterPolynomialPlaySketch(vsketch.SketchClass):
    # Sketch parameters:
    # radius = vsketch.Param(2.0)
    numRoots = vsketch.Param(3)

    def connect_points(self, vsk: vsketch.Vsketch, points):
        if len(points) < 2:
            return 
        p0 = points[0]
        for p in points[1:]:
            vsk.line(p0[0], p0[1], p[0],p[1])
            p0 = p

    def draw(self, vsk: vsketch.Vsketch) -> None:
        vsk.size("a6", landscape=True)
        scale = "mm"
        vsk.scale(scale)
        factor = 1 / vp.convert_length(scale)
        self.width, self.height = factor * vsk.width, factor * vsk.height
        # make the (0,0) the center of canvas 
        x_min, x_max = -self.width/2, self.width/2
        y_min, y_max = -self.height/2, self.height/2
        
        x_min = self.width/2
        vsk.translate(self.width/2,self.height/2)

        vsk.line(-self.width/2, 0,self.width/2, 0)
        domain = [-1, 1]
        window = [-self.width/2, self.width/2]
        roots = [round(vsk.random(window[0], window[1]),3) for _ in range(self.numRoots)]
        for root in roots:
            vsk.circle(root,0, 5)
        f = Polynomial.fromroots(roots, window, window)
        print(roots,f)
        f.convert()
        (xs, ys) = f.linspace()
        # pts = LineString(list(zip(xs, ys)))
        
        pts = list(zip(xs,ys))
        
        self.connect_points(vsk, pts)

        # implement your sketch here
        # vsk.circle(0, 0, self.radius, mode="radius")

    def finalize(self, vsk: vsketch.Vsketch) -> None:
        vsk.vpype("linemerge linesimplify reloop linesort")


if __name__ == "__main__":
    PlotterPolynomialPlaySketch.display()
