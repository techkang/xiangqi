#!/usr/bin/env python
# -*- coding: utf-8 -*-

import argparse
import re
import time
from collections import namedtuple
from itertools import count

###############################################################################
# Piece-Square tables. Tune these to change sunfish's behaviour
###############################################################################
uni_pieces = {'R': '🩤', 'H': '🩣', 'E': '🩢', 'A': '🩡', 'K': '🩠', 'C': '🩥', 'P': '🩦',
              'r': '🩫', 'h': '🩪', 'e': '🩩', 'a': '🩨', 'k': '🩧', 'c': '🩬', 'p': '🩭', '.': '·'}
chinese_pieces = {'R': '车', 'H': '马', 'E': '相', 'A': '仕', 'K': '帅', 'C': '炮', 'P': '兵',
                  'r': '車', 'h': '马', 'e': '象', 'a': '士', 'k': '将', 'c': '砲', 'p': '卒', '.': '· '}

CHESS_ROW = 10
CHESS_COLUMN = 9
BOARD_ROW = CHESS_ROW+4
BOARD_COLUMN = CHESS_COLUMN+2
# king, advisor, elephant, horse, rook, pawn, cannon
piece = {'K': 6000, 'A': 120, 'E': 120, 'H': 270, 'R': 600, 'P': 30, 'C': 285}
pst = {
    'K': (
        0, 0, 0, 0, 0, 0, 0, 0, 0,
        0, 0, 0, 0, 0, 0, 0, 0, 0,
        0, 0, 0, 0, 0, 0, 0, 0, 0,
        0, 0, 0, 0, 0, 0, 0, 0, 0,
        0, 0, 0, 0, 0, 0, 0, 0, 0,
        0, 0, 0, 0, 0, 0, 0, 0, 0,
        0, 0, 0, 0, 0, 0, 0, 0, 0,
        0, 0, 0, -9, -9, -9, 0, 0, 0,
        0, 0, 0, -8, -8, -8, 0, 0, 0,
        0, 0, 0, 1, 5, 1, 0, 0, 0,
    ),
    'A': (
        0, 0, 0, 0, 0, 0, 0, 0, 0,
        0, 0, 0, 0, 0, 0, 0, 0, 0,
        0, 0, 0, 0, 0, 0, 0, 0, 0,
        0, 0, 0, 0, 0, 0, 0, 0, 0,
        0, 0, 0, 0, 0, 0, 0, 0, 0,
        0, 0, 0, 0, 0, 0, 0, 0, 0,
        0, 0, 0, 0, 0, 0, 0, 0, 0,
        0, 0, 0, -1, 0, -1, 0, 0, 0,
        0, 0, 0, 0, 3, 0, 0, 0, 0,
        0, 0, 0, 0, 0, 0, 0, 0, 0,
    ),
    'E': (
        0, 0, 0, 0, 0, 0, 0, 0, 0,
        0, 0, 0, 0, 0, 0, 0, 0, 0,
        0, 0, 0, 0, 0, 0, 0, 0, 0,
        0, 0, 0, 0, 0, 0, 0, 0, 0,
        0, 0, 0, 0, 0, 0, 0, 0, 0,
        0, 0, -1, 0, 0, 0, -1, 0, 0,
        0, 0, 0, 0, 0, 0, 0, 0, 0,
        -2, 0, 0, 0, 3, 0, 0, 0, -2,
        0, 0, 0, 0, 0, 0, 0, 0, 0,
        0, 0, 0, 0, 0, 0, 0, 0, 0,
    ),
    'H': (
        4, 8, 16, 12, 4, 12, 16, 8, 4,
        4, 10, 28, 16, 8, 16, 28, 10, 4,
        12, 14, 16, 20, 18, 20, 16, 14, 12,
        8, 24, 18, 24, 20, 24, 18, 24, 8,
        6, 16, 14, 18, 16, 18, 14, 16, 6,
        4, 12, 16, 14, 12, 14, 16, 12, 4,
        2, 6, 8, 6, 10, 6, 8, 6, 2,
        4, 2, 8, 8, 6, 8, 8, 2, 4,
        0, 2, 4, 4, -10, 4, 4, 2, 0,
        0, -4, 0, 0, 0, 0, 0, -4, 0,

    ),
    'R': (
        14, 14, 12, 18, 16, 18, 12, 14, 14,
        16, 20, 18, 24, 26, 24, 18, 20, 16,
        12, 12, 12, 18, 18, 18, 12, 12, 12,
        12, 18, 16, 22, 22, 22, 16, 18, 12,
        12, 14, 12, 18, 18, 18, 12, 14, 12,
        12, 16, 14, 20, 20, 20, 14, 16, 12,
        6, 10, 8, 14, 14, 14, 8, 10, 6,
        4, 8, 6, 14, 12, 14, 6, 8, 4,
        8, 4, 8, 16, 8, 16, 8, 4, 8,
        -2, 10, 6, 14, 12, 14, 6, 10, -2,
    ),
    'C': (
        6, 4, 0, -10, -12, -10, 0, 4, 6,
        2, 2, 0, -4, -14, -4, 0, 2, 2,
        2, 2, 0, -10, -8, -10, 0, 2, 2,
        0, 0, -2, 4, 10, 4, -2, 0, 0,
        0, 0, 0, 2, 8, 2, 0, 0, 0,
        -2, 0, 4, 2, 6, 2, 4, 0, -2,
        0, 0, 0, 2, 4, 2, 0, 0, 0,
        4, 0, 8, 6, 19, 6, 8, 0, 4,
        0, 2, 4, 6, 6, 6, 4, 2, 0,
        0, 0, 2, 6, 6, 6, 2, 0, 0,
    ),
    'P': (
        0, 3, 6, 9, 12, 9, 6, 3, 0,
        18, 36, 56, 80, 120, 80, 56, 36, 18,
        14, 26, 42, 60, 80, 60, 42, 26, 14,
        10, 20, 30, 34, 40, 34, 30, 20, 10,
        6, 12, 18, 18, 20, 18, 18, 12, 6,
        2, 0, 8, 0, 8, 0, 8, 0, 2,
        0, 0, -2, 0, 4, 0, -2, 0, 0,
        0, 0, 0, 0, 0, 0, 0, 0, 0,
        0, 0, 0, 0, 0, 0, 0, 0, 0,
        0, 0, 0, 0, 0, 0, 0, 0, 0,
    )
}


