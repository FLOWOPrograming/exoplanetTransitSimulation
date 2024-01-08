import math

import pygame

def draw_graph_curve(screen, graph, bottom_left, top_right):
    GRAPH_SIZE = len(graph)
    sorted_graph = graph.copy()
    sorted_graph.sort()
    HILO_DATA = (sorted_graph[GRAPH_SIZE - 1], sorted_graph[0])
    AMPLITUDE = HILO_DATA[0] - HILO_DATA[1]
    SIZE = (top_right[0] - bottom_left[0], bottom_left[1] - top_right[1])
    STEP = (SIZE[0] / GRAPH_SIZE, SIZE[1])

    # Draw the curve
    last_coord = (0, 0)
    for i, ratio in enumerate(graph):
        x = bottom_left[0] + STEP[0] * (i + 1)
        y = ratio * STEP[1]  # Calculate raw y data
        y = SIZE[1] - y  # Flip the graph
        if HILO_DATA[1] == 1:
            y = 0
        else:
            y *= 1 / (1 - HILO_DATA[1])
        y = y + top_right[1]  # Position it correctly

        if not i == 0:
            pygame.draw.line(screen, (255, 100, 100), last_coord, (int(x), int(y)), 2)
            pass
        else:
            pygame.draw.line(screen, (255, 100, 100), (int(x), int(y)), (int(x - STEP[0]), int(y)), 2)

        last_coord = (x, y)

def draw_boundaries(screen, bottom_left, top_right):
    pygame.draw.line(screen, (255, 255, 255), bottom_left, (bottom_left[0], top_right[1]), 2)
    pygame.draw.line(screen, (255, 255, 255), (bottom_left[0], top_right[1]), top_right, 2)
    pygame.draw.line(screen, (255, 255, 255), top_right, (top_right[0], bottom_left[1]), 2)
    pygame.draw.line(screen, (255, 255, 255), (top_right[0], bottom_left[1]), bottom_left, 2)

def draw_scale(screen, graph, bottom_left, top_right):
    font = pygame.font.Font('assets/fonts/Roboto-Black.ttf', 15)

    GRAPH_SIZE = len(graph)
    sorted_graph = graph.copy()
    sorted_graph.sort()
    HILO_DATA = (sorted_graph[GRAPH_SIZE - 1], sorted_graph[0])
    AMPLITUDE = HILO_DATA[0] - HILO_DATA[1]
    SIZE = (top_right[0] - bottom_left[0], bottom_left[1] - top_right[1])
    STEP = (SIZE[0] / GRAPH_SIZE, SIZE[1])

    MIN_DATA_PER_LINE = 5

    # x
    MULT = math.floor(math.log(GRAPH_SIZE, MIN_DATA_PER_LINE))
    BIG_SCALE_X = math.floor(MIN_DATA_PER_LINE ** MULT * STEP[0])
    SMALL_SCALE_X = BIG_SCALE_X / MIN_DATA_PER_LINE

    # y
    BIG_SCALE_Y = SIZE[1] / MIN_DATA_PER_LINE
    SMALL_SCALE_Y = BIG_SCALE_Y / MIN_DATA_PER_LINE

    # draw small scale lines
    prev_x = bottom_left[0]
    col_map_x = SMALL_SCALE_X * MIN_DATA_PER_LINE * 255 / SIZE[0]

    prev_y = top_right[1]
    col_map_y = SMALL_SCALE_Y * MIN_DATA_PER_LINE * 255 / SIZE[1]

    while not prev_x > top_right[0]:
        rel_x = prev_x- bottom_left[0]
        x_val = round(rel_x / STEP[0])

        pygame.draw.line(screen, (col_map_x, col_map_x, col_map_x), (prev_x, bottom_left[1]), (prev_x, top_right[1]))

        # text
        text = font.render(str(x_val), True, (255, 255, 255))
        text_rect = text.get_rect()
        text_rect.center = (prev_x, bottom_left[1] + 20)
        text = pygame.transform.rotate(text, -90)

        screen.blit(text, text_rect)

        prev_x += SMALL_SCALE_X

    while not prev_y > bottom_left[1]:
        rel_y = prev_y - top_right[1]
        y_val = ((((SIZE[1] - rel_y) / (STEP[1])) - 1) * AMPLITUDE + 1)

        pygame.draw.line(screen, (col_map_y, col_map_y, col_map_y), (bottom_left[0], prev_y), (top_right[0], prev_y))

        # text
        text = font.render(str(y_val), True, (255, 255, 255))
        text_rect = text.get_rect()
        text_rect.center = (0, prev_y)
        text_rect.right = bottom_left[0] - 10

        screen.blit(text, text_rect)

        prev_y += SMALL_SCALE_Y

    #draw big scale lines
    prev_x = bottom_left[0]
    prev_y = top_right[1]

    while True:
        prev_x += BIG_SCALE_X
        if prev_x > top_right[0]:
            break

        pygame.draw.line(screen, (255, 255, 255), (prev_x, bottom_left[1]), (prev_x, top_right[1]))


    while True:
        prev_y += BIG_SCALE_Y
        if prev_y > bottom_left[1]:
            break

        pygame.draw.line(screen, (255, 255, 255), (bottom_left[0], prev_y), (top_right[0], prev_y))


def graph(screen, graph, bottom_left, top_right):
    draw_scale(screen, graph, bottom_left, top_right)
    draw_boundaries(screen, bottom_left, top_right)
    draw_graph_curve(screen, graph, bottom_left, top_right)
