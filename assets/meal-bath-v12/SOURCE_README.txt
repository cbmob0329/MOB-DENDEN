CHILL LIFE — MEAL + BATH SPRITES / V12

CONTENTS
- 36 individual RGBA transparent PNG frames, each exactly 256 x 256
- 8 horizontal sprite sheets: meal 1280 x 256, bath 1024 x 256
- 2 contact PNGs and 2 animated GIFs under previews/
- manifest.json with every frame, anchor, duration, runtime food phase and towel emblem
- qa_report.json with dimension, transparency, unique-frame and packing checks
- generation_prompts.json with the final prompt set

FRAMES
Each character: meal = take, handlift, bite, chew, finish.
Each character: bath = relax_01, blink, relax_02, smile.
Characters: denden, pink, nyoro, irukaeru.

ENGINE INTEGRATION
Use nearest texture filtering; disable mipmaps. Never horizontally mirror these sprites.
Meal frames are fully seated. There is no baked food, dish, utensil, chair or table.
The engine owns the food. Use the actual handAnchorPx AND mouthAnchorPx on each frame.
IMPORTANT: the old generic mouth anchor [131,125] is not aligned with these seated heads.
Actual mouth anchors are approximately y163–179; consult the per-frame manifest.
Suggested food visibility: take after contact, handlift held, bite until consumption,
then hidden during chew and finish. Timing may be adjusted to gameplay.
For Nyoro the food offset [10,-8] moves the prop inward/upward from the gripping paw.
Meal duration defaults: 650,750,550,650,900 ms. Take once; repeat lift/bite/chew as
needed; finish once. Do not blindly loop all five frames during a single bite.

Seat anchors: Denden[113,218], Pink[122,215], Nyoro[128,218], Irukaeru[128,218].
Bath waterline anchor: [128,204]. Render opaque game water over pixels at/below the
waterline. The 8px shoulder overlap below it is intentional. No bathwater is baked in.
Bath duration: 420ms per frame, 4-frame loop.

IDENTITY AND TOWELS
All 8 supplied PNG references were inspected and used as imagegen inputs.
Meal clothing, glasses, species features, palettes and asymmetry are retained.
Bath hoods/hats/helmet are off; natural cat ears, dragon horns and dolphin fin stay.
Pink remains mouthless. Bath expressions are small; there are no exaggerated mouths.
Original approved towel emblems: Denden pink paw; Pink pink hood-inspired curl;
Nyoro orange branching crack; Irukaeru teal dolphin-fin curve.
These are newly created identity-based marks, not supplied existing logos.

METHOD AND LIMITATIONS
Built-in imagegen produced exactly 8 outputs, one sheet per character/action.
Code only cropped, uniformly resized with nearest-neighbor, translated and packed
generated RGBA pixels. No character features or animation poses were drawn in code.
All 36 exported frames are distinct; there are no duplicated frame PNGs.
Generated redraws can have small shape/detail changes across frames. Denden and Pink
change active hand between some poses; use actual per-frame anchors. Bodies and
asymmetrical outfits were not mirrored. Exact new poses are not original pixel copies.
Previews have neutral backgrounds for visibility; engine PNGs remain transparent.

HELD-FOOD PATHS
manifest meal.heldFoodTransitions provides start/control/end pixel paths for
a single food object. Interpolate through these paths when switching animation
frames. Denden and Pink change the active hand; never teleport or duplicate food.
Each frame also includes heldFoodAnchorPx (prop center including any grip offset).
The first acquisition starts at the actual runtime table-food position.
