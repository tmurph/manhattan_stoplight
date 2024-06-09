# Manhattan Stoplight

When walking around a city, the practical commute time between two points is
closer to [manhattan distance](https://en.wikipedia.org/wiki/Taxicab_geometry)
than euclidean distance. But when I'm walking around an urban environment, I
also spend a significant amount of time waiting for stoplights. If my
destination is due west, directly down the street, I must wait for each red
light I come to. But if I am walking the same number of blocks northwest, I can
opportunistically move either north or west, depending on which way the green
light is oriented, until I come to one of my cross streets, then I have to walk
straight down the road again. This means that with stoplights, it's more
efficient to move diagonally than in straight lines (relative to Manhattan
distance).

Say that the city is on a regular grid, and at each intersection I encounter,
the traffic light has a 50/50 chance of being green for north/south or
east/west. It takes me 1 unit of time to walk one block, but waiting at an
intersection for the light to change takes an average of w units of time (w is
a nonnegative real-valued parameter of the formula, w=0 equals traditional
manhattan distance). Let's define *stoplight manhattan distance* as the expected
commute time between two points given w.

Euclidan distance is sqrt(x^2 + y^2). Manhattan distance is |x| + |y|. *What's
the formula for stoplight manhattan distance?*
