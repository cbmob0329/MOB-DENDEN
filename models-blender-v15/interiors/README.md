# Blender interior assets — integration notes

These are editable Blender models, not a finished game build. Each room has its own `.blend`, `.glb`, flattened runtime `.json`, and a Cycles-rendered image. `build_interiors.py` recreates all four. Existing game furniture, characters, saves, and source files were not edited.

## Coordinates and ownership

Runtime coordinates are +Y up, +Z front. Origin is floor center. Blender uses +Z up / -Y front. JSON positions already include the conversion; do not rotate again.

| Asset | Floor width × depth | Purpose |
|---|---|---|
| home_shell | 11.5 × 9.3 | Plank floor, wall shell, moldings, structural columns/brackets, existing-position window and wall lights |
| cafe_shell | 10.8 × 8.4 | Wood shell and lighting; keep the game's shelf, counter, table and chairs |
| arcade_shell | 10.8 × 8.4 | Reference 010 checker floor, checker wall band, red trim, columns and warm lights; cabinets remain separate assets |
| bath_interior | 9 × 8.5 | Cedar bath room, hollow stone basin, washing stools/buckets/showers, entry curtain and supplied framed mural |

No front/right wall or ceiling obstructs the current isometric camera. Room shells intentionally show no runtime-owned furniture in Blender previews. This is not a claim that those empty previews are the complete furnished game.

Bath seating remains ±1.2 X / ±1.3 Z / Y 0.55. Water is Y 0.53, center Z -0.05. Basin outer limits approximately X ±2.65, Z -2.2…2.1. Entry anchor is (0,0,3.3). Washing equipment sits at X about -3.8, leaving the X ±3 paths available. Existing home window anchor stays (-2.3,2,-4.2).

## Semantic nodes

- `static`: room geometry and decorations.
- `lamps`: emissive glass / cornice lights. The loader should use the same night/day controls as existing room lights.
- `windows`: colored window pane, separate from frame; suitable for day/night color changes.
- `water`: single upward-facing bath water mesh. Replace the material with the game's water material if needed. No second solid water surface should remain.
- `waterfall`: separate spout stream.
- `entry_curtain`: indigo folded cloth, separable for camera visibility.

The JSON exporter preserves flat/weighted corner normals. Merge geometry only by both semantic node and material. Mural material alone contains a data URL texture with UV coordinates. Do not merge its UVs into a nontextured material. Colors are Blender **linear** base colors. Lamps use emission in the source blend; the runtime node identifies them for matching runtime emissive treatment.

## Reference decisions

All 001, 002, 003, 004, 010, 011, 012 and 013 were opened and viewed separately.

- 001: warm wooden floor, framed calm plaster, curved structural support. The decorative floor character emblem was omitted to retain the user’s layout and avoid an unrequested logo beneath furniture.
- 002/011: warm timber, wall lights and simple wood interior. No extra luxury equipment, chandelier, barrels or extra tables were added.
- 010: primary arcade interior guide. Checker floor/wall band, red border and warm cornice illumination are geometry. The 003 futuristic corridor is deliberately not mixed into that room.
- 012: cedar planks, rounded hollow rock-edged bath, stone floor, buckets with staves and bands, stools, shower fittings and lanterns. Bath dimensions follow the working game's seating contract, not the source sheet's different dimensions.
- 004: actual supplied image inside a modeled frame. Display is horizontal 4.2 × 1.6; UV crop selects the sky/hills/grassland band without stretching. This is the only image plane, explicitly a wall picture.
- 013: plain indigo split entrance curtain. The exterior building and shopkeeper belong to separate tasks.

Steam, surface motion, light changes and residents are runtime functions and are not baked into the models. Mobile performance and combined game screenshots must be checked by the integration task before these assets can be called complete in-game.
