import time
import random
from copy import deepcopy


faces = ['U','D','F','B','L','R']
colors = {'U':'W','D':'Y','F':'G','B':'B','L':'O','R':'R'}

cube = {f:[[colors[f]]*3 for _ in range(3)] for f in faces}


def rotate_face(face):
    c = deepcopy(cube[face])
    cube[face] = [[c[2-j][i] for j in range(3)] for i in range(3)]

def move_U():
    rotate_face('U')
    cube['F'][0], cube['R'][0], cube['B'][0], cube['L'][0] = cube['R'][0], cube['B'][0], cube['L'][0], cube['F'][0]

def move_D():
    rotate_face('D')
    cube['F'][2], cube['L'][2], cube['B'][2], cube['R'][2] = cube['L'][2], cube['B'][2], cube['R'][2], cube['F'][2]

def move_F():
    rotate_face('F')
    u,r,d,l = cube['U'][2], [row[0] for row in cube['R']], cube['D'][0], [row[2] for row in cube['L']]
    cube['U'][2] = l[::-1]
    for i in range(3): cube['R'][i][0] = u[i]
    cube['D'][0] = r[::-1]
    for i in range(3): cube['L'][i][2] = d[i]

def move_B():
    rotate_face('B')
    u,r,d,l = cube['U'][0], [row[2] for row in cube['R']], cube['D'][2], [row[0] for row in cube['L']]
    cube['U'][0] = [r[i] for i in reversed(range(3))]
    for i in range(3): cube['R'][i][2] = d[i]
    cube['D'][2] = [l[i] for i in reversed(range(3))]
    for i in range(3): cube['L'][i][0] = u[i]

def move_L():
    rotate_face('L')
    u,d,f,b = [row[0] for row in cube['U']], [row[0] for row in cube['D']], [row[0] for row in cube['F']], [row[2] for row in cube['B']]
    for i in range(3):
        cube['U'][i][0] = b[2-i]
        cube['F'][i][0] = u[i]
        cube['D'][i][0] = f[i]
        cube['B'][i][2] = d[2-i]

def move_R():
    rotate_face('R')
    u,d,f,b = [row[2] for row in cube['U']], [row[2] for row in cube['D']], [row[2] for row in cube['F']], [row[0] for row in cube['B']]
    for i in range(3):
        cube['U'][i][2] = f[i]
        cube['F'][i][2] = d[i]
        cube['D'][i][2] = b[2-i]
        cube['B'][i][0] = u[2-i]

def move_M():
    for i in range(3):
        cube['U'][i][1], cube['F'][i][1], cube['D'][i][1], cube['B'][2-i][1] = \
        cube['F'][i][1], cube['D'][i][1], cube['B'][2-i][1], cube['U'][i][1]

def move_S():
    col = 1
    u,d,f,b = [row[col] for row in cube['U']], [row[col] for row in cube['D']], \
               [row[col] for row in cube['F']], [row[col] for row in cube['B']]
    for i in range(3):
        cube['U'][i][col] = f[i]
        cube['F'][i][col] = d[i]
        cube['D'][i][col] = b[i]
        cube['B'][i][col] = u[i]

def move_E():
    cube['F'][1], cube['R'][1], cube['B'][1], cube['L'][1] = \
    cube['R'][1], cube['B'][1], cube['L'][1], cube['F'][1]

def move_X():
    move_R()
    for _ in range(3):
        move_M()
    for _ in range(3):
        move_L()

def move_Y():
    move_U()
    for _ in range(3):
        move_E()
    for _ in range(3):
        move_D()

def move_Z():
    move_F()
    move_S()
    for _ in range(3):
        move_B()

def move_M():
    for i in range(3):
        cube['U'][i][1], cube['F'][i][1], cube['D'][i][1], cube['B'][2-i][1] = \
        cube['F'][i][1], cube['D'][i][1], cube['B'][2-i][1], cube['U'][i][1]

def move_S():
    col = 1
    u,d,f,b = [row[col] for row in cube['U']], [row[col] for row in cube['D']], \
               [row[col] for row in cube['F']], [row[col] for row in cube['B']]
    for i in range(3):
        cube['U'][i][col] = f[i]
        cube['F'][i][col] = d[i]
        cube['D'][i][col] = b[i]
        cube['B'][i][col] = u[i]

def move_E():
    cube['F'][1], cube['R'][1], cube['B'][1], cube['L'][1] = \
    cube['R'][1], cube['B'][1], cube['L'][1], cube['F'][1]


def show_cube():
    print("       ", " ".join(cube['U'][0]))
    print("       ", " ".join(cube['U'][1]))
    print("       ", " ".join(cube['U'][2]))
    print()

    for i in range(3):
        print(" ".join(cube['L'][i]), " ", " ".join(cube['F'][i]), " ", " ".join(cube['R'][i]), " ", " ".join(cube['B'][i]))

    print()
    print("       ", " ".join(cube['D'][0]))
    print("       ", " ".join(cube['D'][1]))
    print("       ", " ".join(cube['D'][2]))


def shuffle_cube(moves=20):
    actions = [move_U, move_D, move_F, move_B, move_L, move_R]
    for _ in range(moves):
        random.choice(actions)()

def is_solved() -> bool:
    for face in cube.values():
        color = face[0][0]
        for row in face:
            if any(cell != color for cell in row):
                return False
    return True


def do_move(move_name: str, repetitions: int = 1):
    for _ in range(repetitions):
        globals()[f"move_{move_name}"]()

def cli():
    print("Rubik's Cube CLI. Введи хід: U, D, F, B, L, R, U', D', F', B', L', R' shuffle або exit")

    moves_count = 0
    start_time = time.time()

    shuffle_cube()

    while True:
        show_cube()
        cmd = input(">>> ")
        if cmd.isspace() and is_solved():
            elapsed = time.time() - start_time
            print(f"Congrats =). You've solved cube in {elapsed} seconds and {moves_count} moves.")

        cmd = cmd.strip().upper()
        if cmd == "EXIT":
            break
        elif cmd == "SHUFFLE":
            shuffle_cube()
            start_time = time.time()
        elif cmd in ["U","D","F","B","L","R"]:
            do_move(cmd)
            moves_count += 1
        elif cmd in ["U'","D'","F'","B'","L'","R'"]:
            do_move(cmd[0], repetitions=3)
            moves_count += 1
        elif cmd in ["U2","D2","F2","B2","L2","R2"]:
            do_move(cmd[0], repetitions=2)
            moves_count += 2
        elif cmd in ["M","S","E"]:
            do_move(cmd)
            moves_count += 2
        elif cmd in ["M'","S'","E'"]:
            do_move(cmd[0], repetitions=3)
            moves_count += 2
        elif cmd in ["M2","S2","E2"]:
            do_move(cmd[0], repetitions=2)
            moves_count += 2
        elif cmd in ["X","Y","Z"]:
            do_move(cmd)
        elif cmd in ["X'","Y'","Z'"]:
            do_move(cmd[0], repetitions=3)
        elif cmd in ["X2","Y2","Z2"]:
            do_move(cmd[0], repetitions=2)
        else:
            print("Невідомий хід")


def main():
    cli()


if __name__ == '__main__':
    main()

