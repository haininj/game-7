#!/usr/bin/env python3
"""
Test script for roguelike game - verifies core functionality
"""

import sys
import os

# Add parent directory to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from roguelike import Entity, Player, Enemy, GameMap, Game


def test_entity_creation():
    """Test entity creation"""
    print("Testing entity creation...")
    entity = Entity(5, 5, 'E', 'Test Entity', 10, 5)
    assert entity.x == 5
    assert entity.y == 5
    assert entity.char == 'E'
    assert entity.name == 'Test Entity'
    assert entity.hp == 10
    assert entity.attack == 5
    print("✓ Entity creation test passed")


def test_player_creation():
    """Test player creation"""
    print("Testing player creation...")
    player = Player(10, 10)
    assert player.x == 10
    assert player.y == 10
    assert player.char == '@'
    assert player.name == 'Player'
    assert player.hp == 30
    assert player.attack == 5
    assert player.score == 0
    print("✓ Player creation test passed")


def test_enemy_creation():
    """Test enemy creation"""
    print("Testing enemy creation...")
    
    goblin = Enemy(5, 5, 'goblin')
    assert goblin.char == 'g'
    assert goblin.name == 'Goblin'
    assert goblin.hp == 10
    
    orc = Enemy(10, 10, 'orc')
    assert orc.char == 'O'
    assert orc.name == 'Orc'
    assert orc.hp == 15
    
    print("✓ Enemy creation test passed")


def test_map_creation():
    """Test map creation"""
    print("Testing map creation...")
    game_map = GameMap(50, 20)
    assert game_map.width == 50
    assert game_map.height == 20
    assert len(game_map.tiles) == 20
    assert len(game_map.tiles[0]) == 50
    print("✓ Map creation test passed")


def test_map_generation():
    """Test map generation"""
    print("Testing map generation...")
    game_map = GameMap(50, 20)
    game_map.generate(num_rooms=5)
    
    # Should have created some rooms
    assert len(game_map.rooms) > 0
    assert len(game_map.rooms) <= 5
    
    # Should have some walkable tiles
    walkable_count = sum(1 for row in game_map.tiles for tile in row if tile == '.')
    assert walkable_count > 0
    
    print(f"✓ Map generation test passed (created {len(game_map.rooms)} rooms)")


def test_entity_movement():
    """Test entity movement"""
    print("Testing entity movement...")
    game_map = GameMap(20, 20)
    game_map.create_room(5, 5, 10, 10)
    
    entity = Entity(7, 7, 'E', 'Test', 10, 5)
    
    # Should be able to move within room
    assert entity.move(1, 0, game_map) == True
    assert entity.x == 8
    assert entity.y == 7
    
    # Should not be able to move into wall
    entity.x = 4
    entity.y = 5
    assert entity.move(-1, 0, game_map) == False
    assert entity.x == 4  # Position unchanged
    
    print("✓ Entity movement test passed")


def test_combat():
    """Test combat system"""
    print("Testing combat system...")
    player = Player(5, 5)
    enemy = Enemy(6, 5, 'goblin')
    
    initial_hp = enemy.hp
    is_dead = player.take_damage(3)
    
    # Player should take damage but not die
    assert player.hp < player.max_hp
    assert is_dead == False
    
    # Enemy should die after enough damage
    enemy.hp = 1
    is_dead = enemy.take_damage(5)
    assert is_dead == True
    
    print("✓ Combat test passed")


def test_game_initialization():
    """Test game initialization"""
    print("Testing game initialization...")
    game = Game()
    
    # Game should be set up correctly
    assert game.player is not None
    assert game.game_map is not None
    assert len(game.enemies) > 0
    assert game.running == True
    assert game.turn_count == 0
    
    # Player should be in a valid position
    assert game.game_map.is_walkable(game.player.x, game.player.y)
    
    print(f"✓ Game initialization test passed ({len(game.enemies)} enemies spawned)")


def test_map_walkability():
    """Test map walkability checks"""
    print("Testing map walkability...")
    game_map = GameMap(20, 20)
    game_map.create_room(5, 5, 10, 10)
    
    # Floor should be walkable
    assert game_map.is_walkable(7, 7) == True
    
    # Wall should not be walkable
    assert game_map.is_walkable(0, 0) == False
    
    # Out of bounds should not be walkable
    assert game_map.is_walkable(-1, 5) == False
    assert game_map.is_walkable(5, -1) == False
    assert game_map.is_walkable(25, 5) == False
    assert game_map.is_walkable(5, 25) == False
    
    print("✓ Map walkability test passed")


def run_all_tests():
    """Run all tests"""
    print("\n" + "=" * 50)
    print("Running Roguelike Game Tests")
    print("=" * 50 + "\n")
    
    try:
        test_entity_creation()
        test_player_creation()
        test_enemy_creation()
        test_map_creation()
        test_map_generation()
        test_entity_movement()
        test_combat()
        test_game_initialization()
        test_map_walkability()
        
        print("\n" + "=" * 50)
        print("All tests passed! ✓")
        print("=" * 50 + "\n")
        return 0
    except AssertionError as e:
        print(f"\n✗ Test failed: {e}")
        return 1
    except Exception as e:
        print(f"\n✗ Unexpected error: {e}")
        import traceback
        traceback.print_exc()
        return 1


if __name__ == '__main__':
    sys.exit(run_all_tests())
