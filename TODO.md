Game 7 — Project TODO

A classic roguelike built in Rust. Explore procedural dungeons, battle creatures, collect loot, and discover emergent stories through a hook system. Deterministic RNG for reproducible runs.

---

Table of contents

1. Project mission and goals
2. High-level design goals
3. Systems overview (spine)
4. Minimal viable prototype (MVP) scope
5. Development plan (phases and milestones)
6. Detailed tasks (by subsystem)
7. Data schema & content plan
8. Deterministic RNG strategy
9. Save/load and migration strategy
10. Testing and QA
11. Playtest plan & metrics
12. CI, release, and branch strategy
13. Marketing, community, and monetization ideas
14. Long-term roadmap
15. Appendix: content seeds, sample hooks, and example event flows

---

1. Project mission and goals

Game 7 is a classic turn-based roguelike focused on solid fundamentals and emergent storytelling through deterministic systems. Descend into procedural dungeons, fight monsters, collect loot, and watch your character develop through persistent traits and conditions.

Success criteria:
- Players can complete a full dungeon in 15–45 minutes depending on depth.
- Save files are compact and reproducible given a seed.
- The game produces memorable emergent moments through hook chains and deterministic interactions.
- Classic roguelike feel with modern quality-of-life improvements.

2. High-level design goals

Core principles
- **Deterministic + emergent**: Central RNG with seeded child streams ensures reproducibility while allowing emergent stories to emerge.
- **Classic roguelike feel**: Turn-based, grid-based movement, permadeath, procedural generation.
- **Terminal-first**: ASCII art and text-based UI for fast iteration; rich terminal rendering planned.
- **Meaningful failure**: Death should feel meaningful and feed into persistent progression systems.
- **Modular systems**: Combat, dungeon generation, items, and magic systems are independent modules.
- **Testable & debuggable**: Schema validation, deterministic tests, and comprehensive logging.

Design constraints  
- Built in Rust for performance and safety
- Prototype must be achievable solo in reasonable timeframe
- Content scope starts small but extensible
- Minimal external dependencies for core systems

3. Systems overview (spine)

Primary systems
- **Game Loop**: Turn-based main loop handling player input, monster AI, and world updates.
- **Central RNG**: Single world seed with deterministic derivation for all subsystems.
- **Entity System**: Players, monsters, items with component-based architecture and per-entity seeds.
- **Dungeon Generation**: Procedural level generation with rooms, corridors, and features.
- **Combat System**: Turn-based tactical combat with positioning and abilities.
- **Hook System**: Persistent traits, conditions, and modifiers that create emergent stories.
- **Item System**: Equipment, consumables, and artifacts with rich interactions.
- **Save/Load**: Schema versioning and deterministic state persistence.
- **Terminal UI**: Rich ASCII rendering with color, animations, and intuitive controls.

Support systems
- **Logging/Debug**: Detailed runtime logs of RNG draws, combat outcomes, and hook changes.
- **Data Validation**: JSON schema validation for all game data.
- **Content Pipeline**: Hot-reloading data files and schema validation tools.

4. Minimal viable prototype (MVP) scope

MVP must demonstrate the playable loop and deterministic behavior with a tiny content set.

Must-have features:
- Seeded startup and deterministic roster generation.
- Core loop: prep (choose 3 crew), exploration (move one tile, run one event), encounter resolution, return (apply resources/upgrades).
- Simple event system: 24 events (8 exploration, 8 encounter, 8 return) with scripted outcomes.
- Hook system: 80 compact hooks that can be added/removed and show on UI.
- Save/load: save world seed, entity seeds, and minimal state, with validation.
- Console UI: roster, single-tile map, event narration, notifications.
- Unit tests: RNG reproducibility, JSON parsing, event resolution.

Out-of-scope for MVP:
- Full SDL UI, full tactical combat, large content pools, heavy networking features.

5. Development plan (phases and milestones)

Phase 0 — Scaffold & prototype (this sprint)
- Create repository scaffold and minimal buildable prototype (this commit).
- Implement RNG, existing small main program that picks starters.
- Add TODO and schemas.

Phase 1 — Core systems and content (next 2–4 sprints)
- Core loop + event system + minimal encounter resolver.
- Hook system and entity model + save/load.
- Author content: 6 starters, 12 items, 6 tiles, 24 events, 6 upgrades, 80 hooks.
- Tests & 200-seed replay harness.

Phase 2 — Polish & UI (2–3 sprints)
- Console UI improvements, debug console, logging.
- Add SDL panel option (optional), data-driven map presentation.
- Replace encounter stub with richer tactical system (if time).

Phase 3 — Community, QA, and release
- Playtests, balancing, iterative content expansion.
- CI, automated release packaging, early access/beta.

6. Detailed tasks (by subsystem)

Core Loop
- Implement `CoreLoop` class with phases: Preparation, Exploration, Encounter, Return.
- Expose a `Tick()` method for testing.
- Emit lifecycle events for subsystems to subscribe to.

Central RNG
- Implement `RNG` class (done in scaffold) with: seed, Next(), NextInt, NextDouble, Derive(context).
- Add deterministic subseed derivation rules and document them.
- Ensure thread-safety if/when we go multithreaded.

Entity model
- Define `Entity` struct: id, seed, name, role, hp, endurance, hooks[], inventory[], implants[].
- Implement JSON serialization and validate against schema.
- Implement `EntityFactory` that uses the world seed + entity id to derive entity seeds for reproducible regeneration.

