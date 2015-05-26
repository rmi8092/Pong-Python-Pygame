#!/usr/bin/env python
# -*- coding: utf-8 -*-

import pygame
import sys
from pygame.locals import *

WIDTH = 640
HEIGHT = 480

class Pelota(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.imagen = cargar_imagen("imagenes/pelota.png", True)
        self.rect = self.imagen.get_rect()
        self.rect.centerx = WIDTH / 2
        self.rect.centery = HEIGHT / 2
        self.speed = [0.3, -0.3]

    def actualizar(self, tiempo, pala_jugador, pala_maquina, puntos, teclado):
        self.rect.centerx += self.speed[0] * tiempo
        self.rect.centery += self.speed[1] * tiempo
        if self.rect.left <= 0:
            puntos[1] += 1
            self.rect.centerx = WIDTH / 2
            self.rect.centery = HEIGHT / 2
            self.speed = [0.0, -0.0]
        if self.rect.right >= WIDTH:
            puntos[0] += 1
            self.rect.centerx = WIDTH / 2
            self.rect.centery = HEIGHT / 2
            self.speed = [0.0, -0.0]
        if self.rect.left <= 0 or self.rect.right >= WIDTH:
            self.speed[0] = -self.speed[0]
            self.rect.centerx += self.speed[0] * tiempo
        if self.rect.top <= 0 or self.rect.bottom >= HEIGHT:
            self.speed[1] = -self.speed[1]
            self.rect.centery += self.speed[1] * tiempo
        if pygame.sprite.collide_rect(self, pala_jugador):
            self.speed[0] = -self.speed[0]
            self.rect.centerx += self.speed[0] * tiempo
        if pygame.sprite.collide_rect(self, pala_maquina):
            self.speed[0] = -self.speed[0]
            self.rect.centerx += self.speed[0] * tiempo
        if teclado[K_SPACE]:
            if self.speed == [0,0]:
                if puntos[0] < 5:
                    self.speed = [0.3, -0.3]
                    self.rect.centerx += self.speed[0] * tiempo
                    self.rect.centery += self.speed[1] * tiempo
                if puntos[0] >= 5:
                    self.speed = [0.4, -0.4]
                    self.rect.centerx += self.speed[0] * tiempo
                    self.rect.centery += self.speed[1] * tiempo
        return puntos

class Pala(pygame.sprite.Sprite):
    def __init__(self, x):
        pygame.sprite.Sprite.__init__(self)
        self.imagen = cargar_imagen("imagenes/pala.png", True)
        self.rect = self.imagen.get_rect()
        self.rect.centerx = x
        self.rect.centery = HEIGHT / 2
        self.speed = 0.5

    def mover(self, tiempo, teclado):
        if self.rect.top >= 0:
            if teclado[K_UP]:
                self.rect.centery -= self.speed * tiempo
        if self.rect.bottom <= HEIGHT:
            if teclado[K_DOWN]:
                self.rect.centery += self.speed * tiempo

    def moverPalaMaquina(self, tiempo, pelota):
        if pelota.speed[0] >= 0 and pelota.rect.centerx >= 4*WIDTH/5:
            if self.rect.centery < pelota.rect.centery:
                self.rect.centery += self.speed * tiempo
            if self.rect.centery > pelota.rect.centery:
                self.rect.centery -= self.speed * tiempo

def cargar_imagen(filename, transparent=False):
	try: imagen = pygame.image.load(filename)
	except pygame.error, message:
		raise SystemExit, message
	imagen = imagen.convert()
	if transparent:
		color = imagen.get_at((0, 0))
		imagen.set_colorkey(color, RLEACCEL)
	return imagen


def texto(texto, posx, posy, color=(255, 255, 255)):
    fuente = pygame.font.Font("imagenes/DroidSans.ttf", 35)
    salida = pygame.font.Font.render(fuente, texto, 1, color)
    salida_rect = salida.get_rect()
    salida_rect.centerx = posx
    salida_rect.centery = posy
    return salida, salida_rect

def main():
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Pong Rafa Miranda")
    imagen_fondo = cargar_imagen('imagenes/fondo_pong.png')
    pelota = Pelota()
    pala_jugador = Pala(30)
    pala_maquina = Pala(WIDTH - 30)
    reloj = pygame.time.Clock()
    puntos = [0,0]
    while True:
        tiempo = reloj.tick(60)
        teclado = pygame.key.get_pressed()
        for eventos in pygame.event.get():
            if eventos.type == QUIT:
                sys.exit(0)
        puntos = pelota.actualizar(tiempo, pala_jugador, pala_maquina, puntos, teclado)
        pala_jugador.mover(tiempo, teclado)
        pala_maquina.moverPalaMaquina(tiempo, pelota)
        p_jug, p_jug_rect = texto(str(puntos[0]), WIDTH/4, 40)
        p_cpu, p_cpu_rect = texto(str(puntos[1]), WIDTH-WIDTH/4, 40)      
        screen.blit(imagen_fondo, (0, 0))
        screen.blit(pelota.imagen, pelota.rect)
        screen.blit(pala_jugador.imagen, pala_jugador.rect)
        screen.blit(pala_maquina.imagen, pala_maquina.rect)
        screen.blit(p_jug, p_jug_rect)
        screen.blit(p_cpu, p_cpu_rect)
        pygame.display.flip()
    return 0

pygame.init()
main()
