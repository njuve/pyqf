# pyqf

pyqf is a sql formatter by python.

# Installation

```py
poetry add git+https://github.com/njuve/pyqf
```

# Usage

```py
from pyqf import format
>>> print(format("select a, b from t"))
SELECT
    a,
    b
FROM
    t
```
