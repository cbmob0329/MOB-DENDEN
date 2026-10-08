# MOB CHILL LIFE V18 — NPC motions and BGM

Canonical C:/Users/CB-Me/Documents/GitHub/MOB-DENDEN. Work started at 82b6a3a. Another operation created 6861c77 during this task; this agent did not commit, stage or push. The final runtime delta after that commit is MOB_CHILL_LIFE.html, npc-motion-v18.js, bgm-v18.js. No other project was edited. The BATTLE material folder was only read for the explicitly authorized BGM source.

## NPC motion completion
Official ImageGen created articulated pose atlases referencing the supplied characters and accepted V16 designs. These are separate hand/leg/eye/body drawings, not animation invented by moving a single still. Runtime processing isolates each actual alpha-connected character rectangle, then uses one scale per motion group and a common bottom anchor on 256px transparent canvases. No automatic left/right mirroring. Source atlas: 1774x887, 32 cells per character. A fixed uniform grid was rejected after detecting neighboring tail fragments; measured per-sprite rectangles now include complete tails and exclude neighboring sprites.

| State | Tetsu | Nekokoo | Live assignment |
|---|---:|---:|---|
| Front/back/left/right walking | 2 each (8) | 2 each (8) | Paths in rooms and town; camera-relative direction; distance-based gait |
| Meal | 5 | 5 | Take/lift/bite/chew/finish; existing single food prop |
| Seated waiting | 3 | 3 | Café seating; proprietor's idle seated rest |
| Bath | 4 | 3 | Existing bath queue and waterline; actual immersion, no meditation substitute |
| Joy | 4 | 4 | Satisfied after café/owner meal |
| Idle | 2 | 2 | Standing/proprietor waiting |
| Greeting | 2 | 2 | Interaction and standing conversation; stationary train reaction |
| Sleep | 2 | 2 | Seated night rest; Tetsu's prior two wide-sleep poses also retained |
| Quiet | 2 | 2 | Tetsu meditation / Nekokoo proprietor bow |

Tetsu uses all 32 new cells. Nekokoo uses 31; bath cell 18 is intentionally excluded because a folded towel was not clearly drawn. His bath uses three valid towel frames. Tetsu remains mouthless in every new pose; neither character has food drawn into the atlas. Nekokoo's face follows the supplied mouthless original. Dialogue identities remain Tetsu 拙者/お主/でござる and Nekokoo オラ/だぞ.

Tetsu is now 80% of the former billboard size (1.65→1.32 indoors, 1.25→1.00 town), with food anchors using that same sprite scale. Direct comparison with the existing residents confirms a smaller character. Side-walk passing poses were redrawn to lift a knee and plant the other foot; gait advances per 0.18 world distance, not a global clock tick. No claim of high-frame-count smooth animation: walking remains two drawings per direction.

Seated hands: waiting has three actual hand/arm poses; seated speech no longer selects a standing greeting. Both new residents now use the existing upright contact-depth shader with ordinary depth testing retained. Close-up views at three camera angles confirm visible hands. Food attaches to the authored hand/body frames with no extra hand spheres. Soup close-up shows one food prop between the hands. A 5-frame food action uses the existing timing; the long chew portion is a held pose, not five continuously cycling frames.

Bath allocation was changed from actor-indexed to four actual slots so six residents can share them. Full baths defer entry. Save restoration rebuilds unique slots and queues overflow. Nekokoo returns to his bath station; Tetsu returns home. Pending atlas loads defer the routine rather than silently replacing bathing with meditation.

## BGM completion
Latest BGM.txt mapping: 013.mp3 morning/day, 014.mp3 night, 015.mp3 game center. Exact MP3 bytes copied to assets/audio/chill-day.mp3, chill-night.mp3, chill-arcade.mp3; original MP3, WAV and Japanese source names untouched. SHA256 provenance in assets/audio/manifest.json. Build embeds only these MP3s into the standalone HTML; no additional facility-specific songs invented.
Day 05:00–18:59 and night 19:00–04:59 match the existing game light/time logic. Viewed game center overrides the day/night track; leaving it selects the current clock's track. Single audio element: 0.4s fade-out before switching, 0.6s fade-in; no overlapping players. A user gesture unlocks audio. Pause, document hidden and freeze stop audio; resume keeps the current track position unless the scene/time requires a different song. BGM settings under 操作 → BGM設定 provide mute and volume, saved separately under mob-chill-audio-v1. Existing beeps are labeled 効果音 separately.

## Validation and limits
Build succeeded; three pre-existing damaged-source PNG warnings retain valid embedded backups (pink/dj_a, pink/dj_b, denden meal). New tests: all four directional selections; 32 isolated runtime canvases each with safe canvas margins; five meal body frames and single food owner; joy assignment; both NPC bath round-trips; full bath refusal; reload with unique slots and egg 42 preserved; six-resident restored queue visiting four slots and all exiting; distance-based gait invariant; seated depth and 80% scale; real MP3 playback with expected durations 148.56/162.76/101.08s; gesture unlock; scene/time track priority; pause/resume and freeze/resume; mute/volume persistence; BGM settings at 320/390/430px. Browser page errors: none in the tested flows.
Actual iPhone Safari and audible listening on physical speakers were not tested. Edge decoded and advanced all three real audio files. Previous unrelated gameplay checks were not broadly rerun; prior reports remain in the repository. Final ZIP keeps the established MOB_CHILL_LIFE_V15_1.zip filename but contains V18. Library upload is not available; no upload retried.
