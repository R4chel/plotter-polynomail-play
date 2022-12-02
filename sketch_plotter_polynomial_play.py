import vsketch
import vpype as vp
import numpy as np
from numpy.polynomial import Polynomial
from shapely.geometry import Point, LineString, Polygon
from shapely.ops import clip_by_rect

class PlotterPolynomialPlaySketch(vsketch.SketchClass):
    # Sketch parameters:
    numRoots = vsketch.Param(3)
    numLines = vsketch.Param(10)
    max_delta = vsketch.Param(0.1)
    precision = vsketch.Param(3)
    debug = vsketch.Param(False)

    def draw_polynomial(self, vsk:vsketch.Vsketch, f):
        (xs, ys) = f.linspace(1000)
        pts = LineString(list(zip(xs, ys)))
        pts = pts.intersection(self.region)
        vsk.geometry(pts)
        
    def draw(self, vsk: vsketch.Vsketch) -> None:
        vsk.size("a6", landscape=True)
        scale = "mm"
        vsk.scale(scale)
        factor = 1 / vp.convert_length(scale)
        width, height = factor * vsk.width, factor * vsk.height
        
        # make the (0,0) the center of canvas 
        vsk.translate(width/2,height/2)

        #make x-range [-1,1]
        vsk.scale(width/2, width/2)
        x_min = 1 
        x_max = -1
        y_min = -height/width
        y_max = height/width 
        width = 2
        height = 2 * height/width 

        self.region = Polygon([ (x_min, y_min), (x_max, y_min), (x_max,y_max),(x_min,y_max) ])
        if self.debug:
            vsk.geometry(region)

        domain = [x_min, x_max]
        window = [x_min, x_max]
        roots = [round(vsk.random(domain[0], domain[1]),self.precision) for _ in range(self.numRoots)]
        if self.debug:
            vsk.line(x_min, 0,x_max, 0)
            for root in roots:
                vsk.circle(root,0, .05)
        
        f = Polynomial.fromroots(roots)
        self.draw_polynomial(vsk, f)
        (xs, ys) = f.linspace(1000)
        for i in range(self.numLines-1):
            noise = vsk.noise(xs,ys, grid_mode=False)
            scaled_noise = list(map(lambda x: vsk.map(x,0,1,-self.max_delta, self.max_delta), noise))
            ys = np.add(ys,scaled_noise)
            pts = LineString(list(zip(xs, ys)))
            pts = pts.intersection(self.region)
            vsk.geometry(pts)
            

    def finalize(self, vsk: vsketch.Vsketch) -> None:
        vsk.vpype("linemerge linesimplify reloop linesort")


if __name__ == "__main__":
    PlotterPolynomialPlaySketch.display()