def padrow(row):
    result = (0,) + tuple(x + piece[k] for x in row) + (0,)
    return result


# Pad tables and join piece and pst dictionaries
for k, table in pst.items():
    pst[k] = sum((padrow(table[i * CHESS_COLUMN:(i+1)*CHESS_COLUMN])
                  for i in range(CHESS_ROW)), ())
    pst[k] = (0,) * 22 + pst[k] + (0,) * 22
    pst[k] = pst[k]

###############################################################################
# Global constants
###############################################################################

# Our board is represented as a 120 character string. The padding allows for
# fast detection of moves that don't stay within the board.
initial = (
    '          \n'
    '          \n'
    ' rheakaehr\n'
    ' .........\n'
    ' .c.....c.\n'
    ' p.p.p.p.p\n'
    ' .........\n'
    # river
    ' .........\n'
    ' P.P.P.P.P\n'
    ' .C.....C.\n'
    ' .........\n'
    ' RHEAKAEHR\n'
    '          \n'
    '          \n'
)

# Lists of possible moves for each piece type.
N, E, S, W = -BOARD_COLUMN, 1, BOARD_COLUMN, -1
directions = {
    'P': (N, W, E),
    'H': ((N, N + E), (N, N + W), (S, S + E), (S, S + W), (E, E + N), (E, E + S), (W, W + N), (W, W + S)),
    'E': ((N + E, N + E), (S + E, S + E), (S + W, S + W), (N + W, N + W)),
    'A': (N + E, S + E, S + W, N + W),
    'R': (N, E, S, W),
    'C': (N, E, S, W),
    'K': (N, E, S, W)
}

# Mate value must be greater than all the other values
# King value is set to twice this value such that if the opponent is
# 8 queens up, but we got the king, we still exceed MATE_VALUE.
# When a MATE is detected, we'll set the score to MATE_UPPER - plies to get there
# E.g. Mate in 3 will be MATE_UPPER - 6
MATE_LOWER = piece['K'] - 2 * (piece['R'] + piece['H'] +
                               piece['C'] + piece['A'] + piece['E'] + 2.5 * piece['P'])
MATE_UPPER = piece['K'] + 2 * (piece['R'] + piece['H'] +
                               piece['C'] + piece['A'] + piece['E'] + 2.5 * piece['P'])

# The table size is the maximum number of elements in the transposition table.
TABLE_SIZE = 1e7

