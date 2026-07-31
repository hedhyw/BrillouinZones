# BrillouinZones

Python programs that construct and draw Brillouin zones of crystal lattices,
written for a condensed matter physics course. Two independent drawers:

* `2d Brillouin Zone/` — draws the first N Brillouin zones of a 2D lattice
  as a PNG (Pillow + sympy). It builds the lattice points, constructs Bragg
  plane lines (perpendicular bisectors of reciprocal lattice vectors),
  intersects them with sympy, then flood-fills zones outward from the center.
* `3d Brillouin Zone/` — draws the first Brillouin zone of a 3D reciprocal
  lattice as a matplotlib 3D plot. It uses its own exact-arithmetic geometry
  library (`geometry.py`, `Decimal`-based) to intersect Bragg planes and
  collect the polyhedron faces.

## Layout

```
2d Brillouin Zone/
  index.py                 # entry point; draws zones to a PNG
  crystal.py               # abstract Crystal base, shell grouping
  primitive_crystal.py     # square lattice
  hex_crystal.py           # hexagonal lattice
  parallelogram_crystal.py # trigonal lattice
3d Brillouin Zone/
  index.py                 # entry point; interactive or CLI lattice choice
  geometry.py              # Point3D/Vector3D/Plane/Line3D/Segment3D + intersections
  reciprocal_lattice.py    # abstract lattice, reciprocal vectors, shell grouping
  *_reciprocal_lattice.py  # primitive, body-/face-/base-centered, HCP lattices
tests/                     # pytest suite for the pure-computation modules
Examples/                  # sample output images referenced by the README
```

The source directories contain spaces in their names; `tests/conftest.py`
adds both to `sys.path` so the modules can be imported by tests.

## How to run

```sh
pip3 install -r requirements.txt

# 2D: writes brillouin_zone.png to the working directory (~70 s at 12 zones).
python3 "./2d Brillouin Zone/index.py"

# 3D: interactive lattice menu, or pass the number 1..5 as an argument:
# 1 body-centered, 2 face-centered, 3 primitive, 4 HCP, 5 base-centered.
python3 "./3d Brillouin Zone/index.py" 3
```

Environment variables: `BRILLOUIN_OUTPUT` (output path), `BRILLOUIN_ZONES`
(2D zone count, default 12; 4 is much faster), `BRILLOUIN_NO_SHOW=1` (2D:
skip the image viewer). With `MPLBACKEND=Agg` (or any non-interactive
backend) the 3D drawer saves the figure to a file instead of showing it;
the 2D drawer skips the viewer automatically when no display is available.

## Tests and CI

```sh
pip3 install -r requirements-dev.txt
pytest tests
```

The tests cover the pure-computation parts: 2D lattice shell construction
(coordination numbers, symmetry, determinism), the 3D geometry primitives
(dot/cross products, plane/line/segment intersections, distances) and the
reciprocal lattices (orthogonality and magnitude of reciprocal vectors,
cubic/BCC/FCC coordination shells).

CI (`.github/workflows/check.yml`) compiles all sources, runs pytest, then
runs both drawers headless with `MPLBACKEND=Agg` (the 2D one with
`BRILLOUIN_ZONES=4` for speed) and asserts that the output PNGs are
non-empty. All GitHub Actions are pinned to commit SHAs.

## Conventions

* Python 3.10+; two-space indentation (historic style of this codebase).
* Conventional commit messages (`fix:`, `ci:`, `docs:`, ...).
* Dependencies live in `requirements.txt` (runtime) and
  `requirements-dev.txt` (adds pytest); Dependabot updates pip and
  GitHub Actions monthly.
