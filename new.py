import random
import pygame

#--------------------------------------------------------INITIALIZATION----------------------------------------------------------------
pygame.init()

#-----------------------------------------------CONSTANTS / SETTING UP SCREEN & FONT----------------------------------------------------
WIDTH = 700
HEIGHT = 700
FPS = 60
CLOCK = pygame.time.Clock()
SCREEN = pygame.display.set_mode([WIDTH, HEIGHT])
score_counter = 0 #Contador a mostrar en pantalla. Muestra el puntaje

pygame.display.set_caption("Homer Game")
font = pygame.font.SysFont("Arial Narrow", 50)
background_image = pygame.image.load(r"")

# #------------------------------------------------------------CHARACTERS------------------------------------------------------------------
# #------------HOMER:
class Homer:
    #Definimos los atributos de homero
    def __init__(self, image, x, y, width, height):
        self.image = image            #La ruta de la imagen
        self.rect = image.get_rect()  #El rectangulo de la imagen
        self.rect.x = x               #La coordenada del borde mas izquierdo del rectangulo
        self.rect.y = y               #La coordenada del borde mas derecho del rectangulo
        self.rect.width = width       #El ancho del rectangulo
        self.rect.height = height     #El largo del rectangulo

    #Definimos un metodo "update_coordinates" para actualizar las coordinadas de homero cuando se apreta una tecla de movimiento
    def update_coordinates(self):
        #Se recorren las teclas presionadas
        keys = pygame.key.get_pressed()
        #Si se presiono A:
        if keys[pygame.K_a]:
            new_x = self.rect.x - 5    #Se cambian las coordenadas del borde mas izquierdo del rectangulo hacia la IZQ ("new_x")
            if new_x > 0:              #Comprobamos si las nuevas coordenadas del borde mas izq del rect NO sobrepasan el borde izq de la pantalla
                self.rect.x = new_x    #Ejercemos el cambio de coordenadas
        #Si se presionó D:
        if keys[pygame.K_d]:
            new_x = self.rect.x + 5    #Se cambian las coordenadas del borde mas izquierdo del rectangulo hacia la DER ("new_x")
            if new_x + self.rect.width < WIDTH: #Comprobamos si las nuevas coordenadas del borde mas derecho del rect NO sobrepasan el borde derecho de la pantalla
                self.rect.x = new_x    ##Ejercemos el cambio de coordenadas

homer_image = pygame.image.load(r"") #Cargo la imagen de homero
homer_image = pygame.transform.scale(homer_image, (200, 200)) #Escalo la imagen
homer = Homer(homer_image, WIDTH / 2 - 100, 478, 200, 200)  #Se crea el objeto "Homer"

#-----------DONUTS:
class Donut:
    def __init__(self, image, x, y, speed):
        self.image = image            #La ruta de la imagen
        self.rect = image.get_rect()  #El rectangulo de la imagen
        self.rect.x = x               #La coordenada del borde mas izquierdo del rectangulo
        self.rect.y = y               #La coordenada del borde mas derecho del rectangulo
        self.speed = speed            #La velocidad de la dona

    def update(self):
        self.rect.y += self.speed

# Creamos la lista de donas
def create_donuts_list():
    donuts_list = []
    #Iteramos la cantidad de veces que dicte el range
    for i in range(10):
        x = random.randrange(0, 740, 60)                      #Asignamos un valor random para la coordenada X
        y = random.randrange(-1000, 0, 60)                    #Asignamos un valor random para la coordenada Y
        speed = random.randrange(10, 20, 1)                   #Asignamos un valor random para la velocidad
        donuts_list.append(Donut(donut_image, x, y, speed))   #Creamos un objeto a partir de la clase "Donut" y guardamos este objeto en la lista de donas
    return donuts_list

donut_image = pygame.image.load(r"") #Cargo la imagen de la dona
donut_image = pygame.transform.scale(donut_image, (100, 100))
donuts_list = create_donuts_list() #Obtenemos la lista de donas y la guardamos en la variable "donuts_list"

#------------------------------------------------------------INTERACTIONS---------------------------------------------------------------
# Actualizamos las coordenadas de las donas en pantalla de acuerdo a las colisiones y si las donas caen fuera de la pantalla
def update_donuts_in_screen():
    global score_counter 
    #Recorremos la lista de donas 
    for donut in donuts_list:
        #Nos fijamos si la dona de la iteracion colisionó con homero
        if homer.rect.colliderect(donut.rect):
            make_donut_dissapear(donut)     #Si colisiono se llama a la funcion para que desaparezca
            score_counter += 1              #Si colisiono se suma un punto
        if donut.rect.y > HEIGHT + 20:
            make_donut_dissapear(donut)     #Si no colisiono  y salió de la pantalla se llama a la funcion para que desaparezca
    return score_counter

def make_donut_dissapear(donut):
    #Asignamos nuevas coordinadas random a las donas para que vuelvan a aparecer en pantalla
    donut.rect.x = random.randrange(0, 740, 60)
    donut.rect.y = random.randrange(-1000, 0, 60)

#---------------------------------------------------------------GAME LOOP----------------------------------------------------------------

running = True
while running:
    #Setteamos los FPS
    time = CLOCK.tick(FPS)

    #Chequeamos si hay un nuevo evento
    event_list = pygame.event.get()
    for event in event_list:
        if event.type == pygame.QUIT:
            running = False
    
    #Actualizamos las coordenadas de homero
    homer.update_coordinates()

    #-------------BLITEAR---------------------------------------------
    #Primero bliteamos el fondo
    SCREEN.blit(background_image, (0, -50))
    #Luego bliteamos a homero
    SCREEN.blit(homer.image, homer.rect)
    #Bliteamos a las donas
    for donut in donuts_list:
        #Actualizamos las coordenadas de la dona iterada en funcion de su velocidad
        donut.update()
        #Bliteamos la dona
        SCREEN.blit(donut.image, donut.rect)

    #Actualizamos la pantalla y el puntaje
    score_counter = update_donuts_in_screen()
    text_to_print = f"SCORE: {str(score_counter)}"
    text = font.render(text_to_print, True, (255, 0, 0))
    SCREEN.blit(text, (20, 20))

    #Actualizamos la pantalla al final de cada bucle
    pygame.display.flip()

pygame.quit()