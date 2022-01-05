import random
import copy
import os
import time
import math
import matplotlib.pyplot as plt

list_of_cities = []


# inside the city class keeps the x y coordinates and name of the city also the distance between two cities is calculated here again
class City(object):

    def __init__(self, num, x, y, distance=None):

        self.x = x
        self.y = y
        self.num = num

        list_of_cities.append(self) #list of cities appen global list then we use that

        self.distance = {self.num: 0.0}# Creates a dictionary of the distances to all the other cities initial always 0
        if distance:
            self.distance = distance



    def point_dist(self, x1, y1, x2, y2):# to coordinaats between calculate
        return math.sqrt((x1 - x2)*(x1 - x2) + (y1 - y2)*(y1 - y2))

    def calculate_distances(self):

        for city in list_of_cities:
            tmp_dist = self.point_dist(self.x, self.y, city.x, city.y)
            self.distance[city.num] = tmp_dist


RouteListX = []
RouteListY = []

# Route Class Created to keep route information and support graphic creation
class Route(object):


    def __init__(self):

        self.route = sorted(list_of_cities, key=lambda *args: random.random())
        ### Calculates its length route lentg hesaplanıyor
        self.calc_rt()

    def calc_rt(self): # calculate root lentg


        self.length = 0.0 # rota özelliğindeki her şehir için:
        for city in self.route:
            # listedeki bir sonraki şehri işaret eden bir sonraki şehir değişkeni ayarlayın ve sonunda ata:
            next_city = self.route[self.route.index(city) - len(self.route) + 1]#Bir sonraki şehre olan mesafeyi bulmak için ilk şehrin Distance_to özelliğini kullanır:

            dist_to_next = city.distance[next_city.num]
            # bu uzunluğu uzunluk özelliğine ekler.
            self.length += dist_to_next

    def printcityName_and_takeValueGraph(self, print_route=False):#Rotadaki şehirleri yazdırma ve en iyi halinde grafiği çizdirmek için kullanılır
        RouteListX.clear()
        RouteListY.clear()

        cities_str = ''
        for city in self.route:
            cities_str += city.num + ','
            RouteListX.append(city.x)
            RouteListY.append(city.y)
        cities_str = cities_str[:-1]  # chops off last comma

        if print_route:
            print('    ' + cities_str)


# Route() nesnelerinin bir popülasyonunu içerir çıkartma Rota nesnelerinin bir listesini içerir ve bunlar hakkında bilgi sağlar.
class RoutePop(object):


    def __init__(self, size, initialise): # Bir popülasyon başlatmak istiyorsak: rt_pop kullanırız
        self.rt_pop = []
        self.size = size

        if initialise:
            for x in range(0, size):
                new_rt = Route()
                self.rt_pop.append(new_rt)#Route nesnelerini listeye ekliyoruz
            self.get_fittest()# en uygun rota, kendi kendine en uygun rotayı ona ayarlar ve Rotayı döndürür

    def get_fittest(self):#Calcualtes fittest route, sets self.fittest to it, and returns the Route.

        # listeyi rotaların uzunluklarına göre sıralar
        sorted_list = sorted(self.rt_pop, key=lambda x: x.length, reverse=False)
        self.fittest = sorted_list[0]
        return self.fittest


