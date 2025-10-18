stack = [1, 2, 3, 4, 5, 6, 7, 8, 9]
cube = [[0, 0, 0],
        [0, 0, 0],
        [0, 0, 0]]

def magic_cube():
  

  if cube[0][0] + cube[0][1] + cube[0][2] == 15 and cube[1][0] + cube[1][1] + cube[1][2] == 15 and cube[2][0] + cube[2][1] + cube[2][2] == 15 and cube[0][0] + cube[1][0] + cube[2][0] == 15 and cube[0][1] + cube[1][1] + cube[2][1] == 15 and cube[0][2] + cube[1][2] + cube[2][2] == 15 and cube[0][0] + cube[1][1] + cube[2][2] == 15 and cube[2][0] + cube[1][1] + cube[0][2] == 15:
    print("Magin cube is complete")
    return cube