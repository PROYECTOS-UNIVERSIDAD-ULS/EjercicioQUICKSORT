import sys
import pygame

# Inicializar Pygame
pygame.init()

# Dimensiones de la ventana
ANCHO, ALTO = 800, 600
VENTANA = pygame.display.set_mode((ANCHO, ALTO))
pygame.display.set_caption(
    "Visualizador de Quicksort - Mis Valores (Pygame)"
)

# Definir Colores
BLANCO = (255, 255, 255)
NEGRO = (0, 0, 0)
AZUL = (52, 152, 219)
NARANJA = (230, 126, 34)  # Pivote
VERDE = (46, 204, 113)  # Barras ordenadas

# Se agregan valores dependiendo de la situacion (de 5 a 15 valores unicamente)
mis_valores = [120, 350, 80, 400, 200, 150, 300, 50, 270, 190]

# Validar automáticamente que cumpla con la regla de 5 a 15 valores
if len(mis_valores) < 5:
  mis_valores = [100, 200, 300, 400, 150]  # Por defecto si pones menos de 5
elif len(mis_valores) > 15:
  mis_valores = mis_valores[:15]  # Corta a 15 si te pasas

datos = mis_valores
NUM_ELEMENTOS = len(datos)
ancho_barra = ANCHO // NUM_ELEMENTOS


def dibujar(datos_actuales, pivote_idx=-1):
  """Dibuja el estado actual del arreglo de barras en la pantalla."""
  VENTANA.fill(BLANCO)

  for i, val in enumerate(datos_actuales):
    color = AZUL
    if i == pivote_idx:
      color = NARANJA  # Resaltar el pivote actual

    pygame.draw.rect(
        VENTANA,
        color,
        (i * ancho_barra + 10, ALTO - val - 80, ancho_barra - 20, val),
    )

    # Mostrar el número exacto encima de cada barra para que se lea bien
    fuente_val = pygame.font.SysFont("Arial", 16)
    texto_val = fuente_val.render(str(val), True, NEGRO)
    VENTANA.blit(texto_val, (i * ancho_barra + (ancho_barra // 2) - 10, ALTO - val - 110))

  # Texto explicativo en pantalla
  fuente = pygame.font.SysFont("Arial", 20)
  texto = fuente.render(
      "Visualizando Quicksort con tus valores: Naranja = Pivote", True, NEGRO
  )
  VENTANA.blit(texto, (20, 20))

  pygame.display.update()
  pygame.time.delay(300)  # Pausa de 300ms para verlo con calma y claridad


def quicksort_animado(arr, inicio, fin):
  """Función recursiva de Quicksort adaptada para animación con Pygame."""
  if inicio < fin:
    yield from particion_animada(arr, inicio, fin)
    pi = particion_indice(arr, inicio, fin)

    yield from quicksort_animado(arr, inicio, pi - 1)
    yield from quicksort_animado(arr, pi + 1, fin)


def particion_animada(arr, inicio, fin):
  """Anima los movimientos de la partición."""
  pivote = arr[fin]
  i = inicio - 1

  for j in range(inicio, fin):
    for event in pygame.event.get():
      if event.type == pygame.QUIT:
        pygame.quit()
        sys.exit()

    if arr[j] <= pivote:
      i += 1
      arr[i], arr[j] = arr[j], arr[i]

    dibujar(arr, fin)
    yield

  arr[i + 1], arr[fin] = arr[fin], arr[i + 1]
  dibujar(arr, i + 1)
  yield


def particion_indice(arr, inicio, fin):
  """Calcula la posición final del pivote sin animar."""
  pivote = arr[fin]
  i = inicio - 1
  for j in range(inicio, fin):
    if arr[j] <= pivote:
      i += 1
      arr[i], arr[j] = arr[j], arr[i]
  arr[i + 1], arr[fin] = arr[fin], arr[i + 1]
  return i + 1


def main():
  reloj = pygame.time.Clock()
  ordenador = quicksort_animado(datos, 0, len(datos) - 1)

  corriendo = True
  completado = False

  while corriendo:
    for event in pygame.event.get():
      if event.type == pygame.QUIT:
        corriendo = False

    if not completado:
      try:
        next(ordenador)
      except StopIteration:
        completado = True
    else:
      # Pantalla final cuando termina de ordenar
      VENTANA.fill(BLANCO)
      for i, val in enumerate(datos):
        pygame.draw.rect(
            VENTANA,
            VERDE,
            (i * ancho_barra + 10, ALTO - val - 80, ancho_barra - 20, val),
        )
        fuente_val = pygame.font.SysFont("Times New Roman", 16)
        texto_val = fuente_val.render(str(val), True, NEGRO)
        VENTANA.blit(texto_val, (i * ancho_barra + (ancho_barra // 2) - 10, ALTO - val - 110))

      fuente = pygame.font.SysFont("Arial", 22)
      texto = fuente.render(
          "Se completo el ordenamiento exitosamente",
          True,
          NEGRO,
      )
      VENTANA.blit(texto, (20, 20))
      pygame.display.update()

    reloj.tick(60)

  pygame.quit()


if __name__ == "__main__":
  main()