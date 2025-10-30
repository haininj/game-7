#!/usr/bin/env python3
"""
Demo script for roguelike game - shows a sample game state
"""

import sys
import os

# Add parent directory to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from roguelike import Game


def demo_game():
    """Create and display a sample game state"""
    print("\n" + "=" * 70)
    print("ROGUELIKE GAME - DEMO")
    print("=" * 70 + "\n")
    
    # Create a game instance
    game = Game()
    
    print("Game initialized successfully!")
    print(f"- Map size: {game.width}x{game.height}")
    print(f"- Rooms generated: {len(game.game_map.rooms)}")
    print(f"- Enemies spawned: {len(game.enemies)}")
    print(f"- Player starting position: ({game.player.x}, {game.player.y})")
    print(f"- Player HP: {game.player.hp}/{game.player.max_hp}")
    print()
    
    # Display the initial game state
    print("Initial game state:")
    print()
    
    # Create a copy of the map for rendering
    display = [row[:] for row in game.game_map.tiles]
    
    # Place enemies
    for enemy in game.enemies:
        if 0 <= enemy.y < game.height and 0 <= enemy.x < game.width:
            display[enemy.y][enemy.x] = enemy.char
    
    # Place player
    if 0 <= game.player.y < game.height and 0 <= game.player.x < game.width:
        display[game.player.y][game.player.x] = game.player.char
    
    # Draw map
    print('=' * (game.width + 2))
    for row in display:
        print('|' + ''.join(row) + '|')
    print('=' * (game.width + 2))
    
    print()
    print("Legend:")
    print("  @ = Player (You)")
    print("  g = Goblin (Enemy)")
    print("  O = Orc (Stronger Enemy)")
    print("  # = Wall")
    print("  . = Floor")
    print()
    print("To play the actual game, run: python3 roguelike.py")
    print()
    print("Controls: W/A/S/D to move, Q to quit")
    print("Goal: Defeat all enemies to win!")
    print()
    print("=" * 70)


if __name__ == '__main__':
    demo_game()
