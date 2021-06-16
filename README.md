Wellcome to join and be a programmer-charter!

+ `note.py` defines the classes used throughout the project. Each statement in aff, including both hit objects and control statements, is considered as a `note`. The structure of these notes doesn't strictly follow the aff format, but should rather comform to intuition or convenience in pratice. The classes that needs attention the most are `arc`, `collection` and `snake`.
+ `aff.py` handles aff files, including parsing and serializing, loading and saving. Of course, things follow exactly Arcaea's format here.
+ `gen.py` provides a bunch of handy tools and generators that help to compose your chart.
+ `coordinate.py` is used for coordinates calculations, such as addition and subtraction of positions, traslational and rotational motion, and the relationship among chart positions, judge points, camera spots and where they display on screen.

## The most important utils

Here are the most important, most general, and perhaps most used functions in `gen.py`. Using these instead of creating arcs one by one improves efficiency by greatly reducing data redundance you have to type.

+ `equidistant`: Equidistant points.
+ `taps`: Write tuples for taps.
+ `put_arctaps`: Create arctaps with ease.
+ `swing`: A snake composed of arcs of equal duration.
+ `batch_snakes`: A batch of snakes with same numbers of arcs.

There are other functions generating circles, diamonds and various other shaped snakes, see `gen.py` for details. I'm also planning to include a tool that converts a picture to black line art automatically.
