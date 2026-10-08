# MOB CHILL LIFE V17 local delivery — 2026-10-08

Canonical repo: C:/Users/CB-Me/Documents/GitHub/MOB-DENDEN. No commit, push, staging, old-PC access or other-repo edits. Existing save key mob-chill-life-v2 remains unchanged.

## Requested character correction
Tetsu's entire 16-frame atlas now has no mouth, tongue, mouth bubble or baked-in dorayaki/other food. Runtime eating uses empty-handed pose 14 plus the existing shared food renderer (dorayaki, omelet or soup). Nekokoo retains his own face. The transparent PNG and embedded JS data URI match. Source references were user-supplied 016.png / 014.png. These NPCs use 16 poses each, front/three-quarter billboards with two-step walking, not full directional animation. The separate original Nyoro/Irukaeru 27-action/108-frame set was preserved.

## Daily routine and dialogue
routine-dialogue.js contains six characters × eleven contexts × two lines = 132 editable lines. Breakfast 07–09, lunch 12–14, snack 15–17, dinner 18–20, bath 20–22, rest 22–06 use the existing 20-minute game day. Start times stagger by actor. Background pause and independent offline cooking are retained; missed meal windows do not trigger closed-game catch-up.
Nekokoo uses オラ / だぞ; Tetsu 拙者 / お主 / でござる; Pink 僕 / であります; Denden ～でやんす / ほぅ～; Nyoro ニョロ; Irukaeru polite natural speech. Original meal greetings remain, except new NPC-specific greetings.
Active jobs, service, modal interaction, travel and furniture editing defer routine starts. Meals use existing cooked inventory and café stock only. Queued guests can miss a meal if seats remain busy; their transferred dishes stay in café stock. No food is generated. Per-day/window records, meal spacing and daily cap prevent autonomous overeating. Explicit user meal actions may override spacing. Stock reservations retain the existing ledger. A consumed staff meal is reconciled after interrupted saves. Nekokoo uses a persisted inventory escrow and returns only unconsumed food after reload.
One existing bed can be reserved; other residents rest seated. Morning releases rest locks. Tetsu has no bath immersion frames and meditates instead; Nekokoo watches the bath as proprietor. No substitute bath poses were invented.

## Verification
Build succeeded. Existing three damaged-source PNG warnings remain: pink/dj_a, pink/dj_b and denden meal sheet; build reuses their valid embedded versions without modifying source originals.
New automated Edge checks passed: empty-food morning, inventory conservation, meal spacing, all six time windows, next-day eligibility, active work preservation, single-bed reservation, six residents resting/waking, persisted meal records/egg 42, no offline clock catch-up, paused clock, consumption rollback on save failure, consumed/unconsumed owner escrow, staff consumed-save reconciliation, Nekokoo meal voice, no browser errors. The final corrected atlas was visually inspected.
Earlier V16 evidence remains in verification-v16 and V16_TOWN_NPC_REPORT.md: widths 320/390/430, heart collection and mobile speech, town pan/pinch/raycast, 20 front-door routes, café seating/serving and reload, furniture select/move/rotate/store/confirm, three recipes and double-collection prevention. These are prior checks, not claimed to be a new exhaustive V17 run. Actual iPhone Safari is unverified.

## Green heart rectangle diagnosis
The heart was an HTML button. Global button:hover overrode .heart-drop and painted #e3e9dd (reproduced rgb(227,233,221)). Explicit transparent button.heart-drop hover/active/focus styling fixes the rectangle; the drop animation and inventory transaction were retained.

## Delivery
MOB_CHILL_LIFE_V15_1.zip keeps the requested established filename; its HTML is V17. It contains current standalone HTML, runtime reference sources, retained Blender source/assets, and verification reports. Runtime-reference is supporting source, not a complete independently buildable repository. Existing unrelated/wrongly named archives are excluded. Library upload remains unavailable; this delivery is local only.
