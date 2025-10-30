#!/usr/bin/env python3
"""
Roguelike Game - A simple ASCII-based dungeon crawler
"""

import random
import os
import sys


class Entity:
    """Base class for all game entities (player, enemies, etc.)"""
    
    def __init__(self, x, y, char, name, hp, attack):
        self.x = x
        self.y = y
        self.char = char
        self.name = name
        self.hp = hp
        self.max_hp = hp
        self.attack = attack
    
    def move(self, dx, dy, game_map):
        """Move entity by dx, dy if the destination is walkable"""
        new_x = self.x + dx
        new_y = self.y + dy
        
        if game_map.is_walkable(new_x, new_y):
            self.x = new_x
            self.y = new_y
            return True
        return False
    
    def take_damage(self, damage):
        """Apply damage to entity"""
        self.hp -= damage
        return self.hp <= 0


class Player(Entity):
    """Player character"""
    
    def __init__(self, x, y):
        super().__init__(x, y, '@', 'Player', hp=30, attack=5)
        self.score = 0


class Enemy(Entity):
    """Enemy character"""
    
    def __init__(self, x, y, enemy_type='goblin'):
        if enemy_type == 'goblin':
            super().__init__(x, y, 'g', 'Goblin', hp=10, attack=3)
        elif enemy_type == 'orc':
            super().__init__(x, y, 'O', 'Orc', hp=15, attack=4)
        else:
            super().__init__(x, y, 'e', 'Enemy', hp=8, attack=2)
    
    def ai_move(self, player, game_map, entities):
        """Simple AI: move towards player if adjacent, otherwise move randomly"""
        dx = 0
        dy = 0
        
        # Calculate distance to player
        dist_x = player.x - self.x
        dist_y = player.y - self.y
        
        # If adjacent to player, attack
        if abs(dist_x) <= 1 and abs(dist_y) <= 1 and (dist_x != 0 or dist_y != 0):
            return None  # Don't move, just attack
        
        # Move towards player
        if abs(dist_x) > abs(dist_y):
            dx = 1 if dist_x > 0 else -1
        else:
            dy = 1 if dist_y > 0 else -1
        
        # Try to move
        new_x = self.x + dx
        new_y = self.y + dy
        
        # Check if destination is walkable and not occupied by another entity
        if game_map.is_walkable(new_x, new_y):
            occupied = any(e.x == new_x and e.y == new_y for e in entities if e != self)
            if not occupied:
                self.x = new_x
                self.y = new_y


