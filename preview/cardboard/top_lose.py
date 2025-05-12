import matplotlib.pyplot as plt
import matplotlib.patches as patches

def cm_to_mm(number):
  return number * 10

def calculate_top_depth(depth_mm):
  if depth_mm <= 50:
    return 15
  elif depth_mm <= 100:
    return 20
  else:
    return 20 + 10 * math.ceil((depth_mm - 100) / 50)

def get_clearance(thickness):
  if thickness in (1.90, 2.00):
    clearance = 7.0
  elif thickness == 2.50:
    clearance = 8.0
  else:
    clearance = thickness * 3
  return clearance

def preview(width, height, depth, thickness):
  W = cm_to_mm(width) + get_clearance(thickness)
  H = cm_to_mm(height) + get_clearance(thickness)
  D = calculate_top_depth(cm_to_mm(depth))
  T = thickness

  x0 = D
  y0 = D
  x1 = x0 + W
  y1 = y0 + H
  xL = 0
  xR = x1 + D
  yT = y1 + D
  yB = 0

  fig, ax = plt.subplots()
  ax.set_aspect('equal')
  ax.axis('off')

  # Aba superior
  ax.plot([
    x0,
    x0 - T,
    x0 - T,
    x0,
    x0,
    x1,
    x1,
    x1 + T,
    x1 + T,
    x1
  ], [
    y1,
    y1,
    y1 + D/2,
    y1 + D/2,
    yT,
    yT,
    y1 + D/2,
    y1 + D/2,
    y1,
    y1
  ], 'black', linewidth=0.5)

  # Aba inferior
  ax.plot([
    x0, 
    x0 - T, 
    x0 - T, 
    x0, 
    x0, 
    x1, 
    x1, 
    x1 + T, 
    x1 + T, 
    x1
  ], [
    y0, 
    y0, 
    y0 - D/2, 
    y0 - D/2, 
    y0 - D, 
    y0 - D, 
    y0 - D/2, 
    y0 - D/2, 
    y0, 
    y0
  ], 'black', linewidth=0.5)

  # Aba esquerda
  ax.plot([
    x0, 
    x0 - D/2, 
    x0 - D/2, 
    xL, 
    xL, 
    x0 - D/2, 
    x0 - D/2, 
    x0
  ], [
    y0, 
    y0, 
    y0 - T, 
    y0 - T, 
    y1 + T, 
    y1 + T, 
    y1, 
    y1
  ], 'black', linewidth=0.5)

  # Aba direita
  ax.plot([
    x1, 
    xR - D/2, 
    xR - D/2, 
    xR, 
    xR, 
    xR - D/2, 
    xR - D/2, 
    x1
  ], [
    y0, 
    y0, 
    y0 - T, 
    y0 - T, 
    y1 + T, 
    y1 + T, 
    y1, 
    y1
  ], 'black', linewidth=0.5)

  # Base
  ax.add_patch(
    patches.Rectangle(
      (x0, y0), W, H, 
      edgecolor='red', 
      facecolor='none', 
      linewidth=0.5
    ))

  # Régua vertical à esquerda da aba esquerda
  regua_x = xL - 5
  ax.plot([
    regua_x, 
    regua_x
  ], [
    y0 - T, 
    y1 + T
  ], color='blue', linewidth=0.5)

  ax.plot([
    regua_x - 2, 
    regua_x + 2
  ], [
    y0 - T, 
    y0 - T
  ], color='blue', linewidth=0.5)

  ax.plot([
    regua_x - 2, 
    regua_x + 2
  ], [
    y1 + T, 
    y1 + T
  ], color='blue', linewidth=0.5)

  ax.text(
    regua_x, 
    (y0 + y1) / 2, 
    f"{(H + (2 * T))/10:.1f} cm", 
    fontsize=7, 
    color='blue', 
    ha='right', 
    va='center', 
    rotation=90
  )

  # Régua vertical da altura da base
  regua_x = x1 - 5
  ax.plot([
    regua_x, 
    regua_x
  ], [
    y0, 
    y1
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
    y1, 
    y1
  ], color='blue', linewidth=0.5)

  ax.text(
    regua_x, 
    (y0 + y1) / 2, 
    f"{H/10:.1f} cm", 
    fontsize=7, 
    color='blue', 
    ha='right', 
    va='center', 
    rotation=90
  )

  # Régua horizontal acima da aba superior
  regua_y = y1 + D + 5
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
    f"{(W - (2 * T))/10:.1f} cm", 
    ha='center', 
    va='bottom', 
    fontsize=7, 
    color='blue'
  )

  # Régua horizontal da largura da base
  regua_y = y0 + 5
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
    f"{W/10:.1f} cm", 
    ha='center', 
    va='bottom', 
    fontsize=7, 
    color='blue'
  )

  # Régua vertical da profundidade
  regua_x = x1 - (x1 - x0)/2
  ax.plot([
    regua_x, 
    regua_x
  ], [
    y1, 
    yT
  ], color='blue', linewidth=0.5)

  ax.plot([
    regua_x - 2, 
    regua_x + 2
  ], [
    y1, 
    y1
  ], color='blue', linewidth=0.5)

  ax.plot([
    regua_x - 2, 
    regua_x + 2
  ], [
    yT, 
    yT
  ], color='blue', linewidth=0.5)

  ax.text(
    regua_x,
    (y1 + yT) / 2, 
    f"{D/10:.1f} cm", 
    fontsize=4, 
    color='blue', 
    ha='left', 
    va='center', 
    rotation=-90
  )

  total_width = xR - xL
  total_height = yT

  ax.set_xlim(-7, total_width + 1)
  ax.set_ylim(-1, total_height + 7)

  return fig
