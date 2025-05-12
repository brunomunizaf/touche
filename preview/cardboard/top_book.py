import matplotlib.pyplot as plt
import matplotlib.patches as patches

def cm_to_mm(number):
  return number * 10

def get_in_between_spacing(thickness):
  if thickness >= 1.5 and thickness <= 2:
    return 6
  else:
    return 8

def preview(width, height, depth, thickness):
  W = cm_to_mm(width)
  H = cm_to_mm(height)
  D = cm_to_mm(depth)
  T = thickness

  in_between_spacing = get_in_between_spacing(T)

  x0 = 0
  y0 = 0
  x1 = x0 + W + 15

  yA = y0 + H + 10
  yB = yA + in_between_spacing
  yC = yB + D
  yD = yC + in_between_spacing
  yE = yD + yA

  fig, ax = plt.subplots()
  ax.set_aspect('equal')
  ax.axis('off')

  ax.add_patch(
    patches.Rectangle(
      (x0, y0), x1, yA, 
      edgecolor='black', 
      facecolor='none', 
      linewidth=0.5
  ))

  ax.add_patch(
    patches.Rectangle(
      (x0, yB), x1, D,
      edgecolor='black', 
      facecolor='none', 
      linewidth=0.5
  ))

  ax.add_patch(
    patches.Rectangle(
      (x0, yD), x1, yE-yD,
      edgecolor='black', 
      facecolor='none', 
      linewidth=0.5
  ))

  # Régua horizontal da largura da base
  regua_y = yE + 5
  ax.plot([
    x0, 
    x1
  ], [
    regua_y, 
    regua_y
  ], color='blue', linewidth=0.5)

  ax.plot([
    x0, 
    x0
  ], [
    regua_y - 2, 
    regua_y + 2
  ], color='blue', linewidth=0.5)
  
  ax.plot([
    x1, 
    x1
  ], [
    regua_y - 2, 
    regua_y + 2
  ], color='blue', linewidth=0.5)

  ax.text(
    (x0 + x1) / 2, 
    regua_y, 
    f"{(x1-x0)/10:.1f} cm", 
    ha='center', 
    va='bottom', 
    fontsize=6, 
    color='blue'
  )

  # Régua vertical da profundidade
  regua_x = x1 + 5
  ax.plot([
    regua_x, 
    regua_x
  ], [
    yB, 
    yC
  ], color='blue', linewidth=0.5)

  ax.plot([
    regua_x - 2, 
    regua_x + 2
  ], [
    yC, 
    yC
  ], color='blue', linewidth=0.5)

  ax.plot([
    regua_x - 2, 
    regua_x + 2
  ], [
    yB, 
    yB
  ], color='blue', linewidth=0.5)

  ax.text(
    regua_x,
    yB + (yC - yB)/2,
    f"{D/10:.1f} cm", 
    fontsize=6, 
    color='blue', 
    ha='left', 
    va='center', 
    rotation=-90
  )

  # Régua vertical do tampo superior
  regua_x = x1 + 5
  ax.plot([
    regua_x, 
    regua_x
  ], [
    yD, 
    yE
  ], color='blue', linewidth=0.5)

  ax.plot([
    regua_x - 2, 
    regua_x + 2
  ], [
    yD, 
    yD
  ], color='blue', linewidth=0.5)

  ax.plot([
    regua_x - 2, 
    regua_x + 2
  ], [
    yE, 
    yE
  ], color='blue', linewidth=0.5)

  ax.text(
    regua_x,
    yD + (yE - yD)/2,
    f"{(H + 10)/10:.1f} cm", 
    fontsize=6, 
    color='blue', 
    ha='left', 
    va='center', 
    rotation=-90
  )

  # Régua vertical do tampo inferior
  regua_x = x1 + 5
  ax.plot([
    regua_x, 
    regua_x
  ], [
    yA, 
    y0
  ], color='blue', linewidth=0.5)

  ax.plot([
    regua_x - 2, 
    regua_x + 2
  ], [
    y0, 
    y0
  ], color='blue', linewidth=0.5)

  ax.plot([
    regua_x - 2, 
    regua_x + 2
  ], [
    yA, 
    yA
  ], color='blue', linewidth=0.5)

  ax.text(
    regua_x,
    y0 + (yA - y0)/2,
    f"{(H + 10)/10:.1f} cm", 
    fontsize=6, 
    color='blue', 
    ha='left', 
    va='center', 
    rotation=-90
  )

  total_width = x1 - x0
  total_height = yE

  ax.set_xlim(0, total_width + 8)
  ax.set_ylim(-1, total_height + 7)
  return fig