# Constants for tuning search
QS_LIMIT = 219
EVAL_ROUGHNESS = 13
DRAW_TEST = True


###############################################################################
# Chess logic
###############################################################################

class Position(namedtuple('Position', 'board score')):
    """ A state of a chess game
    board -- a BOARD_ROW*BOARD_COLUMN char representation of the board
    score -- the board evaluation
    """

    def gen_moves(self):
        # For each of our pieces, iterate through each possible 'ray' of moves,
        # as defined in the 'directions' map. The rays are broken e.g. by
        # captures or immediately in case of pieces such as horse.
        for i, p in enumerate(self.board):
            if not p.isupper():
                continue
            for d in directions[p]:
                cannon_flag = False
                step = 0
                if isinstance(d, tuple):
                    step = d[0]
                    d = sum(d)
                for j in count(i + d, d):
                    q = self.board[j]
                    # inside the board
                    if q.isspace():
                        break
                    # friend chess
                    if q.isupper() and p != 'C':
                        break
                    if p == 'C':
                        if cannon_flag:
                            if q.islower():
                                pass
                            elif q.isupper():
                                break
                            else:
                                continue
                        # cannon need a carriage to attack opponent
                        elif q.isalpha():
                            cannon_flag = True
                            continue
                    # horse and elephant leg should not be crappy
                    if p in ('H', 'E') and self.board[i + step] != '.':
                        break
                    # king and advisor should stay in palace
                    if p in ('A', 'K'):
                        row, column = j // BOARD_COLUMN, j % BOARD_COLUMN
                        if not (9 <= row <= BOARD_COLUMN and 4 <= column <= 6):
                            break
                    # elephant cannot go across river
                    if p == 'E' and not 6 <= j // BOARD_COLUMN <= BOARD_COLUMN:
                        break
                    # pawn can move east or west only after crossing river
                    if p == 'P' and j // BOARD_COLUMN > 6 and d in (E, W):
                        break
                    # two kings cannot see each other
                    black_king = self.board.index('k')
                    if p == 'K':
                        red_king = j
                    else:
                        red_king = self.board.index('K')
                    if black_king % BOARD_COLUMN == red_king % BOARD_COLUMN:
                        if not any(piece != '.' for piece in self.board[black_king+BOARD_COLUMN:red_king:BOARD_COLUMN]):
                            break

                    # Move it
                    yield i, j
                    if p in 'HPEAK' or q.islower():
                        break

    def rotate(self):
        """ Rotates the board"""
        return Position(self.board[::-1].swapcase(), -self.score)

    def put(self, board, i, p):
        return board[:i] + p + board[i + 1:]

    def move(self, move):
        i, j = move
        # Copy variables and reset ep and kp
        board = self.board
        score = self.score + self.value(move)
        # Actual move
        board = self.put(board, j, board[i])
        board = self.put(board, i, '.')
        return Position(board, score).rotate()

    def value(self, move):
        i, j = move
        p, q = self.board[i], self.board[j]
        MOVE_COST = 0
        # Actual move
        score = pst[p][j] - pst[p][i] - MOVE_COST
        # Capture
        if q.islower():
            score += pst[q.upper()][BOARD_ROW * BOARD_COLUMN-1 - j]
        return score


###############################################################################
# Search logic
###############################################################################

# lower <= s(pos) <= upper
Entry = namedtuple('Entry', 'lower upper')


