# Requests: libreria super basica que te permite traer una pagina y hacer algunos trabajos con ella
# Documentacion: https://requests.readthedocs.io/en/master/
import requests
result = requests.get('https://www.google.com/search?q=gustavo&oq=gustavo&aqs=chrome..69i57j46l3j69i61l2j69i65j69i61.3649j0j7&sourceid=chrome&ie=UTF-8')   # traigo la pagina
ok = (result.status_code == 200) # verifico el codigo (200=OK)
result.headers # aca se guardan los headers (sea lo que eso fuere...(tengo que aprender algo de web))
cont = result.content  # guardo el contenido de la pagina en una variable

# Beautiful Soup 4: libreria que te permite hacer parsind de la pagina obtenida, buscar los elementos en ella. 
# Con esta y requests es suficiente para hacer algun programita sencillo
# Documentacion: https://www.crummy.com/software/BeautifulSoup/bs4/doc/
# Ejemplito de uso: https://gist.github.com/bradmontgomery/1872970
from bs4 import BeautifulSoup
soup = BeautifulSoup(cont) # genero el objeto tipo 'soup'. alternativa soup = BeautifulSoup(cont,'html.parser')
samples = soup.find_all("a")  # busco dentro del objeto generado

for a in samples:
    print(a.attrs['href'])


# Lxml: libreria que te permite hacer lo mismo que Beautiful Soup (tambien requiere la libreria requests)
# esta es mejor desde el punto de vista de la performance aunque es cuestion de gustos elegir una o la otra
# Documentacion: https://lxml.de/index.html
# Tutorial: https://docs.python-guide.org/scenarios/scrape/
from lxml import html
page = requests.get('http://econpy.pythonanywhere.com/ex/001.html') # traigo la pagina con requests
tree = html.fromstring(page.content) # genero un arbol, que luego puedo inspeccionar con XPath o CSSSelect

buyers = tree.xpath('//div[@title="buyer-name"]/text()') # armo una lista con los nombres
prices = tree.xpath('//span[@class="item-price"]/text()') # armo una lista con los precios

# Selenium: Esta libreria se necesita cuando el sitio a scrapear no carga directamente sino que lo hace a 
# medida que el usuario pasa por lugares con el mouse o tiene un funcionamiento especifico programado con
# javascript. Lo que hace es automatizar la tarea de abrir un chrome o algun navegador y hacer los clicks 
# necesarios para obtener la info. Despues usas tu parser favorito para convertir esa info en la estructura
# de datos que necesitas.
# Documentacion: https://selenium-python.readthedocs.io/
# Tutorial: http://thiagomarzagao.com/2013/11/12/webscraping-with-selenium-part-1/
# Programa Ejemplo: https://www.scrapehero.com/tutorial-web-scraping-hotel-prices-using-selenium-and-python/


# Scrapy: Este es el mejor pero tambien el mas complicado, de hecho no es solo una libreria sino un 
# framework completo, que te permite automatizar sistemas de scraping para sitios completos. Se puede usar
# en conjunto con Selenium o cualquier modulo de scraping para Python
# Documentacion: https://scrapy.org/
# Tutorial de como hacer scraping a un sitio de e-commerce: https://medium.com/@kaismh/extracting-data-from-websites-using-scrapy-e1e1e357651a#.sw7c9ycio





