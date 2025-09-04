# How to Install

To use the *"Pycube Projection"* project, you must have Python installed
on your computer and follow these steps:

1.  Clone the repository to a folder of your choice. Use the command:

`git clone https://github.com/JoaoLucasMBC/pycube-projection.git`

2.  Using the terminal / the IDE of your choice, create a Python
    *Virtual Env* and activate it:

- Using venv:

        python -m venv <ENVIRONMENT-NAME>

        <ENVIRONMENT-NAME>/Scripts/Activate.ps1 (Windows)

        source <ENVIRONMENT-NAME>/bin/activate (Linux and MacOS)

- Using uv:

        uv venv <ENVIRONMENT-NAME> --python 3.13

        <ENVIRONMENT-NAME>/Scripts/activate (Windows)

        source <ENVIRONMENT-NAME>/bin/activate (Linux and MacOS)

3.  Move into the *"Pycube Projection"* folder and install the required
    libraries:

`cd ./pycube-projection`

`pip install -r requirements.txt (venv)`

`uv pip install -r requirements.txt (uv)`

4.  After installation, run the *main.py* file through the terminal to
    start the project:

`python src/main.py (Windows)`

`python3 src/main.py (Linux and MacOS)`

------------------------------------------------------------------------

# How to Manipulate the Cube

The cube can be manipulated using a few commands: \* `Q` and `T` --
These two keys toggle the automatic rotation mode: the cube spins around
all its axes indefinitely (with an increment of 1 degree per loop). `Q`
activates rotation mode, and `T` stops it. While the cube is in rotation
mode, only the `Mouse Scroll` command can be used simultaneously. To
manually manipulate the cube, stop the rotation mode. \*
`W, A, S, D, Z, X` -- These commands perform manual cube rotations. `W`
and `S` rotate around the $x$ axis, `A` and `D` around the $y$ axis, and
`Z` and `X` around the $z$ axis. \* `Mouse Scroll` -- The mouse scroll
changes the cube's focal distance `d`, zooming in or out. Scrolling up
increases `d` ("zoom in"), and scrolling down decreases `d` ("zoom
out"). (On an external mouse and a laptop touchpad scroll, the
directions are inverted)

*Note: since the rotation keys only increment the rotation matrix angle,
it is important to keep in mind that, for example, if the user rotates
the cube 180° on the x axis, the rotation on the y axis will have
inverted controls. In other words, pay attention when combining
rotations, as they change the directions the axes point to.*

## Other Pages

- [Project Description](../README.md)
- [Contribuiting to the Project](CONTRIBUTING_.md) (or [portuguese version](CONTRIBUTING-PTBR.md))
- [Mathematical Model](MATHEMATICAL-MODEL.md) (or [portuguese version](MATHEMATICAL-MODEL-PTBR.md))