# Blender town production

This is an actual Blender mesh production, not a background image or a set of runtime box proxies. `build_town.py` creates editable meshes, modifiers, material assignments, semantic collections and cameras. The source images are modeling references only; none are pasted over building facades.

## Deliverables

- `MOB_CHILL_TOWN.blend`: editable assembled source, with independent asset roots.
- `MOB_CHILL_TOWN.glb`: assembled game mesh export.
- `town_terrain.json`, `town_home.json`, `town_cafe.json`, `town_arcade.json`, `town_bath.json`, `town_farm.json`, `town_train.json`: local-coordinate meshes in the agreed Three.js contract.
- `manifest.json`: counts, coordinates, doorway anchors, six expansion plots, lighting nodes, reference interpretation and deviations.
- `town_overview.png`, `station_detail.png`, `station_front.png`, `bath_detail.png`, `town_*_detail.png`, `train_detail.png`: actual Blender renders of the delivered geometry.

## Modeling decisions

| Part | Actual production and reference use |
|---|---|
| Sharehouse | Newly modeled in Blender: plaster infill, wood structural frame, porch boards and curved brackets, rails, framed glazing, clay roof tiles. The warm wood/plaster palette comes from 001. There was no supplied exterior plan; its exterior is an interpretation. |
| Cafe | Newly modeled from 011: individual pink tiles, projecting sculpted cup sign, sloped striped awning, timber framed windows, chimney masonry, restrained planters and bench. Omits the crowded terrace, extra typography and very small ornamental trim. |
| Arcade | Newly modeled from 009: stepped parapet, side masonry courses, sloped striped awning, arched marquee and bulbs, raised mummy face with separate wrap seams, ears, eyes and gold spectacles, ventilator and entry. Posters and tiny text are omitted. |
| Bath exterior | Newly modeled from 013: tiled gable roof, timber structure, window frames, chimney courses, split indigo noren, porch canopy, rock-edged water basin and bench. The permitted name ネコクー温泉 is Japanese font lettering converted to real mesh. No shopkeeper, extra logo or duplicate bath interior. |
| Farm | Newly modeled small yard with nine timber beds, crops, fence with an entry gap, tool shed, corrugated roof, crates and barrel. This town exterior is separate from the working gameplay farm. |
| Terrain/station | Newly modeled following 017 and the text: continuous countryside with coast and rounded hills, joined footpaths, six vacant plots, rice plots, broadleaf trees, utility poles and sagging wires, raised one-sided platform, stairs with handrails, timber waiting shelter, bench and single railway. The obsolete prohibition on the five buildings/train was superseded by the latest user request. |
| Train | Newly modeled two-car rural train: rounded body and roof, door/window frames, waist stripe, roof pods, wheels, coupler and lamps. No passenger/boarding feature. |

## Integration

Coordinates are Three.js +Y up, +Z front. Each building JSON is local; place it at `manifest.facilityPositions`. Terrain is centered at 0. The train is local with its lowest wheel tread at Y=0 and travels along +X; its assembled world Y is **0.8975**, and railway center Z is **-13.6**. It must not be positioned at the older V14 train height.

Use the JSON doorway anchors or manifest entrances, rather than assuming every door is at X=0. Bath additionally exposes `chimneySteam`. Materials are linear Blender colors. `emissive_windows` and `emissive_lamps` nodes are separated so the existing runtime clock can control their emission. No imported camera or light is needed in the runtime.

The tile/structure parts are editable separately in Blender. The agreed runtime loader should merge static parts by node/material for fewer draws. The assembled source is intentionally more granular than the optimized runtime draw list.

After the Blender build, run `prune_runtime.py` and `validate_town.py` with Python. The first removes invisible zero-area pole/bevel triangles; the second records geometry checks and hashes. The optimized runtime contains 84,504 visible triangles across seven assets. This optimization does not change the rendered geometry.

## Visual review and limits

The first actual overview exposed black patches where independent road slabs overlapped at the same height. Those slabs were replaced with a non-overlapping road tessellation, and the corrected overview was reviewed. Stair elevations were corrected to meet the platform. Final inspection also covers roof seams, gable infill, awning slope and the Japanese bath sign.

These are game-sized cartoon interpretations of the illustrated instructions, not exact reconstructions of every decorative detail. The playable core remains about 34 × 29 units with 72 × 66 surrounding scenery instead of a literal 200 m simulation. No original `.blend`, user asset or game source was edited by this production task. The integrator still needs to judge runtime lighting, camera framing, touch labels and performance in the actual application; Blender renders alone do not establish those.
