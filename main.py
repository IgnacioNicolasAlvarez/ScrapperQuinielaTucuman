from datetime import datetime, timedelta

from src.etl.scrapper import QuinielaScrapper


def obtener_fecha_formateada(fecha=None):

    if fecha is None:
        fecha = datetime.now()

    if fecha.weekday() == 6:
        fecha -= timedelta(days=1)

    dia = fecha.strftime('%d')
    mes = fecha.strftime('%m').lstrip('0')
    ano = fecha.strftime('%Y')
    return f"{dia}/{mes}/{ano}"


def main(fecha=None):
    url = f"https://www.cajapopular.gov.ar/sorteos.php?fecha={obtener_fecha_formateada(fecha)}"
    scrapper = QuinielaScrapper(url=url)
    scrapper.scrappear()


if __name__ == "__main__":
    main()
