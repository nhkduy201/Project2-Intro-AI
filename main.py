import time
from pysat.solvers import Glucose3
import os
from utlcls import *


GREEN_COLOR = '\033[92m'
RED_COLOR = '\033[91m'


def get_comb(arr, k):
    if k == 0:
        return [[]]

    combs = []

    def comb_utl(arr, k, i, kth, v):
        for j in range(i, len(arr) - kth):
            if kth == 0:
                combs.append(v + [arr[j]])
                continue
            comb_utl(arr, k, j + 1, kth - 1, v + [arr[j]])
    comb_utl(arr, k, 0, k - 1, [])
    return combs


def get_cell_adj(row, col, i, j):
    cell_adj = []
    for h in range(i - 1, i + 2):
        for k in range(j - 1, j + 2):
            if h in range(row) and k in range(col):
                cell_adj.append(h * col + k + 1)
    return cell_adj


def get_exist_clauses(adj, gre):
    if gre == len(adj) or gre == 0:
        return []
    clauses = []
    for i in range(gre):
        combs = get_comb(adj, i)
        for comb in combs:
            clause = []
            for a in adj:
                if a in comb:
                    clause.append(-a)
                else:
                    clause.append(a)
            clauses.append(clause)
    return clauses


def get_cons_clauses(adj, gre):
    if gre == len(adj):
        return [[a] for a in adj]
    elif gre == 0:
        return [[-a] for a in adj]
    clauses = []
    red = len(adj) - gre
    for i in range(red):
        combs = get_comb(adj, i)
        for comb in combs:
            clause = []
            for a in adj:
                if a in comb:
                    clause.append(a)
                else:
                    clause.append(-a)
            clauses.append(clause)
    return clauses


def read_input(input_file):
    return [list(map(lambda x: int(x), line.split()))
            for line in open(input_file, 'r').read().strip().split('\n')]


def write_output(*output_input):
    # print(sol)
    is_sol = output_input[0]
    output = open('output', 'w')
    if not is_sol:
        output.write('NO SOLUTION')
        return
    row = output_input[1]
    col = output_input[2]
    sol = output_input[3]
    for i in range(row):
        for j in range(col):
            if i*col+j+1 in sol:
                print(GREEN_COLOR + '▄', end=' ')
                output.write('g ')
            else:
                print(RED_COLOR + '▄', end=' ')
                output.write('r ')
        print('')
        output.write('\n')
    print('\033[0m')


def get_cell_clauses(inp_mat, row, col, i, j):
    cell_clauses = []
    if inp_mat[i][j] != -1:
        seft_adj = get_cell_adj(
            row, col, i, j)
        exist_clauses = get_exist_clauses(seft_adj, inp_mat[i][j])
        cons_clauses = get_cons_clauses(seft_adj, inp_mat[i][j])
        cell_clauses += (exist_clauses + cons_clauses)
    return cell_clauses


def generate_cnf(inp_mat):
    row = len(inp_mat)
    col = len(inp_mat[0])
    clauses = []
    if row == 2 and col == 2:
        grs = []
        for i in range(row):
            for j in range(col):
                if inp_mat[i][j] not in grs:
                    clauses += get_cell_clauses(inp_mat, row, col, i, j)
                grs.append(inp_mat[i][j])
        return clauses
    if row == 2 and (col == 1 or col > 2):
        for j in range(col):
            if inp_mat[0][j] == inp_mat[1][j]:
                clauses += get_cell_clauses(inp_mat, row, col, 0, j)
            else:
                clauses += get_cell_clauses(inp_mat, row, col, 0, j)
                clauses += get_cell_clauses(inp_mat, row, col, 1, j)
        return clauses
    if col == 2 and (row == 1 or row > 2):
        for i in range(row):
            if inp_mat[i][0] == inp_mat[i][1]:
                clauses += get_cell_clauses(inp_mat, row, col, i, 0)
            else:
                clauses += get_cell_clauses(inp_mat, row, col, i, 0)
                clauses += get_cell_clauses(inp_mat, row, col, i, 1)
        return clauses
    for i in range(row):
        for j in range(col):
            clauses += get_cell_clauses(inp_mat, row, col, i, j)
    # print(clauses)
    return clauses


def pysat_solve(inp_mat):
    row = len(inp_mat)
    col = len(inp_mat[0])
    clauses = generate_cnf(inp_mat)
    g = Glucose3()
    for it in clauses:
        g.add_clause([int(k) for k in it])
    result = g.solve()
    # print(result)
    if result:
        model = g.get_model()
        write_output(*[result, row, col, model])
    else:
        write_output(*[result, None, None, None])


def get_adj_sol(sol, row, col, i, j):
    sol_adj = []
    for h in range(i - 1, i + 2):
        for k in range(j - 1, j + 2):
            if h in range(row) and k in range(col):
                sol_adj.append(sol[h * col + k])
    return sol_adj


def brute_force_check(inp_mat, sol):
    row = len(inp_mat)
    col = len(inp_mat[0])
    for i in range(row):
        for j in range(col):
            if inp_mat[i][j] != -1:
                gr = 0
                for h in range(i - 1, i + 2):
                    for k in range(j - 1, j + 2):
                        if h in range(row) and k in range(col):
                            if sol[h * col + k]:
                                gr += 1
                if inp_mat[i][j] != gr:
                    return False
    return True