class GameMap:
    """Dungeon map with procedural generation"""
    
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.tiles = [['#' for _ in range(width)] for _ in range(height)]
        self.rooms = []
    
    def is_walkable(self, x, y):
        """Check if a tile is walkable"""
        if x < 0 or x >= self.width or y < 0 or y >= self.height:
            return False
        return self.tiles[y][x] in ['.', '+']
    
    def create_room(self, x, y, width, height):
        """Carve out a rectangular room"""
        for dy in range(height):
            for dx in range(width):
                if 0 <= y + dy < self.height and 0 <= x + dx < self.width:
                    self.tiles[y + dy][x + dx] = '.'
        
        room = {'x': x, 'y': y, 'width': width, 'height': height}
        self.rooms.append(room)
        return room
    
    def create_corridor(self, x1, y1, x2, y2):
        """Create an L-shaped corridor between two points"""
        # Horizontal first
        for x in range(min(x1, x2), max(x1, x2) + 1):
            if 0 <= x < self.width and 0 <= y1 < self.height:
                self.tiles[y1][x] = '.'
        
        # Then vertical
        for y in range(min(y1, y2), max(y1, y2) + 1):
            if 0 <= x2 < self.width and 0 <= y < self.height:
                self.tiles[y][x2] = '.'
    
    def generate(self, num_rooms=6):
        """Generate a dungeon with rooms and corridors"""
        for _ in range(num_rooms):
            width = random.randint(4, 10)
            height = random.randint(4, 8)
            x = random.randint(1, self.width - width - 1)
            y = random.randint(1, self.height - height - 1)
            
            # Check if room overlaps with existing rooms
            overlaps = False
            for room in self.rooms:
                if not (x + width < room['x'] or x > room['x'] + room['width'] or
                        y + height < room['y'] or y > room['y'] + room['height']):
                    overlaps = True
                    break
            
            if not overlaps:
                room = self.create_room(x, y, width, height)
                
                # Connect to previous room
                if len(self.rooms) > 1:
                    prev_room = self.rooms[-2]
                    prev_center_x = prev_room['x'] + prev_room['width'] // 2
                    prev_center_y = prev_room['y'] + prev_room['height'] // 2
                    curr_center_x = room['x'] + room['width'] // 2
                    curr_center_y = room['y'] + room['height'] // 2
                    
                    self.create_corridor(prev_center_x, prev_center_y, curr_center_x, curr_center_y)
    
    def get_random_room_position(self, room_index=0):
        """Get a random position within a room"""
        if not self.rooms:
            return (self.width // 2, self.height // 2)
        
        room = self.rooms[room_index % len(self.rooms)]
        x = room['x'] + random.randint(1, room['width'] - 2)
        y = room['y'] + random.randint(1, room['height'] - 2)
        return (x, y)


class Game:
    """Main game class"""
    
    def __init__(self):
        self.width = 60
        self.height = 20
        self.game_map = GameMap(self.width, self.height)
        self.game_map.generate()
        
        # Place player in first room
        player_pos = self.game_map.get_random_room_position(0)
        self.player = Player(player_pos[0], player_pos[1])
        
        # Place enemies
        self.enemies = []
        num_enemies = min(len(self.game_map.rooms) * 2, 8)
        for i in range(num_enemies):
            room_idx = (i % (len(self.game_map.rooms) - 1)) + 1  # Skip first room
            enemy_pos = self.game_map.get_random_room_position(room_idx)
            enemy_type = 'goblin' if random.random() < 0.7 else 'orc'
            self.enemies.append(Enemy(enemy_pos[0], enemy_pos[1], enemy_type))
        
        self.messages = []
        self.running = True
        self.turn_count = 0
    
    def add_message(self, message):
        """Add a message to the message log"""
        self.messages.append(message)
        if len(self.messages) > 5:
            self.messages.pop(0)
    
    def clear_screen(self):
        """Clear the terminal screen"""
        os.system('clear' if os.name != 'nt' else 'cls')
    
    def render(self):
        """Render the game screen"""
        self.clear_screen()
        
        # Create a copy of the map for rendering
        display = [row[:] for row in self.game_map.tiles]
        
        # Place enemies
        for enemy in self.enemies:
            if 0 <= enemy.y < self.height and 0 <= enemy.x < self.width:
                display[enemy.y][enemy.x] = enemy.char
        
        # Place player
        if 0 <= self.player.y < self.height and 0 <= self.player.x < self.width:
            display[self.player.y][self.player.x] = self.player.char
        
        # Draw map
        print('=' * (self.width + 2))
        for row in display:
            print('|' + ''.join(row) + '|')
        print('=' * (self.width + 2))
        
        # Draw UI
        print(f"HP: {self.player.hp}/{self.player.max_hp} | Score: {self.player.score} | Enemies: {len(self.enemies)} | Turn: {self.turn_count}")
        print()
        
        # Draw messages
        print("Messages:")
        for msg in self.messages:
            print(f"  {msg}")
        print()
        print("Controls: WASD to move, Q to quit")
        print("Goal: Defeat all enemies!")
    
    def handle_combat(self, attacker, defender):
        """Handle combat between two entities"""
        damage = attacker.attack + random.randint(-1, 1)
        damage = max(1, damage)  # At least 1 damage
        
        is_dead = defender.take_damage(damage)
        self.add_message(f"{attacker.name} attacks {defender.name} for {damage} damage!")
        
        if is_dead:
            self.add_message(f"{defender.name} has been defeated!")
            return True
        return False
    
    def player_move(self, dx, dy):
        """Handle player movement and combat"""
        new_x = self.player.x + dx
        new_y = self.player.y + dy
        
        # Check for enemy at destination
        enemy_at_pos = None
        for enemy in self.enemies:
            if enemy.x == new_x and enemy.y == new_y:
                enemy_at_pos = enemy
                break
        
        if enemy_at_pos:
            # Attack enemy
            if self.handle_combat(self.player, enemy_at_pos):
                self.enemies.remove(enemy_at_pos)
                self.player.score += 10
        else:
            # Move player
            if self.player.move(dx, dy, self.game_map):
                self.turn_count += 1
    
    def enemy_turn(self):
        """Process all enemy turns"""
        all_entities = [self.player] + self.enemies
        
        for enemy in self.enemies[:]:  # Use slice to iterate over copy
            # Check if adjacent to player
            dx = abs(self.player.x - enemy.x)
            dy = abs(self.player.y - enemy.y)
            
            if dx <= 1 and dy <= 1 and (dx != 0 or dy != 0):
                # Attack player
                if self.handle_combat(enemy, self.player):
                    self.add_message("You have been defeated!")
                    self.running = False
                    return
            else:
                # Move towards player
                enemy.ai_move(self.player, self.game_map, all_entities)
    
    def check_win_condition(self):
        """Check if player has won"""
        if len(self.enemies) == 0:
            self.add_message("Congratulations! You've defeated all enemies!")
            self.running = False
            return True
        return False
    
    def run(self):
        """Main game loop"""
        self.add_message("Welcome to the dungeon! Defeat all enemies to win.")
        
        while self.running:
            self.render()
            
            # Get player input
            try:
                if os.name == 'nt':  # Windows
                    import msvcrt
                    key = msvcrt.getch().decode('utf-8').lower()
                else:  # Unix-like
                    import tty
                    import termios
                    fd = sys.stdin.fileno()
                    old_settings = termios.tcgetattr(fd)
                    try:
                        tty.setraw(fd)
                        key = sys.stdin.read(1).lower()
                    finally:
                        termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)
            except:
                key = input("Enter command (w/a/s/d/q): ").lower()
            
            # Process input
            if key == 'q':
                self.running = False
                break
            elif key == 'w':
                self.player_move(0, -1)
                self.enemy_turn()
            elif key == 's':
                self.player_move(0, 1)
                self.enemy_turn()
            elif key == 'a':
                self.player_move(-1, 0)
                self.enemy_turn()
            elif key == 'd':
                self.player_move(1, 0)
                self.enemy_turn()
            else:
                continue
            
            # Check win condition
            self.check_win_condition()
        
        # Game over
        self.render()
        print("\n" + "=" * 40)
        if len(self.enemies) == 0:
            print(f"VICTORY! Final Score: {self.player.score}")
        elif self.player.hp <= 0:
            print(f"GAME OVER! Final Score: {self.player.score}")
        else:
            print(f"Thanks for playing! Final Score: {self.player.score}")
        print("=" * 40)


def main():
    """Entry point"""
    game = Game()
    game.run()


if __name__ == '__main__':
    main()
