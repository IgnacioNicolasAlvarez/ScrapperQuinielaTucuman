

import requests
from bs4 import BeautifulSoup

from src.db.mongo import ResultadosQuiniela
from src.model import Premio, Sorteo


class QuinielaScrapper:

    def __init__(self, url):
        self.url = url
        self.repositorio = ResultadosQuiniela()

    def __obtener_contenido(self):
        try:
            response = requests.get(self.url)
            response.raise_for_status()
        except requests.exceptions.RequestException as e:
            print("Error al obtener la página:", e)
            return None

        return response.content

    def __parsear_sorteo(self, texto: str) -> Sorteo:
        lineas = texto.split('\n')

        nombre = lineas[0].strip()
        fecha_hora = lineas[1].replace(
            'Sorteo Realizado el', '').replace('a hs', '').replace('  ', '-').strip()
        fecha, hora = fecha_hora.split("-")

        premios = []
        for premio_linea in lineas[2:]:
            if not premio_linea.strip():
                continue
            posicion, _, numero = premio_linea.split()
            premio = Premio(posicion=int(posicion[:-1]), numero=int(numero))
            premios.append(premio)

        sorteo = Sorteo(nombre=nombre, fecha=fecha, hora=hora, premios=premios)
        return sorteo

    def __guardar_sorteo(self, sorteo: Sorteo) -> None:
        self.repositorio.upsert_por_store_day(
            fecha=sorteo.fecha, hora=sorteo.hora, elemento=sorteo.dict())

    def scrappear(self):

        doc = self.__obtener_contenido()

        if doc:
            soup = BeautifulSoup(doc, 'html.parser')

            div_listado = soup.find('div', class_='listado')

            if div_listado:

                divs_box = div_listado.find_all('div', class_='box')

                for div_box in divs_box:
                    contenido = ""
                    ul_listado = div_box.find_all('ul')
                    h1 = div_box.find('h1')
                    contenido = contenido + h1.text + '\n'
                    h2 = div_box.find('h2')
                    contenido = contenido + h2.text + '\n'
                    if ul_listado:
                        for ul in ul_listado:
                            for li in ul.find_all('li'):
                                li_ = ' '.join(
                                    li.text.replace(' °', '°').split())
                                contenido = contenido + li_ + '\n'
                    else:
                        print("No se encontró el elemento ul dentro del div 'box'")

                    self.__guardar_sorteo(
                        sorteo=self.__parsear_sorteo(texto=contenido))
