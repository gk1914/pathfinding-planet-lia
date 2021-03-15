from core.enums import SawDirection


# Predicts the position of the saws in the next game update.
#   return: list of saw positions
def future(saws, map):
    ret = []
    for s in saws:
        sx = s["x"]
        sy = s["y"]
        direction = s["direction"]
        if direction == SawDirection.UP_LEFT:
            next_x = sx - 1
            next_y = sy + 1
        elif direction == SawDirection.UP_RIGHT:
            next_x = sx + 1
            next_y = sy + 1
        elif direction == SawDirection.DOWN_LEFT:
            next_x = sx - 1
            next_y = sy - 1
        else:  # if direction == SawDirection.DOWN_RIGHT:
            next_x = sx + 1
            next_y = sy - 1
        if is_off_map(next_x, next_y, map):
            code = is_off_map(next_x, next_y, map)
            direction = mirror(direction, code)
        if direction == SawDirection.UP_LEFT:
            sx -= 1
            sy += 1
        elif direction == SawDirection.UP_RIGHT:
            sx += 1
            sy += 1
        elif direction == SawDirection.DOWN_LEFT:
            sx -= 1
            sy -= 1
        else:  # if direction == SawDirection.DOWN_RIGHT:
            sx += 1
            sy -= 1
        ret.append((sx, sy))
    return ret


# Checks if position is outside the map limits.
def is_off_map(posX, posY, map):
    map_width = len(map[0])
    map_height = len(map)
    if posX >= map_width and posY >= map_height:
        return 11
    elif posX >= map_width and posY < 0:
        return 12
    elif posX < 0 and posY < 0:
        return 13
    elif posX < 0 and posY >= map_height:
        return 14
    if posX >= map_width:
        return 1
    elif posX < 0:
        return 2
    elif posY >= map_height:
        return 3
    elif posY < 0:
        return 4
    return 0


# Changes the direction when saw collides with a wall/map limit.
def mirror(direction, mirror_code):
    if mirror_code > 10:
        if direction == SawDirection.UP_LEFT:
            return SawDirection.DOWN_RIGHT
        elif direction == SawDirection.UP_RIGHT:
            return SawDirection.DOWN_LEFT
        elif direction == SawDirection.DOWN_LEFT:
            return SawDirection.UP_RIGHT
        elif direction == SawDirection.DOWN_RIGHT:
            return SawDirection.UP_LEFT
    elif mirror_code == 1:
        if direction == SawDirection.UP_RIGHT:
            return SawDirection.UP_LEFT
        elif direction == SawDirection.DOWN_RIGHT:
            return SawDirection.DOWN_LEFT
    elif mirror_code == 2:
        if direction == SawDirection.UP_LEFT:
            return SawDirection.UP_RIGHT
        elif direction == SawDirection.DOWN_LEFT:
            return SawDirection.DOWN_RIGHT
    elif mirror_code == 3:
        if direction == SawDirection.UP_RIGHT:
            return SawDirection.DOWN_RIGHT
        elif direction == SawDirection.UP_LEFT:
            return SawDirection.DOWN_LEFT
    elif mirror_code == 4:
        if direction == SawDirection.DOWN_LEFT:
            return SawDirection.UP_LEFT
        elif direction == SawDirection.DOWN_RIGHT:
            return SawDirection.UP_RIGHT
