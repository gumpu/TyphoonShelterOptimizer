"""TODO
"""

class Plot( object ):
    def __init__( self, file ):
        self.screen_x = 400
        self.screen_y = 400
        self.file     = file
        file.write("""<?xml version="1.0" encoding="UTF-8" standalone="no"?>
<svg xmlns="http://www.w3.org/2000/svg" version="1.1" width="{}" height="{}">)
""".format( self.screen_x, self.screen_y ))

    def set_domain(self, domain):
        self.xmin = domain[0]
        self.xmax = domain[1]
        self.ymin = domain[2]
        self.ymax = domain[3]

        # Add margin
        dx = self.xmax - self.xmin
        dy = self.ymax - self.ymin
        self.xmin -= 0.05*dx
        self.xmax += 0.05*dx
        self.ymin -= 0.05*dy
        self.ymax += 0.05*dy


    def scalex(self, x):
        return self.screen_x * (x-self.xmin)/(self.xmax-self.xmin)

    def scaley(self, y):
        return self.screen_y * (y-self.ymin)/(self.ymax-self.ymin)

    def line(self, x1, y1, x2, y2, color="green"):
        self.file.write("""print '<line x1="{}" y1="{}" x2="{}" y2="{}" 
stroke-width="1" stroke="{}"/>""".format(
            self.scalex(x1), self.scaley(y1), 
            self.scalex(x2), self.scaley(y2), color))

    def dot(self, x, y, r=4):
        self.file.write("""<circle cx="{}" cy="{}" r="{}"
fill="#ff0000" stroke="#000000" stroke-width="2"/>""".format(
                self.scalex(x), self.scaley(y), r))

    def box(self, x, y, r=4):
        self.file.write(
"""<rect x="{}" y="{}" width="{}" height="{}" fill="#00ff00" stroke="#000000" stroke-width="2"/>
""".format( self.scalex(x)-0.5*r, self.scaley(y)-0.5*r, r, r))

    def rectangle(self, x,y, h, w):
        pass

    def label(self, x, y, text):
        self.file.write("""<text x="{}" y="{}">{}</text>""".format( 
                self.scalex(x)-15, self.scaley(y)+5, text))

    def close(self):
        self.file.write("</svg>\n")

