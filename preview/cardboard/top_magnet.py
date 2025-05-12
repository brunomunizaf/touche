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
  radius = 7

  in_between_spacing = get_in_between_spacing(T)

  x0 = 0
  y0 = 0
  x1 = x0 + W + 15
  yA = y0 + D - 5
  yB = yA + in_between_spacing
  yC = yB + H
  yD = yC + in_between_spacing
  yE = yD + D
  yF = yE + in_between_spacing
  yG = yF + H + 10

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
      (x0, yB), x1, H,
      edgecolor='black', 
      facecolor='none', 
      linewidth=0.5
  ))

  ax.add_patch(
    patches.Rectangle(
      (x0, yD), x1, D,
      edgecolor='black', 
      facecolor='none', 
      linewidth=0.5
  ))

  ax.add_patch(
    patches.Rectangle(
      (x0, yF), x1, H + 10,
      edgecolor='black', 
      facecolor='none', 
      linewidth=0.5
  ))

  if (yA - y0) > 70:
    magnetCenterY = y0 + 30
  else:
    magnetCenterY = y0 + (yA - y0)/2

  if W > 100:
    magnetCenterXA = x0 + (x1 - x0)/4
    magnetCenterXB = x1 - (x1 - x0)/4

    ax.add_patch(
    patches.Circle(
      (magnetCenterXA, magnetCenterY), radius, 
      edgecolor='black', 
      facecolor='none', 
      linewidth=0.5
    ))

    ax.add_patch(
      patches.Circle(
        (magnetCenterXB, magnetCenterY), radius, 
        edgecolor='black', 
        facecolor='none', 
        linewidth=0.5
    ))

    ax.plot([
      x0,
      magnetCenterXA
    ], [
      magnetCenterY, 
      magnetCenterY
    ], color='blue', linewidth=0.5)

    ax.plot([
      x0,
      x0
    ], [
      magnetCenterY + 2, 
      magnetCenterY - 2
    ], color='blue', linewidth=0.5)

    ax.plot([
      magnetCenterXA,
      magnetCenterXA
    ], [
      magnetCenterY + 2, 
      magnetCenterY - 2
    ], color='blue', linewidth=0.5)

    ax.text(
      x0 + (x0 + magnetCenterXA) / 2, 
      magnetCenterY + 5, 
      f"{(magnetCenterXA - x0)/10:.1f} cm", 
      ha='center', 
      va='bottom', 
      fontsize=4, 
      color='blue'
    )
  else:
    magnetCenterX = x0 + (x1 - x0)/2

    ax.add_patch(
      patches.Circle(
        (magnetCenterX, magnetCenterY), radius, 
        edgecolor='black', 
        facecolor='none', 
        linewidth=0.5
    ))

    ax.plot([
      x0,
      magnetCenterX
    ], [
      magnetCenterY, 
      magnetCenterY
    ], color='blue', linewidth=0.5)

    ax.plot([
      x0,
      x0
    ], [
      magnetCenterY + 2, 
      magnetCenterY - 2
    ], color='blue', linewidth=0.5)

    ax.plot([
      magnetCenterX,
      magnetCenterX
    ], [
      magnetCenterY + 2, 
      magnetCenterY - 2
    ], color='blue', linewidth=0.5)

    ax.text(
      x0 + (x0 + magnetCenterX) / 2, 
      magnetCenterY + 5, 
      f"{(magnetCenterX - x0)/10:.1f} cm", 
      ha='center', 
      va='bottom', 
      fontsize=4, 
      color='blue'
    )

  # Régua horizontal da largura da base
  regua_y = yG + 5
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
    f"{(x1 - x0)/10:.1f} cm", 
    ha='center', 
    va='bottom', 
    fontsize=6, 
    color='blue'
  )

  # Régua vertical do tampo inferior

  regua_x = x1 + 5
  ax.plot([
    regua_x, 
    regua_x
  ], [
    yG, 
    yF
  ], color='blue', linewidth=0.5)

  ax.plot([
    regua_x - 2, 
    regua_x + 2
  ], [
    yF, 
    yF
  ], color='blue', linewidth=0.5)

  ax.plot([
    regua_x - 2, 
    regua_x + 2
  ], [
    yG, 
    yG
  ], color='blue', linewidth=0.5)

  ax.text(
    regua_x,
    yF + (yG - yF)/2,
    f"{(H + 10)/10:.1f} cm", 
    fontsize=6, 
    color='blue', 
    ha='left', 
    va='center', 
    rotation=-90
  )

  # Régua vertical da lombada
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
    f"{(H)/10:.1f} cm", 
    fontsize=6, 
    color='blue', 
    ha='left', 
    va='center', 
    rotation=-90
  )

  # Régua vertical da língua

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
    f"{(D-5)/10:.1f} cm", 
    fontsize=6, 
    color='blue', 
    ha='left', 
    va='center', 
    rotation=-90
  )

  total_width = x1 - x0
  total_height = yG

  ax.set_xlim(0, total_width + 7)
  ax.set_ylim(-1, total_height + 7)
  return fig
