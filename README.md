# BrillouinZones
Programs for constructing Brillouin zones in three- and two-dimensional space. It was written to create images of Brillouin zones for the course of condensed matter physics.

#### How to use?
1. Install dependencies (Python 3.10+):
```sh
pip3 install -r requirements.txt
```
2. Run the drawers:
```sh
# First Brillouin zone in three-dimensional space
# (prompts for a lattice: body-centered, face-centered, primitive,
# hexagonal close-packed or base-centered).
python3 "./3d Brillouin Zone/index.py"

# Non-interactive: pass the lattice number (1..5) as an argument.
python3 "./3d Brillouin Zone/index.py" 3

# First several Brillouin zones in two-dimensional space.
python3 "./2d Brillouin Zone/index.py"
```

Configuration via environment variables:
* `BRILLOUIN_OUTPUT` — output image path (default `brillouin_zone.png` for 2D, `brillouin_zone_3d.png` for 3D);
* `BRILLOUIN_ZONES` — number of zones to highlight in the 2D drawer (default `12`);
* `BRILLOUIN_NO_SHOW=1` — do not open an image viewer after the 2D drawer finishes;
* `MPLBACKEND=Agg` — render the 3D figure to a file instead of opening a window (headless mode).

To edit the 2D lattice type (primitive, hexagonal or parallelogram), change the crystal initialization in `2d Brillouin Zone/index.py`.

#### Development
```sh
pip3 install -r requirements-dev.txt
pytest tests
```

#### Examples

![FirstZoneForBaseCenteredLattice](https://raw.githubusercontent.com/hedhyw/BrillouinZones/master/Examples/base_centered.png "Base Centered lattice")

![FirstZoneForFaceCenteredLattice](https://raw.githubusercontent.com/hedhyw/BrillouinZones/master/Examples/face_centered.png "Face Centered Lattice")

![SeveralZonesForTheSquareLattice](https://raw.githubusercontent.com/hedhyw/BrillouinZones/master/Examples/square.png "Square lattice")
