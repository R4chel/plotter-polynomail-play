import vsketch
import vpype as vp
import numpy as np
from numpy.polynomial import Polynomial
from shapely.geometry import Point, LineString, Polygon
from shapely.ops import clip_by_rect

class PlotterPolynomialPlaySketch(vsketch.SketchClass):
    # Sketch parameters:
    # radius = vsketch.Param(2.0)
    numRoots = vsketch.Param(3)

    def draw(self, vsk: vsketch.Vsketch) -> None:
        vsk.size("a6", landscape=True)
        scale = "mm"
        vsk.scale(scale)
        factor = 1 / vp.convert_length(scale)
        self.width, self.height = factor * vsk.width, factor * vsk.height
        # make the (0,0) the center of canvas 
        x_min, x_max = -self.width/2, self.width/2
        y_min, y_max = -self.height/2, self.height/2 

        region = Polygon([ (x_min, y_min), (x_max, y_min), (x_max,y_max),(x_min,y_max) ])

        vsk.translate(self.width/2,self.height/2)

        vsk.line(-self.width/2, 0,self.width/2, 0)
        window = [-self.width/2, self.width/2]
        roots = [round(vsk.random(x_min, x_max),3) for _ in range(self.numRoots)]
        for root in roots:
            vsk.circle(root,0, 5)
        f = Polynomial.fromroots(roots, window, window)
        print(roots,f)
        f.convert()
        (xs, ys) = f.linspace()
        pts = LineString(list(zip(xs, ys)))
        pts = pts.intersection(region)
        vsk.geometry(pts)
        

        # implement your sketch here
        # vsk.circle(0, 0, self.radius, mode="radius")

    def finalize(self, vsk: vsketch.Vsketch) -> None:
        vsk.vpype("linemerge linesimplify reloop linesort")


if __name__ == "__main__":
    PlotterPolynomialPlaySketch.display()