# Class for bringing together all of the methods to do with the Genetic Algorithm
class GA(object):


    def crossover(self, parent1, parent2):
        '''
        basit anlamda bir bölgesinden kesilen arrayı 12345678 ile 1234.... X ....5678 gibi karşılıklı yer değiştirir
        '''
        child_rt = Route() #child root created
        for x in range(0, len(child_rt.route)):
            child_rt.route[x] = None

        # Two random integer indices of the parent1:
        start_position = random.randint(1, len(parent1.route)) #every time start pos< end pos
        end_position = random.randint(start_position-1, len(parent1.route))

        for i in range(end_position, start_position):
                child_rt.route[i] = parent1.route[i]  #degerleri birbiri arasında yer değiştiriyoruz

        # Cycles through the parent2. And fills in the child_rt
        # cycles through length of parent2:
        for i in range(len(parent2.route)):

            if not parent2.route[i] in child_rt.route:

                for x in range(len(child_rt.route)): #henüz çocuğu olmayan bir düğüme sahipse yok diyio çıkar
                    if child_rt.route[x] == None:
                        child_rt.route[x] = parent2.route[i]
                        break
        # tüm şehirler alt rotada olana kadar tekrarlanır alt rotayı döndürür (Route() türünden)
        child_rt.calc_rt()
        return child_rt

    def mutation(self, route_to_mut): # mutasyon
        '''
        Route() --> Route()
        Swaps two random indexes in route_to_mut.route. Runs k_mut_prob*100 % of the time
        '''

        if random.random() < 0.39: # her seferinde mutasyon yapılmaması için şart koyuldu böylece  %60  mutasyon yapılıyor
            #bunun yararı rasgelelik olayının artması
            #Choosing Mutation and Crossover Ratios for Genetic Algorithms—A Review with a NewDynamic Approach Ahmad Hassanat Esra’a Alkafaween 2, 2.1 GA PARAMETERS

            # two random indices:
            mut_pos1 = random.randint(0, len(route_to_mut.route) - 1)
            mut_pos2=mut_pos1
            while(mut_pos2==mut_pos1): #chosed different mut
                mut_pos2 = random.randint(0, len(route_to_mut.route) - 1)


            # swap 2 position
            city1 = route_to_mut.route[mut_pos1]
            city2 = route_to_mut.route[mut_pos2]

            route_to_mut.route[mut_pos2] = city1
            route_to_mut.route[mut_pos1] = city2

        # Rotanın uzunluğunu yeniden hesaplayın (.length'i günceller) ve en iyi olan dönmüş olur
        route_to_mut.calc_rt()

        return route_to_mut

    def tournament_select(self, population):#rastgele bir yol bulma ihtimali artar böylece


        # New smaller population#size= tournament size
        tournament_pop = RoutePop(size=7, initialise=False)


        for i in range(6):#size= tournament size -1 # rastgele bireylerle doldurur (aynısını iki kez seçebilir)
            tournament_pop.rt_pop.append(random.choice(population.rt_pop))

        # returns the fittest:
        return tournament_pop.get_fittest()

    def evolve_population(self, init_pop):


        # makes a new population:
        descendant_pop = RoutePop(size=init_pop.size, initialise=True)
        # Elitizm ofseti (yeni popülasyona taşınan Routes() miktarı)
        elitismOffset = 0
        # elitizmimiz varsa, yeni popülasyonun ilkini eskinin en uygununa ayarlayın
        if elitism:
            descendant_pop.rt_pop[0] = init_pop.fittest
            elitismOffset = 1
        # Yeni popülasyondan geçer ve önceki popülasyondan iki turnuva kazananın çocuğuyla doldurur
        for x in range(elitismOffset, descendant_pop.size):
            # two parents:
            tournament_parent1 = self.tournament_select(init_pop)
            tournament_parent2 = self.tournament_select(init_pop)
            # A child:
            tournament_child = self.crossover(tournament_parent1, tournament_parent2)
            # Fill the population up with children
            descendant_pop.rt_pop[x] = tournament_child

        # Tüm yolları mutasyona uğratır (bir prob ile gerçekleşen mutasyon p = 0.4)
        for route in descendant_pop.rt_pop:
            if random.random() < 0.39:
                self.mutation(route)

        # En uygun rotayı güncelleyin:
        descendant_pop.get_fittest()

        return descendant_pop


counterList = []
FittestList = []

def GA_loop(n_generations, pop_size):

    counter = 0

    # Popülasyonu oluşturur:
    print("Creates the population:")
    the_population = RoutePop(pop_size, True)


    best_route = Route()#initial look like counter=0


    for x in range(1, n_generations):# Kaç kez genere edileceği
        # Mevcut tuvali her n nesilde bir günceller (gecikmesini önlemek için n'yi artırın)

        #popolasyonu  geliştirir: Yeni popülasyondan geçer ve önceki popülasyondan iki turnuva kazananın çocuğuyla doldurur
        the_population = GA().evolve_population(the_population)

        # If we have found a new shorter route, save it to best_route
        if the_population.fittest.length < best_route.length:
           #bir kopyasını kullanıyoruz çünkü pointerda hatalara neden oluyor.
            best_route = copy.deepcopy(the_population.fittest)


        # for fitness graph
        counterList.append(counter)
        FittestList.append(the_population.fittest.length)
        counter += 1



    # Prints final output to terminal:
    print("best way founded")
    print('Final best distance:   {0:.2f}'.format(best_route.length))
    print(the_population.fittest.printcityName_and_takeValueGraph())
    best_route.printcityName_and_takeValueGraph(print_route=True)



# Elitizm Doğruysa, bir nesilden en iyisi diğerine aktarılacaktır.
elitism = True

cities = []
cityForGraphX = []
cityForGraphY = []
def CityAnd_GAStarter():
    c = open("City_cord.txt", 'r')
    text = c.read()
    text = text.split("\n")

    for i in text:
        cities.append(i.split(" "))

    print(cities)

    for i in range(101):
        tmp2 = City(str(cities[i][0]), int(cities[i][1]), int(cities[i][2]))
        cityForGraphX.append(cities[i][1])
        cityForGraphY.append(cities[i][2])
    for city in list_of_cities:
        city.calculate_distances()
    ######## create and run an application instance:
    GA_loop(n_generations=10, pop_size=100)


def geneticAlgorithmPlot(zaman, graph):
    plt.plot(zaman, graph, 'r')
    plt.axis([0, max(zaman), min(graph), max(graph)])

    plt.ylabel('Current Fittest')
    plt.xlabel('Time')
    plt.show()


def plotCities():
    cityForGraphX.append(cityForGraphX[0])
    cityForGraphY.append(cityForGraphY[0])
    plt.plot(cityForGraphX, cityForGraphY, 'r')
    plt.show()

    plt.ylabel('City Location')
    plt.xlabel('Time')


def draw_Best():
    plt.plot(RouteListX, RouteListY, 'y')
    plt.show()


CityAnd_GAStarter()
geneticAlgorithmPlot(counterList,FittestList)
plotCities()
print("deger=", RouteListY, RouteListX)
print()
draw_Best()
