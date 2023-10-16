from board import GoBoard
from board_util import GoBoardUtil
from board_base import (
    BLACK,
    WHITE,
    EMPTY,
    BORDER,
    GO_COLOR, GO_POINT,
    PASS,
    MAXSIZE,
    coord_to_point,
    opponent
)

def undo(board,move):
    board.board[move]=EMPTY
    board.current_player=opponent(board.current_player)

def game_end(board):
    game_end = board.detect_five_in_a_row()
    if game_end==1:
        return 1 
    elif game_end==2:
        return -1
    elif game_end==3:
        return 0
    else:
        return None

def alphabeta(board,alpha,beta):
    result=game_end(board)
    if (result!=None):
        return result
    solvePoint=board.list_solving_points()
    if solvePoint:
        board.play_move(solvePoint[0],board.current_player)
        result=-alphabeta(board,-beta,-alpha)
        if(result>alpha):
            alpha=result
        undo(board,solvePoint[0])
        if(result>=beta):
            return beta
    else:
        for m in GoBoardUtil.generate_legal_moves(board):
            board.play_move(m,board.current_player)
            result=-alphabeta(board,-beta,-alpha)
            if(result>alpha):
                alpha=result
            undo(board,m)
            if(result>=beta):
                return beta
    return alpha


def solve(board):
    result=game_end(board)
    if (result!=None):
        return result,"First"
    alpha,beta=-1,1
    haveDraw=False
    solvePoint=board.list_solving_points()
    if solvePoint:
        board.play_move(solvePoint[0],board.current_player)
        result=-alphabeta(board,-beta,-alpha)
        undo(board,solvePoint[0])
        if(result==1):
            return True,solvePoint[0]
        elif(result==0):
            haveDraw=True
    else: 
        for m in GoBoardUtil.generate_legal_moves(board):
            board.play_move(m,board.current_player)
            result=-alphabeta(board,-beta,-alpha)
            undo(board,m)
            if(result==1):
                return True,m
            elif(result==0):
                haveDraw=True
    return haveDraw,"NoMove"