class Searcher:
    def __init__(self):
        self.tp_score = {}
        self.tp_move = {}
        self.history = set()

    def bound(self, pos, mid, depth, root=True):
        """ returns r where
                s(pos) <= r < mid    if mid > s(pos)
                mid <= r <= s(pos)   if mid <= s(pos)"""

        # Depth <= 0 is QSearch. Here any position is searched as deeply as is needed for
        # calmness, and from this point on there is no difference in behaviour depending on
        # depth, so so there is no reason to keep different depths in the transposition table.
        depth = max(depth, 0)

        # Sunfish is a king-capture engine, so we should always check if we
        # still have a king. Notice since this is the only termination check,
        # the remaining code has to be comfortable with being mated, stalemated
        # or able to capture the opponent king.
        if pos.score <= -MATE_LOWER:
            return -MATE_UPPER

        # We detect 3-fold captures by comparing against previously
        # _actually played_ positions.
        # Note that we need to do this before we look in the table, as the
        # position may have been previously reached with a different score.
        # This is what prevents a search instability.
        # FIXME: This is not true, since other positions will be affected by
        # the new values for all the drawn positions.
        if DRAW_TEST:
            if not root and pos in self.history:
                return 0

        # Look in the table if we have already searched this position before.
        # We also need to be sure, that the stored search was over the same
        # nodes as the current search.
        entry = self.tp_score.get(
            (pos, depth, root), Entry(-MATE_UPPER, MATE_UPPER))
        if entry.lower >= mid and (not root or self.tp_move.get(pos) is not None):
            return entry.lower
        if entry.upper < mid:
            return entry.upper

        # Here extensions may be added
        # Such as 'if in_check: depth += 1'

        # Generator of moves to search in order.
        # This allows us to define the moves, but only calculate them if needed.
        def moves():
            # First try not moving at all. We only do this if there is at least one major
            # piece left on the board, since otherwise zugzwangs are too dangerous.
            if depth > 0 and not root and any(c in pos.board for c in 'RHCP'):
                yield None, -self.bound(pos.rotate(), 1 - mid, depth - 3, root=False)
            # For QSearch we have a different kind of null-move, namely we can just stop
            # and not capture anything else.
            if depth == 0:
                yield None, pos.score
            # Then killer move. We search it twice, but the tp will fix things for us.
            # Note, we don't have to check for legality, since we've already done it
            # before. Also note that in QS the killer must be a capture, otherwise we
            # will be non deterministic.
            killer = self.tp_move.get(pos)
            if killer and (depth > 0 or pos.value(killer) >= QS_LIMIT):
                yield killer, -self.bound(pos.move(killer), 1 - mid, depth - 1, root=False)
            # Then all the other moves
            for move in sorted(pos.gen_moves(), key=pos.value, reverse=True):
                # for val, move in sorted(((pos.value(move), move) for move in pos.gen_moves()), reverse=True):
                # If depth == 0 we only try moves with high intrinsic score (captures and
                # promotions). Otherwise we do all moves.
                if depth > 0 or pos.value(move) >= QS_LIMIT:
                    yield move, -self.bound(pos.move(move), 1 - mid, depth - 1, root=False)

        # Run through the moves, shortcutting when possible
        best = -MATE_UPPER
        for move, score in moves():
            best = max(best, score)
            if best >= mid:
                # Clear before setting, so we always have a value
                if len(self.tp_move) > TABLE_SIZE:
                    self.tp_move.clear()
                # Save the move for pv construction and killer heuristic
                self.tp_move[pos] = move
                break

        # Stalemate checking is a bit tricky: Say we failed low, because
        # we can't (legally) move and so the (real) score is -infinity.
        # At the next depth we are allowed to just return r, -infinity <= r < gamma,
        # which is normally fine.
        # However, what if gamma = -10 and we don't have any legal moves?
        # Then the score is actually a draw and we should fail high!
        # Thus, if best < gamma and best < 0 we need to double check what we are doing.
        # This doesn't prevent sunfish from making a move that results in stalemate,
        # but only if depth == 1, so that's probably fair enough.
        # (Btw, at depth 1 we can also mate without realizing.)
        if best < mid and best < 0 and depth > 0:
            def is_dead(pos): return any(pos.value(m) >=
                                         MATE_LOWER for m in pos.gen_moves())
            if all(is_dead(pos.move(m)) for m in pos.gen_moves()):
                in_check = is_dead(pos.rotate())
                best = -MATE_UPPER if in_check else 0

        # Clear before setting, so we always have a value
        if len(self.tp_score) > TABLE_SIZE:
            self.tp_score.clear()
        # Table part 2
        if best >= mid:
            self.tp_score[pos, depth, root] = Entry(best, entry.upper)
        if best < mid:
            self.tp_score[pos, depth, root] = Entry(entry.lower, best)

        return best

    def search(self, pos, history=()):
        """ Iterative deepening MTD-bi search """
        if DRAW_TEST:
            self.history = set(history)
            # print('# Clearing table due to new history')
            self.tp_score.clear()

        # In finished games, we could potentially go far enough to cause a recursion
        # limit exception. Hence we bound the ply.
        for depth in range(1, 1000):
            # The inner loop is a binary search on the score of the position.
            # Inv: lower <= score <= upper
            # 'while lower != upper' would work, but play tests show a margin of 20 plays
            # better.
            lower, upper = -MATE_UPPER, MATE_UPPER
            while lower < upper - EVAL_ROUGHNESS:
                mid = (lower + upper + 1) // 2
                score = self.bound(pos, mid, depth)
                if score >= mid:
                    lower = score
                if score < mid:
                    upper = score
            # We want to make sure the move to play hasn't been kicked out of the table,
            # So we make another call that must always fail high and thus produce a move.
            self.bound(pos, lower, depth)
            # If the game hasn't finished we can retrieve our move from the
            # transposition table.
            yield depth, self.tp_move.get(pos), self.tp_score.get((pos, depth, True)).lower