Hook system
- Define `Hook` object: id, display, tooltip, type, modifiers, lifetime, priority, flags.
- Implement hook add/remove/transform logic and priority/conflict resolution.
- Expose hook inspector in debug logs.

Event system
- Design `Event` JSON format: id, type, preconditions, rng_subseed, outcomes, text_template.
- Implement event parser and executor with outcome types: add_hook, remove_hook, change_stat, add_item, spawn_encounter.
- Implement outcome templating engine for text interpolation.

Encounter resolver
- Implement deterministic encounter bundles (damage bundles, simple choice outcomes).
- For combat stub: creatures have HP, endurance; attacks use deterministic rolls from derived RNGs.
- Record combat log to hook into narrative events.

Save & Load
- Save structure: {schema_version, world_seed, time, entities: [compact], global_state}
- Implement validation: schema check, checksum, schema_version migration hooks.
- Implement safe-load fallback (backup auto-save, reject corrupt file and offer continue from seed).

Console UI
- Roster panel: list names, roles, HP, 1–3 visible hooks (badge), brief morale indicator.
- Map panel: show one tile with tile type and short description.
- Event pane: show event narration and choices.
- Notification ticker: displays recent logs and event outcomes.

Data & Content
- Create `data/` folder; author JSON files for starters, items, tiles, events.
- Maintain a `content_version` string and schema_version for migration.

Testing
- Unit tests for RNG, event resolution, save/load, hook caps, and invariants.
- Integration test harness: run 200 seeds and ensure no crashes and invariants hold.

CI
- GitHub Actions: build, run unit tests, run 200-seed smoke test (can be gated to PRs to save CI cost).

7. Data schema & content plan

Schemas to author (place in `data/schemas/`):
- character.schema.json
- item.schema.json
- tile.schema.json
- event.schema.json
- hook.schema.json
- save.schema.json

Content minimal examples (MVP):
- 6 starters with defined seeds and 1 signature hook each.
- 12 items (rations, medkit, flare, switchblade, wrench, tool roll, battery pack, grease rag, pocket terminal, coin pouch, snare, whistle).
- 6 tiles: road, ruin, swamp, trading_post, radiation_patch, ambush_clear.
- 24 events split across phases (exploration/encounter/return).
- 6 settlement upgrades.
- 80 compact hooks (tag, display, tooltip, effects).

8. Deterministic RNG strategy

Principles
- Single global `world_seed` provided at run start.
- All RNG calls derive from the central RNG via `Derive("subsystem:name")` to produce independent child streams.
- Subsystems must not call std::random_device or ad-hoc RNGs.
- Per-entity persistent `entity_seed` = Hash(world_seed, entity_id) used for deterministic regeneration.
- Every event uses a derived RNG with a documented context and optional `rng_subseed` field from content to allow manual variance.

Derivation rules
- Use a stable hash mixing function for seeds. Document it and ensure cross-platform consistency.
- Avoid floating point exactness assumptions when using RNG; use integer-based thresholds where possible.

9. Save/load and migration strategy

Save structure
- `schema_version`: integer
- `world_seed`: integer
- `timestamp` and `play_time`
- `entities`: compact list serialized with their minimal mutable state
- `global_state`: levels, upgrades, message_log

Migration
- Keep a migration table: when schema_version increments, provide a migration function for each change.
- Provide `save_migrate(old_json)` entrypoints to transform old saves.

Safety
- Keep autosaves and a `last_known_good` snapshot; on load error, offer to restore from snapshot.

10. Testing and QA

Unit tests
- RNG determinism: same seed -> same sequence
- Schema validation: invalid files are rejected
- Event resolution: deterministic outcomes for given seed + inputs
- Hook invariants: no more than X modifiers, priority resolution

Integration tests
- 200-seed replay harness that runs the full loop and asserts invariants.
- Fuzz harness: randomized event sequences to stress hooks and transformations.

Manual QA
- Create playtest checklist (see section 11).

11. Playtest plan & metrics

Metrics to log during playtests
- Average run time
- Average hooks per run
- Event types frequency
- Failure rate (run-ending events) and mean time to run failure or success
- Item scarcity metrics

Playtest process
- Internal playtest 10 runs with designer notes.
- Remote playtests with recorded seeds and short survey.
- Use telemetry (optional) or local log export.

12. CI, release, and branch strategy

Branches
- `main` — stable prototype releases
- `dev` — day-to-day work
- feature branches: `feature/<name>`

CI
- On PR: build + unit tests
- Nightly: run 200-seed harness and report failures

Releases
- Tag semantic versions and attach release notes with major content changes acknowledged.

13. Community and release ideas

Community
- Seed challenges: weekly seeds with injected modifiers.
- Shareable run pages: players post seed + run summary.

Release
- Launch as open source or paid indie game when ready.

14. Long-term roadmap

Year 1 goals
- Stable CLI release with full features and 200+ hooks
- SDL UI option and richer tactical combat
- Expand content pools and hook systems

Year 2 goals
- Feature DLCs, mod tools, community hooks, potential multiplayer-asynchronous leaderboards

15. Appendix: content seeds, sample hooks, and example event flows

(Authoring appendix with sample hooks and events to be expanded)

---

Developer notes
- Keep everything in source-control. Commit early. Use branches.
- Keep the content files tiny and schema-validated.
- When adding RNG draws to a new system, document the Derive("system:context") string used.

This TODO can and will be expanded. It can be used as the master checklist and slowly converted into project management tasks in your tracker of choice.
