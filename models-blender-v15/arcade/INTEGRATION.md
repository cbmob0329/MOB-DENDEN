# Arcade Blender assets — review before integration

All assets are authored as real Blender meshes with bevels, molded outlines, curves converted on export, shells and explicit structural components. No instruction image is used as a plane. `build_arcade.py` rebuilds `.blend`, `.glb`, runtime `.json`, measured manifest and Blender renders. Original repo and reference images are read-only.

The canonical rebuild is `blender --background --disable-autoexec --python build_arcade.py` (append `-- --no-render` for exports only). `render_details.py` adds close-up views. `validate_assets.py` validates runtime contracts. `finalize_roof.py` and `fix_ufo_controls.py` are one-time production patch history; their changes are already incorporated in the canonical build script, so do not run those patches on a fresh rebuild. `.blend1` and build logs are working history, not deliverables. The delivered `.blend` initially shows the UFO collection; toggle the other named collections to inspect each model at local origin.

## Coordinates and semantic nodes

JSON uses Three coordinates: X right, Y up, Z toward viewer. Object transforms are baked into geometry. Nodes use world-local positions within each asset; construct animation groups around the named anchor by subtracting the pivot from vertices or translating child mesh groups inversely. Do not rotate around mesh origin without pivot correction.

- `gacha`: `knob`, `hatch`, `glass`, `static`; knob rotates around Z axis; hatch swings around X at `hatchPivot`. Material `green` is the replaceable cabinet accent for a cyan second cabinet. Capsule colors are currently shared materials, so changing *all* green also recolors green stored capsules; clone/remap only desired named parts if needed. `capsuleOutlet` is the animation start.
- `capsule`: independent `capsule_top` and `capsule_bottom`; split around `splitCenter`. No prize image is baked inside. Insert actual awarded keychain at `prizeCenter`.
- `ufo`: `static`, `roof`, `glass`, `carriage`, `cable`, `claw`, `finger_0..2`. The crown and MOB header are `roof`: show them in the room and hide/fade them in the dedicated play view so they cannot hide the claw. The steel rail and motor are `carriage`; black cable is separate. Fingers have individual `fingerPivot_N` and `fingerTip_N`. `gripCenter` is the useful central gap near finger tips; `gripPoint` is the original modeled head-to-tip reference (not a physics success target). Match existing physics, not these artistic anchors, to determine catch success. The game must move all finger nodes along with the claw head.
- UFO floor top is **Y=1.05**. Actual floor opening includes X[-1.40,-1.025], Z[.625,1.05], with chute center(-1.225,1.05,.90), matching existing play-to-world conversion X/Z×.5, Y×.5+1.05. The lower shell is open behind the prize mouth. Chute exit is a different lower exterior point.
- `race`: `screen_left/right` have replaceable material and UVs, `wheel_left/right` rotate around a tilted axis approximately (0,.45,.9). Seat anchors are seat surfaces, not standing feet. The runtime must supply actual screen textures; blank dark screens in Blender preview are intentional.
- `race_course`: road center X radius2.76, Z radius1.2, surfaceY=.12, width.62. Curbs/paint are slightly raised. Preserve existing movement centerline. `startLine` at(0,.12,1.2). Spectators are small original black cat silhouettes with gold glasses and colored bodies, not substituted residents.
- `kart`: +Z forward; `driverSeat` anchor. Recolor `cyan` for player/cart lanes. Tires are `wheels`; front/rear are named anchors.

## Appearance vs references

005: adopted cat-ear silhouette, rounded color trims, transparent capsule chamber, real two-piece stored capsules, twist knob, buttons and hinged prize door. Omitted all non-MOB wording and cat stamps as explicitly requested.

006: real hemispherical upper/lower shells, seam, and opening animation separation. Prize/keychain is supplied dynamically by the game.

007: adopted yellow/black body, transparent display chamber, rails, motor, cable, three hooked metal/yellow fingers, joystick, grab button, service slots and actual chute aperture. Footprint widened about 13–15% to preserve existing physics hole without clipping a wall. Header does not reproduce the large illustrated mascot faces. Plush inventory is supplied by existing game assets.

008: adopted joined two-player unit, green/blue bucket seats, contoured backrests, harness openings, steering columns/wheels, pedals, colored screen bezels, raised checkers and MOB header. Mascot illustrations and large sculpted character-head header ornaments are not recreated. Back surfaces are simpler service shells. The extra course/kart translate the illustrated cartoon-racing style into actual low-poly scenery while retaining existing game route coordinates.

These are inspection candidates, not a declaration that all reference detail or game integration is finished. The parent must inspect live game scale, glass sorting, textures, claw travel, prize opening, seat occupancy and buttons before accepting them.
