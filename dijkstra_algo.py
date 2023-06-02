import heapq
from numpy import Inf
import pygame
from function_utils import *


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

