import vsketch
import vpype as vp
import numpy as np
from numpy.polynomial import Polynomial
from shapely.geometry import Point, LineString, Polygon
from shapely.ops import clip_by_rect
import math

fns = {
    "zero": (lambda x: x - x),
    "noop": (lambda x: x),
    "sin": np.sin,
    "cos": np.cos,
    "sqrt": np.sqrt,
    "sqr": (lambda x: x**2),
    "third": (lambda x: x**3)
}


class PlotterPolynomialPlaySketch(vsketch.SketchClass):
    # Sketch parameters:
    debug = vsketch.Param(False)
    numRoots = vsketch.Param(3)
    numLines = vsketch.Param(10)
    num_pts = vsketch.Param(1000)
    precision = vsketch.Param(3)
    y_offset = vsketch.Param(0.3, decimals=2)
    y_delta = vsketch.Param(0.01, decimals=6)
    max_delta = vsketch.Param(0.1)
    z_fn = vsketch.Param("noop", choices=fns.keys())
    after_noise = vsketch.Param("sqr", choices=fns.keys())
    mode = vsketch.Param("linear", choices=vsketch.EASING_FUNCTIONS.keys())
    draw_first_line = vsketch.Param(False)
    layer_count = vsketch.Param(1)

    def draw(self, vsk: vsketch.Vsketch) -> None:
        vsk.size("4inx6in", landscape=True, center=False)
        scale = "mm"
        vsk.scale(scale)
        factor = 1 / vp.convert_length(scale)
        width, height = factor * vsk.width, factor * vsk.height

        # make the (0,0) the center of canvas
        vsk.translate(width / 2, height / 2)

        #make x-range [-1,1]
        vsk.scale(width / 2, width / 2)
        x_min = -1
        x_max = 1
        y_min = -height / width
        y_max = height / width
        width = 2
        height = 2 * height / width

        self.region = Polygon([(x_min, y_min), (x_max, y_min), (x_max, y_max),
                               (x_min, y_max)])
        if self.debug:
            vsk.geometry(self.region)

        domain = [x_min, x_max]
        window = [x_min, x_max]
        roots = [
            round(vsk.random(domain[0], domain[1]), self.precision)
            for _ in range(self.numRoots)
        ]
        f = Polynomial.fromroots(roots)
        if self.debug:
            vsk.line(0, 0, 0, y_max)
            vsk.line(0, 0, x_max, 0)
            for root in roots:
                vsk.circle(root, 0, .05)

        (xs, ys) = f.linspace(self.num_pts)
        if self.draw_first_line:
            ys_to_draw = ys + self.y_offset
            pts = LineString(list(zip(xs, ys_to_draw)))
            pts = pts.intersection(self.region)
            vsk.geometry(pts)

        layers = range(1, self.layer_count + 1)
        for i in range(1, self.numLines + 1):
            # zs = np.full(len(xs), i)
            zs = [i + fns[self.z_fn](j) for j in range(len(xs))]
            noise = vsk.noise(xs, ys, zs, grid_mode=False)
            noise = fns[self.after_noise](noise)
            # scaled_noise = list(
            #     map(
            #         lambda x: vsk.map(x, 0, 1, -self.max_delta, self.max_delta
            #                           ), noise))

            scaled_noise = vsk.easing(
                noise,
                mode=self.mode,
                start1=0,
                stop1=1,
                start2=0,
                stop2=self.max_delta,
            )
            ys = np.add(ys, scaled_noise)
            ys_to_draw = ys + self.y_delta * i + self.y_offset
            pts = LineString(list(zip(xs, ys_to_draw)))
            pts = pts.intersection(self.region)
            vsk.stroke(layers[i % len(layers)])
            vsk.geometry(pts)

    def finalize(self, vsk: vsketch.Vsketch) -> None:
        vsk.vpype("linemerge linesimplify reloop linesort")


if __name__ == "__main__":
    PlotterPolynomialPlaySketch.display()
