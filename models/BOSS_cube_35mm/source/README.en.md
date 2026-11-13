# Using the source

English | [简体中文](README.md)

`build_model.py` extracts the original lettering outlines from the adjacent `images.jpg` and regenerates a generic color 3MF, two STL files, outline data, geometry validation results, and a preview.

Install Python 3.11 or later and uv, then run this command from this directory:

```sh
uv run build_model.py
```

The script declares its dependencies in its header, and uv creates the runtime environment. Output is written to a new `BOSS_cube_35mm` subdirectory here, without overwriting the delivered Bambu project.

The dimension constants are `SIDE=35.0`, `LOGO_WIDTH=28.0`, and `RELIEF=0.8`, in millimeters. The lettering comes directly from the reference image; no substitute font is used.

The generator output is not tied to a printer model. The P2S process settings are saved in `../BOSS_cube_35mm_P2S_04.3mf`. The adjacent `verified_process_settings.json` lists the checked settings, which can be reproduced in Studio using the [main usage guide](../USAGE.en.md). Confirm the physical AMS slots after connecting the printer.
