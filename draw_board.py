def chinese_chess(mode='unicode'):
    pieces_chinese = '帅仕相马车炮兵将士象馬車砲卒'
    pieces_unicode = U''.join(chr(0x1FA60 + i) for i in range(14))
    # king advisor elephant rook cannon horse pawn
    pieces_fen = 'KAEHRCPkaehrcp'
    if mode == 'unicode':
        pieces = pieces_unicode
    else:
        pieces = pieces_chinese
    fen_map = dict(zip(pieces_fen, pieces))
    fen_start = 'rheakaehr/9/1c5c1/p1p1p1p1p/9/9/P1P1P1P1P/1C5C1/9/RHEAKAEHR w - - 0 1'

    box = u''.join(chr(9472 + x) for x in (2, 0, 12, 16, 20, 24, 44, 52, 28, 36, 60))
    vbar, hbar, ul, ur, ll, lr, nt, st, wt, et, plus = box
    # │     ─   ┌   ┐   └   ┘   ┬   ┴    ├    ┤   ┼
    ls, rs = '\uff3c', '\uff0f'
    # ／ ＼
    h3 = hbar * 3
    h2 = hbar * 2
    # useful constant unicode strings to draw the square borders
    inter = (vbar + '   ') * 8 + vbar
    topline = [ul, *[nt] * 7, ur]
    midline = [wt, *[plus] * 7, et]
    rivertop = [wt, *[st] * 7, et]
    riverline = [vbar, '楚', '河', '     ', '汉', '界', vbar]
    riverdown = [wt, *[nt] * 7, et]
    blackline = [vbar] * 9
    topblackline = [vbar, '   '] * 3 + [vbar, ' ', ls, vbar, rs, ' ', vbar] + ['   ', vbar] * 3
    canonblackline = [vbar, '   '] * 3 + [vbar, ' ', rs, vbar, ls, ' ', vbar] + ['   ', vbar] * 3
    bottomline = [ll, *[st] * 7, lr]

    def fill(line: list, fen_string: str):
        """Return a unicode string with a line of the chessboard.
        """
        line_copy = line[:]
        h_list = []
        index = 0
        for char in fen_string:
            if char.isnumeric():
                index += int(char)
                h_list.extend([h3] * int(char))
            else:
                line_copy[index] = fen_map[char]
                index += 1
                if mode == 'unicode':
                    h_list.append(' ' + h2)
                else:
                    h_list.append(h2)
        result = ''
        h_list[-1] = ''
        for char, h in zip(line_copy, h_list):
            result += char + h
        return result

    def _game(fen_line):
        for i, fen in enumerate(fen_line.split()[0].split('/')):
            if i == 0:
                line = topline
            elif i == 9:
                line = bottomline
            elif i == 4:
                line = rivertop
            elif i == 5:
                line = riverdown
            else:
                line = midline
            yield fill(line, fen)
            if i == 0 or i == 7:
                yield ''.join(topblackline)
            elif i == 1 or i == 8:
                yield ''.join(canonblackline)
            elif i == 4:
                yield '   '.join(riverline)
            elif i < 9:
                yield '   '.join(blackline)

    game = lambda squares: "\n".join(_game(squares))
    game.__doc__ = """Return the chessboard as a string for a given position.
        position is a list of 8 lists or tuples of length 8 containing integers
    """
    return game(fen_start)


def chess():
    pieces = u''.join(chr(9812 + x) for x in range(12))
    pieces = u' ' + pieces[:6][::-1] + pieces[6:]
    box = u''.join(chr(9472 + x) for x in (2, 0, 12, 16, 20, 24, 44, 52, 28, 36, 60))
    vbar, hbar, ul, ur, ll, lr, nt, st, wt, et, plus = box
    # │     ─   ┌   ┐   └   ┘   ┬   ┴    ├    ┤   ┼
    h3 = hbar * 3
    # useful constant unicode strings to draw the square borders
    topline = ul + (h3 + nt) * 7 + h3 + ur
    midline = wt + (h3 + plus) * 7 + h3 + et
    botline = ll + (h3 + st) * 7 + h3 + lr
    tpl = u' {0} ' + vbar

    def inter(*args):
        """Return a unicode string with a line of the chessboard.

        args are 8 integers with the values
            0 : empty square
            1, 2, 3, 4, 5, 6: white pawn, knight, bishop, rook, queen, king
            -1, -2, -3, -4, -5, -6: same black pieces
        """
        assert len(args) == 8
        return vbar + u''.join((tpl.format(pieces[a]) for a in args))

    print(pieces)
    print(' '.join(box))
    start_position = (
            [
                (-4, -2, -3, -5, -6, -3, -2, -4),
                (-1,) * 8,
            ] +
            [(0,) * 8] * 4 +
            [
                (1,) * 8,
                (4, 2, 3, 5, 6, 3, 2, 4),
            ]
    )

    def _game(position):
        yield topline
        yield inter(*position[0])
        for row in position[1:]:
            yield midline
            yield inter(*row)
        yield botline

    game = lambda squares: "\n".join(_game(squares))
    game.__doc__ = """Return the chessboard as a string for a given position.
        position is a list of 8 lists or tuples of length 8 containing integers
    """
    return game(start_position)


if __name__ == "__main__":
    print(chinese_chess())
