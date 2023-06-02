import heapq
from numpy import Inf
import pygame
from function_utils import *


def astar(draw, grid, start, end):
    count = 0
    open_set = PriorityQueue()
    open_set.put((0, count, start))
    came_from = {}
    g_score = {spot: float("inf") for row in grid for spot in row}
    g_score[start] = 0

    f_score = {spot: float("inf") for row in grid for spot in row}
    f_score[start] = h(start.get_pos(), end.get_pos())

    open_set_hash = {start}

    while not open_set.empty():
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()

        current = open_set.get()[2]
        open_set_hash.remove(current)
        if current == end:
            reconstruct_path(came_from, end, draw)
            end.make_end()
            start.make_start()
            return True

        for neighbor in current.neighbors:
            temp_g_score = g_score[current] + 1
            if temp_g_score < g_score[neighbor]:
                came_from[neighbor] = current
                g_score[neighbor] = temp_g_score
                f_score[neighbor] = temp_g_score + h(neighbor.get_pos(), end.get_pos())

                if neighbor not in open_set_hash:
                    count += 1
                    open_set.put((f_score[neighbor], count, neighbor))
                    open_set_hash.add(neighbor)
                    neighbor.make_open()

        draw()
        if current != start:
            current.make_close()

    return False

def dijkstra(draw, grid, start, end):

    grid_size = len(grid)
    dist = [[Inf] * grid_size for i in range(grid_size)]
    dist[start.row][start.col] = 0

    vis = [[False] * grid_size for i in range(grid_size)]

    pqueue = [(0, start)]
    came_from = {}

    while len(pqueue) > 0:

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()

        _, current = heapq.heappop(pqueue)
        if current == end:
            reconstruct_path(came_from, end, draw)
            end.make_end()
            start.make_start()
            return True

        if vis[current.row][current.col]:
            continue

        vis[current.row][current.col] = True

        for neigh in grid[current.row][current.col].neighbors:
            if dist[current.row][current.col] + 1 < dist[neigh.row][neigh.col]:
                came_from[neigh] = current
                dist[neigh.row][neigh.col] = dist[current.row][current.col] + 1
                heapq.heappush(pqueue, (dist[neigh.row][neigh.col], neigh))

        draw()
        if current != start:
            current.make_close()

    return False

