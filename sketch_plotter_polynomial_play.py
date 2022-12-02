import vsketch
import vpype as vp
import numpy as np
from numpy.polynomial import Polynomial
from shapely.geometry import Point, LineString, Polygon
from shapely.ops import clip_by_rect

class PlotterPolynomialPlaySketch(vsketch.SketchClass):
    # Sketch parameters:
    numRoots = vsketch.Param(3)
    debug = vsketch.Param(False)

    def draw(self, vsk: vsketch.Vsketch) -> None:
        vsk.size("a6", landscape=True)
        scale = "mm"
        vsk.scale(scale)
        factor = 1 / vp.convert_length(scale)
        width, height = factor * vsk.width, factor * vsk.height
        
        # make the (0,0) the center of canvas 
        vsk.translate(width/2,height/2)

        #make x range [-1,1]
        vsk.scale(width/2, width/2)
        x_min = 1 
        x_max = -1
        y_min = -height/width
        y_max = height/width 
        width = 2
        height = 2 * height/width 

        region = Polygon([ (x_min, y_min), (x_max, y_min), (x_max,y_max),(x_min,y_max) ])
        if self.debug:
            vsk.geometry(region)

        domain = [x_min, x_max]
        window = [x_min, x_max]
        roots = [round(vsk.random(domain[0], domain[1]),3) for _ in range(self.numRoots)]
        if self.debug:
            vsk.line(x_min, 0,x_max, 0)
            for root in roots:
                vsk.circle(root,0, .05)
        f = Polynomial.fromroots(roots, window, window)
        print(roots,f)
        # f.convert()
        (xs, ys) = f.linspace(1000, window)
        pts = LineString(list(zip(xs, ys)))
        pts = pts.intersection(region)
        vsk.geometry(pts)
        

        # implement your sketch here
        # vsk.circle(0, 0, self.radius, mode="radius")

    def finalize(self, vsk: vsketch.Vsketch) -> None:
        vsk.vpype("linemerge linesimplify reloop linesort")


if __name__ == "__main__":
    PlotterPolynomialPlaySketch.display()
