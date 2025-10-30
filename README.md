# Roguelike Game

A classic ASCII-based roguelike dungeon crawler game built in Python. Explore procedurally generated dungeons, fight enemies, and survive!

## Features

- **Procedurally Generated Dungeons**: Each game creates a unique dungeon layout with rooms and corridors
- **Turn-Based Combat**: Strategic gameplay where every move counts
- **Enemy AI**: Enemies track and pursue the player
- **ASCII Graphics**: Classic retro-style display
- **Score System**: Track your performance as you defeat enemies
- **Permadeath**: When you die, the game is over - true roguelike experience!

## Game Elements

- `@` - Player (You!)
- `g` - Goblin (HP: 10, Attack: 3)
- `O` - Orc (HP: 15, Attack: 4)
- `#` - Wall (impassable)
- `.` - Floor (walkable)

## How to Play

### Installation

No external dependencies required! Just Python 3.6+

```bash
python3 roguelike.py
```

### Controls

- `W` - Move up
- `A` - Move left
- `S` - Move down
- `D` - Move right
- `Q` - Quit game

### Gameplay

1. You start in the first room of a randomly generated dungeon
2. Enemies are scattered throughout the other rooms
3. Move into an enemy to attack it
4. Enemies will chase and attack you when adjacent
5. Defeat all enemies to win!
6. Don't let your HP reach 0!

## Game Stats

- **HP**: Your health points (starts at 30)
- **Score**: Points earned by defeating enemies (10 points per enemy)
- **Enemies**: Number of remaining enemies
- **Turn**: Current turn number

## Strategy Tips

- Don't rush! The game is turn-based, so take your time
- Enemies only move when you move
- Try to fight enemies one at a time
- Orcs are tougher than goblins - be careful!
- Use corridors to your advantage to limit enemy approach angles

## Development

The game is built with pure Python using only standard library modules:
- `random` - For procedural generation
- `os` - For screen clearing
- `sys` - For system operations

## License

MIT License - Feel free to use and modify!