###############################################################################
# User interface
###############################################################################

A1 = CHESS_ROW*BOARD_COLUMN+1


def parse(c):
    fil, rank = ord(c[0]) - ord('a'), int(c[1]) - 1
    return A1 + fil - BOARD_COLUMN * rank


def render(i):
    rank, fil = divmod(i - A1, BOARD_COLUMN)
    return chr(fil + ord('a')) + str(-rank + 1)


def print_pos(pos, width=2, piece_type='unicode'):
    print()
    if piece_type == 'unicode':
        pieces = uni_pieces
    else:
        pieces = chinese_pieces
    space = ' '*width
    for i, row in enumerate(pos.board.split()):
        print(' ', CHESS_ROW - 1 - i, ' '.join(pieces.get(p, p) for p in row))
    print('    '+space.join('abcdefghi\n'))


def parse_move(move, board, is_red):
    # import ipdb
    # ipdb.set_trace()
    piece = board[move[0]]
    number_chinese = dict(zip(range(1, 10), '一二三四五六七八九'))
    name = chinese_pieces[piece if is_red else piece.lower()]
    row = CHESS_COLUMN + 1 - move[0] % BOARD_COLUMN
    direction = move[0]//BOARD_COLUMN-move[1]//BOARD_COLUMN
    index = int(direction/abs(direction)) if direction != 0 else 0
    action = ['平', '进', '退'][index]
    if index == 0 or piece in 'AEH':
        destionation = CHESS_COLUMN + 1 - move[1] % BOARD_COLUMN
    else:
        destionation = abs(direction)
    if is_red:
        row = number_chinese[row]
        destionation = number_chinese[destionation]
    else:
        row, destionation = str(row), str(destionation)
    if piece in 'CHPR':
        all_row = [m.start() for m in re.finditer(piece, board)
                   if m.start() % BOARD_COLUMN == move[0] % BOARD_COLUMN]
        if len(all_row) >= 2:
            all_row.remove(move[0])
            row = '前' if all_row[0] > move[0] else '后'
            print(row+name+action+destionation)
            return
    print(name+row+action+destionation)


def main(arg):
    hist = [Position(initial, 0)]
    searcher = Searcher()
    while True:
        print_pos(hist[-1], arg.width, arg.piece)

        if hist[-1].score <= -MATE_LOWER:
            print("You lost")
            break

        # We query the user until she enters a (pseudo) legal move.
        move = None

        while True:
            match = re.match('([a-i][0-9])' * 2, input('Your move: '))
            # match = re.match('([a-i][0-9])' * 2, 'e0d0')
            if match:
                move = parse(match.group(1)), parse(match.group(2))
                if move not in hist[-1].gen_moves():
                    print('Invalid move')
                else:
                    break
            else:
                # Inform the user when invalid input (e.g. "help") is entered
                print("Please enter a move like h2e2")
        parse_move(move, hist[-1].board, True)
        hist.append(hist[-1].move(move))

        # After our move we rotate the board and print it again.
        # This allows us to see the effect of our move.
        print_pos(hist[-1].rotate(), arg.width, arg.piece)

        if hist[-1].score <= -MATE_LOWER:
            print("You won")
            break

        # Fire up the engine to look for a move.
        start = time.perf_counter()
        for _, move, score in searcher.search(hist[-1], hist):
            if time.perf_counter() - start > 1:
                break

        if score == MATE_UPPER:
            print("Checkmate!")

        # The black player moves from a rotated position, so we have to
        # 'back rotate' the move before printing it.
        print("My move: ", end='')
        parse_move(move, hist[-1].board, False)
        hist.append(hist[-1].move(move))


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="xiangqi(Chinese Chess)")
    parser.add_argument('-p', '--piece', default='unicode', type=str, choices=['unicode', 'chinese'],
                        help="Choose unicode if you can distringuish these two character:🩤, 🩣. Otherwise choose chinese.")
    parser.add_argument('-w', '--width', type=int, default=1,
                        help='num of space between two pieces.')
    main(parser.parse_args())