def brute_force_solve(inp_mat):
    row = len(inp_mat)
    col = len(inp_mat[0])
    cell = row * col
    tf_sol = []

    def brute_force_solve_utl(i):
        for v in [False, True]:
            tf_sol.append(v)
            if i == cell - 1:
                if brute_force_check(inp_mat, tf_sol):
                    return True
            elif brute_force_solve_utl(i + 1):
                return True
            tf_sol.pop()
        return False

    result = brute_force_solve_utl(0)
    if result:
        sol = []
        for i in range(len(tf_sol)):
            if tf_sol[i]:
                sol.append(i + 1)
        write_output(*[result, row, col, sol])
    else:
        write_output(*[result, None, None, None])


def backtracking_check(inp_mat, sol):
    row = len(inp_mat)
    col = len(inp_mat[0])
    j = (len(sol) - 1) % col
    i = int((len(sol) - 1 - j) / col)
    for h in range(i - 1, i + 2):
        for k in range(j - 1, j + 2):
            if h in range(row) and k in range(col) and inp_mat[h][k] != -1:
                gr = 0
                re = 0
                adj = 0
                for u in range(h - 1, h + 2):
                    for v in range(k - 1, k + 2):
                        if u in range(row) and v in range(col):
                            adj += 1
                            if u * col + v < len(sol):
                                if sol[u * col + v]:
                                    gr += 1
                                else:
                                    re += 1
                if gr > inp_mat[h][k] or re > adj - inp_mat[h][k]:
                    return False
    return True


def backtracking_solve(inp_mat):
    row = len(inp_mat)
    col = len(inp_mat[0])
    cell = row * col
    tf_sol = []

    def backtracking_solve_utl(i):
        for v in [False, True]:
            tf_sol.append(v)
            if backtracking_check(inp_mat, tf_sol):
                if i == cell - 1:
                    return True
                if not backtracking_solve_utl(i + 1):
                    tf_sol.pop()
                else:
                    return True
            else:
                tf_sol.pop()
        return False
    result = backtracking_solve_utl(0)

    if result:
        sol = []
        for i in range(len(tf_sol)):
            if tf_sol[i]:
                sol.append(i + 1)
        write_output(*[result, row, col, sol])
    else:
        write_output(*[result, None, None, None])


def A_star_solve(inp_mat):
    cla = generate_cnf(inp_mat)
    row = len(inp_mat)
    col = len(inp_mat[0])
    rdc_cla = cla
    sol = list(range(1, row * col + 1))
    for i in sol:
        tmp_cla = []
        for c in rdc_cla:
            if -i in c:
                cc = []
                for l in c:
                    cc.append(l)
                cc.remove(-i)
                tmp_cla.append(cc)
            elif i not in c:
                tmp_cla.append(c)
        rdc_cla = tmp_cla
    heu = len(rdc_cla)
    node = MyNode(0, heu, cla, sol)
    open_set = MyHeap([node])
    while len(open_set.arr) != 0:
        cur = open_set.poll()
        if cur.heu == 0:
            write_output(*[True, row, col, cur.sol])
            return
        for j in range(len(cur.sol)):
            tmp_sol = []
            for s in cur.sol:
                tmp_sol.append(s)
            tmp_sol[j] = -tmp_sol[j]
            fir_cla = []
            i = tmp_sol[j]
            for c in cur.cla:
                if -i in c:
                    cc = []
                    for l in c:
                        cc.append(l)
                    cc.remove(-i)
                    fir_cla.append(cc)
                elif i not in c:
                    fir_cla.append(c)
            tmp_cla = cur.cla
            for i in tmp_sol:
                r_cl = []
                for c in tmp_cla:
                    if -i in c:
                        cc = []
                        for l in c:
                            cc.append(l)
                        cc.remove(-i)
                        r_cl.append(cc)
                    elif i not in c:
                        r_cl.append(c)
                tmp_cla = r_cl
            neig_cost = cur.cost + 1
            neig_heu = len(tmp_cla)
            neig_cla = fir_cla
            tmp_sol.remove(tmp_sol[j])
            neig_sol = tmp_sol
            neig_node = MyNode(neig_cost, neig_heu, neig_cla, neig_sol)
            open_set.add(neig_node)
    write_output(*[False, None, None, None])


INPUT_FILE = 'input0'
inp_mat = read_input(INPUT_FILE)
start = time.time()

# pysat_solve(inp_mat)
# brute_force_solve(inp_mat)
# backtracking_solve(inp_mat)
# A_star_solve(inp_mat)

# i = 0
# while os.path.isfile(f'./input{i}'):
#     s = time.time()
#     inp_mat = read_input(f'input{i}')
#     brute_force_solve(inp_mat)
#     e = time.time()
#     print(e - s)
#     print('')
#     i += 1

claus = generate_cnf(inp_mat)
for c in claus:
    print(c)

end = time.time()
print(end - start)
