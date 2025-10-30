# Game 7

A classic roguelike built in Rust with deterministic systems for emergent storytelling.

## Goals

- Classic turn-based roguelike with modern quality-of-life improvements
- Deterministic RNG for reproducible runs and shareable seeds
- Hook system for emergent character development and storytelling
- Terminal-first UI with rich ASCII rendering
- Modular, testable architecture

## Building

Project is being converted from C++ to Rust. Build instructions will be updated when Rust implementation begins.

## Features (Planned)

- Procedural dungeon generation
- Turn-based tactical combat
- Equipment and inventory systems
- Persistent traits and conditions (hooks)
- Save/load with schema versioning
- Deterministic replay from seeds

## Next Steps

- Set up Rust project structure with Cargo
- Implement core systems: RNG, entity system, game loop
- Build terminal UI with crossterm/ratatui
- Add content system with JSON schemas

License: MIT (see `LICENSE`)