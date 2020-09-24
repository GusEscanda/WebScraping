import requests
import lxml.html

html = requests.get('https://store.steampowered.com/explore/new/') # trae el html de la pagina a inspeccionar 
doc = lxml.html.fromstring(html.content) # genera el objeto lxml que contiene el metodo xpath con el que inspeccionaremos el html


# This statement will return a list of all the divs in the HTML page which have an id of tab_newreleases_content. Now because we know that only 
# one div on the page has this id we can take out the first element from the list ([0]) and that would be our required div. Let's break down the
# xpath and try to understand it:

#      // these double forward slashes tell lxml that we want to search for all tags in the HTML document which match our requirements/filters. 
#      Another option was to use / (a single forward slash). The single forward slash returns only the immediate child tags/nodes which match our 
#      requirements/filters

#      div tells lxml that we are searching for divs in the HTML page

#      [@id="tab_newreleases_content"] tells lxml that we are only interested in those divs which have an id of tab_newreleases_content

new_releases = doc.xpath('//div[@id="tab_newreleases_content"]')[0]


# ahora tengo en new_releases todos los elementos que estan en esa parte del html general (tengo un subconjunto) y puedo seguir haciendo busquedas
# dentro de esa seccion del documento, con el mismo metodo xpath.

# busco entonces, dentro de la seccion "tab_newreleases_content", todos los contenedores (div) de la clase "tab_item_name" y asi obtengo
# una lista de los titulos

# Let's break down this XPath a little bit because it is a bit different from the last one.

#      . tells lxml that we are only interested in the tags which are the children of the new_releases tag

#      [@class="tab_item_name"] is pretty similar to how we were filtering divs based on id. The only difference is that here we are filtering 
#      based on the class name

#      /text() tells lxml that we want the text contained within the tag we just extracted. In this case, it returns the title contained in the
#      div with the tab_item_name class name


titles = new_releases.xpath('.//div[@class="tab_item_name"]/text()')

# lo mismo puedo hacer para extraer los precios

prices = new_releases.xpath('.//div[@class="discount_final_price"]/text()')

# Ahora quiero obtener los tags correspondientes a cada titulo (accion, juego de mesa, aventura, etc)
# la clase es "tab_item_top_tags", pero no se bien porque (tengo que aprender un poco de html y esas cosas...) no funciona lo de poner /text() al
# final del query, como en los dos casos anteriores, para obtener directamente el texto. En cambio hay que obtener una lista de los objetos y 
# despues usar el metodo text_content() para obtener el texto de cada uno

tag_divs = new_releases.xpath('.//div[@class="tab_item_top_tags"]')
tags = []
for div in tag_divs:
    tags.append(div.text_content())
    
# o bien, mas lindo...

tags = [ div.text_content() for div in new_releases.xpath('.//div[@class="tab_item_top_tags"]') ]
    
# >>> tags
# ['Strategy, Casual, Building, Simulation', 'Action, Gore, FPS, Adventure', 'Action', 'Military, FPS, Realistic, Multiplayer', 
# 'Casual, Action, Co-op, Local Co-Op', 'Indie, Funny, Comedy, Stealth', 'Roguelike, Action, Zombies, Medieval', 
# 'Racing, Sports, Driving, Physics', 'Free to Play, Strategy, Card Game, Indie', 'Flight, Programming, Immersive Sim, Open World Survival Craft',
# 'Turn-Based, Board Game, Card Game, Turn-Based Strategy', 'RPG, Adventure, Strategy, Turn-Based', 'Action Roguelike, Action, Indie, RPG', 
# 'Action, Indie, Farming Sim, Action Roguelike', 'Action, Indie, Adventure, Rhythm', 'Indie, Adventure, Base Building, Crafting', 
# 'Action, RPG, Action RPG, Fantasy', 'Singleplayer, JRPG, Roguelite, Tactical RPG', 'Action, Adventure, RPG, Superhero', 
# ...... ]

tags = [ tag.split(', ') for tag in tags ] # convierto todos esos strings de palabras separadas por comas en listas

# Para el caso de las plataformas en que corre cada juego, la data esta organizada distinto. El nombre de la plataforma no viene dado en el texto 
# de algun tag html, como en el resto de los casos de aqui arriba, sino que es el nombre de una clase. Los div donde estan las plataformas de cada 
# juego son los "tab_item_details" y dentro de ellos hay diferentes span c/u con una clase "platform_img" y una correspondiente a la plataforma
# (win/mac/etc.). El proceso de extraccion es un poco mas complicado:

platforms_div = new_releases.xpath('.//div[@class="tab_item_details"]') # obtengo los div
total_platforms = [] # inicializo la lista de plataformas

for game in platforms_div: # para cada juego...
    temp = game.xpath('.//span[contains(@class, "platform_img")]') # obtengo una lista de spans cuyo campo class contenga la palabra "platform_img"
    # para cada span obtengo su campo class (.get('class')) y saco de ahi la ultima palabra (la clase correspondiente a la plataforma)
    platforms = [t.get('class').split(' ')[-1] for t in temp] 
    # elimino de la lista de plataformas el simbolo 'hmd_separator' que estan usando para poner una barra vertical separando distintas categorias
    if 'hmd_separator' in platforms:
        platforms.remove('hmd_separator')
    total_platforms.append(platforms) # agrego la lista de plataformas correspondiente a este juego

# Ahora que tengo todas las listas con la info que necesito, las recorro en paralelo (zip), creo un diccionario (un registro) con cada juego y armo
# una lista con esos diccionarios.

output = []
for info in zip(titles,prices, tags, total_platforms):
    resp = {}
    resp['title'] = info[0]
    resp['price'] = info[1]
    resp['tags'] = info[2]
    resp['platforms'] = info[3]
    output.append(resp)
    
