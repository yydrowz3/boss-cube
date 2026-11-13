# BOSS Zhipin · 50 mm two-color cube

English | [简体中文](使用说明.md)

The model was successfully imported and inspected in Bambu Studio 2.8.2.61. This delivery covered model generation and import only; it was not sliced, and no print job was sent.

## Files

- `BOSS_cube_50mm.3mf`: the preferred file. A single object contains two separate parts, the cyan body and white lettering, with colors and relative positions preserved.
- `body_cyan.stl`: the 50 × 50 × 50 mm body.
- `lettering_white.stl`: the white raised lettering, with assembly coordinates preserved and its bottom at Z=50 mm. Do not import it as a separate object and let it drop to the build plate.
- `preview.png`: perspective and front-view previews.
- `geometry_validation.json`: dimension, watertightness, and orientation checks.
- `lettering_outline.json`: lettering outlines extracted from the original image, in millimeters.
- The complete package's `source` directory contains the generator and reference image.

## Open in Bambu Studio

1. Load `BOSS_cube_50mm.3mf`. This file stores the model but does not include a complete printer process configuration.
2. In the checked version, loading through **Open Project** displays a message stating that the 3MF configuration is invalid and only geometry will be loaded. Confirm to continue. This indicates that a complete print configuration is not embedded; the meshes have passed validation.
3. In the standard 3MF color import dialog, retain **2 colors**, check the cyan and white assignments, and confirm.
4. Expand the model in the **Objects** panel. It should contain `Cyan body` and `White BOSS lettering`. In the inspected session, they used project filaments **2 (cyan)** and **3 (white)**; the existing yellow filament 1 was not assigned to either part. Numbers may differ in a new session, so identify them by color.
5. If using the STL alternatives, select both files together, import them as multiple parts of one object, and preserve their original relative positions. STL files do not store colors.

## Dimensions and appearance

- Cube body: 50 × 50 × 50 mm, with square corners.
- White lettering: 40 mm wide, approximately 35.59 mm tall, with 0.8 mm relief. Overall height including lettering is 50.8 mm.
- The outlines were extracted directly from the supplied 148 × 148 pixel image and lightly smoothed, without selecting a different font or rearranging the text.
- The displayed cyan color is `#53CAC6`; the lettering is white.
- The lettered face points toward +Z, and the back is at Z=0. For display, the lettered face can be turned forward.

## Validation and later use

Checks completed: all meshes are watertight, have consistent winding and positive volume, and the lettering contacts the body at Z=50 mm. Bambu Studio displayed dimensions of 50 × 50 × 50.8 mm, correct lettering orientation and cyan/white colors, and two separately selectable parts. The lettering consists of 8 watertight connected components and retains 14 internal holes.

This delivery did not include slicing validation or a physical print test. It is ready for inspection and further editing. Before printing, choose the appropriate printer and filament profiles, then map cyan and white to the actual AMS slots. This model file is not tied to a printer or AMS slot.

## Regenerate

After extracting the complete package, run this command from its `source` directory:

```powershell
uv run build_model.py
```

The script declares its Python dependencies and writes the model, preview, and geometry report to a `BOSS_cube_50mm` directory beside the script. Keep `images.jpg` next to the script. If changing the geometry constants at the top, also update the corresponding dimension checks.

The 3MF compatibility check referenced Bambu Studio's [official open-source import implementation](https://github.com/bambulab/BambuStudio/blob/master/src/libslic3r/Format/bbs_3mf.cpp).
