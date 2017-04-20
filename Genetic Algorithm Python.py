from random import (choice, random, randint)

__all__ = ['Chromosome', 'Population','Maze']

class Maze:
    WALL = '#'
    FLOOR = ' '
    PLAYER = 'P'
    FINISH = 'F'

    def __init__(self):
        self.playerCurrentPosition = [5,1]
        self.penalties=0
        self.finishPosition = [8,13]
        self.Board = [
    ['#', '#', '#', '#', '#', '#', '#', '#', '#', '#', '#', '#', '#', '#', '#'],
    ['#', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', '#'],
    ['#', ' ', '#', '#', '#', '#', ' ', '#', ' ', '#', '#', '#', ' ', ' ', '#'],
    ['#', ' ', '#', '#', '#', '#', ' ', '#', ' ', '#', '#', '#', ' ', ' ', '#'],
    ['#', ' ', '#', '#', '#', '#', '#', '#', ' ', '#', ' ', '#', ' ', ' ', '#'],
	['#', 'P', '#', '#', '#', '#', ' ', ' ', ' ', '#', ' ', '#', ' ', ' ', '#'],
    ['#', ' ', '#', '#', '#', '#', '#', '#', '#', '#', ' ', '#', '#', ' ', '#'],
    ['#', ' ', '#', '#', '#', ' ', ' ', ' ', ' ', ' ', ' ', '#', '#', ' ', '#'],
    ['#', ' ', ' ', ' ', ' ', ' ', '#', '#', '#', '#', ' ', ' ', '#', 'F', '#'],
    ['#', '#', '#', '#', '#', '#', '#', '#', '#', '#', '#', '#', '#', '#', '#']]

    def display(self,gene):
        for i in range(0,30):
            if(gene[i] == 1):
                self.moveUp()
            elif(gene[i] == 2):
                self.moveDown()
            elif(gene[i] == 3):
                self.moveRight()
            elif(gene[i] == 4):
                self.moveLeft()
            else:
                continue
        print("Player Current Position: ", self.playerCurrentPosition[0],", ",self.playerCurrentPosition[1],"\n")
        for j in range(0,10):
            print(self.Board[j])
        self.resetPlayer()


    def moveRight(self):
        priv2 = self.playerCurrentPosition[1] + 1
        priv1 = self.playerCurrentPosition[0]
        self.movePlayerAndUpdateBoard(priv1,priv2)


    def moveLeft(self):
        priv2 = self.playerCurrentPosition[1] - 1
        priv1 = self.playerCurrentPosition[0]
        self.movePlayerAndUpdateBoard(priv1,priv2)


    def moveUp(self):
        priv2 = self.playerCurrentPosition[1]
        priv1 = self.playerCurrentPosition[0]- 1
        self.movePlayerAndUpdateBoard(priv1,priv2)


    def moveDown(self):
        priv2 = self.playerCurrentPosition[1]
        priv1 = self.playerCurrentPosition[0] + 1
        self.movePlayerAndUpdateBoard(priv1,priv2)

    def isWall(self,x,y):
        if((x>=0 and x<10) and (y>=0 and y<15)):
            return self.Board[x][y] == self.WALL;

    def isFinished(self,x,y):
        if((x>=0 and x<10) and (y>=0 and y<15)):
            return self.Board[x][y]== self.FINISH

    def isFloor(self,x,y):
        if((x>=0 and x<10) and (y>=0 and y<15)):
            return self.Board[x][y] == self.FLOOR

    def movePlayerAndUpdateBoard(self,x,y):
        if(self.isWall(x,y)):
            self.penalties = self.penalties + 1
            self.Board[self.finishPosition[0]][self.finishPosition[1]] = self.FINISH
            self.Board[self.playerCurrentPosition[0]][self.playerCurrentPosition[1]] = self.PLAYER
        elif(self.isFloor(x,y)):
            self.Board[self.playerCurrentPosition[0]][self.playerCurrentPosition[1]] = self.FLOOR
            self.Board[x][y] = self.PLAYER
            self.playerCurrentPosition[0] = x
            self.playerCurrentPosition[1] = y
            self.Board[self.finishPosition[0]][self.finishPosition[1]] = self.FINISH
        elif(self.isFinished(x,y)):
            self.Board[self.playerCurrentPosition[0]][self.playerCurrentPosition[1]] = self.FLOOR
            self.Board[x][y] = self.PLAYER
            self.playerCurrentPosition[0] = x
            self.playerCurrentPosition[1] = y
            print("Found exit, we finished, now we are on the position ( ",x,", ",y,")")
            self.penalties = 0


    def resetPlayer(self):
        if (self.playerCurrentPosition[0]!=5 or self.playerCurrentPosition[1]!=1):
            self.movePlayerAndUpdateBoard(5,1)
        self.Board[8][13] = self.FINISH
        self.penalties=0

class Chromosome:

    def __init__(self, gene):
        maze = Maze()
        self.gene = gene
        self.maze = maze
        self.fitness = Chromosome._update_fitness(gene,maze)


    def mate(self, mate):
        """
        Method used to mate the chromosome with another chromosome,
        resulting in a new chromosome being returned.
        """

        """pivot = randint(0, len(self.gene) - 1)

        gene1 = self.gene[:pivot] + mate.gene[pivot:]
        gene2 = mate.gene[:pivot] + self.gene[pivot:]

        return Chromosome(gene1), Chromosome(gene2)"""

        pivot = randint(0, len(self.gene) - 1)
        while(pivot==0):
            pivot = randint(0,len(self.gene) - 1)
        splitFirstHalf = randint(0,pivot-1)
        splitSecondHalf = randint(pivot,len(self.gene) - 1)
        gene1 = self.gene[:splitFirstHalf] + mate.gene[splitFirstHalf:pivot] + self.gene[pivot:splitSecondHalf] + mate.gene[splitSecondHalf:]
        gene2 = mate.gene[:splitFirstHalf] + self.gene[splitFirstHalf:pivot] + mate.gene[pivot:splitSecondHalf] + self.gene[splitSecondHalf:]

        return Chromosome(gene1), Chromosome(gene2)

    def mutate(self):
        """
        Method used to generate a new chromosome based on a change in a
        random character in the gene of this chromosome.  A new chromosome
        will be created, but this original will not be affected.
        """
        gene = list(self.gene)
        delta = randint(1, 4)
        idx = randint(0, len(gene) - 1)
        gene[idx] = delta

        return Chromosome(gene)

    def _update_fitness(gene,maze):
        """
        Helper method used to return the fitness for the chromosome based
        on its gene.
        """

        fitness = 0
        for i in range(0,30):
            if(gene[i] == 1):
                maze.moveUp()
            elif(gene[i] == 2):
                maze.moveDown()
            elif(gene[i] == 3):
                maze.moveRight()
            elif(gene[i] == 4):
                maze.moveLeft()
            else:
                continue

        fitness = abs(maze.finishPosition[0] - maze.playerCurrentPosition[0]) + abs(maze.finishPosition[1] - maze.playerCurrentPosition[1]) + maze.penalties;

        maze.resetPlayer()

        return fitness

    @staticmethod
    def gen_random():
        """
        A convenience method for generating a random chromosome with a random
        gene.
        """
        gene = []
        for x in range(30):
            gene.append(randint(1, 4))

        return Chromosome(gene)

class Population:

    _tournamentSize = 3

    def __init__(self, size=20000, crossover=0.8, elitism=0.1, mutation=0.03):
        self.elitism = elitism
        self.mutation = mutation
        self.crossover = crossover
        self.size = size

        buf = []
        for i in range(size): buf.append(Chromosome.gen_random())
        self.population = list(sorted(buf, key=lambda x: x.fitness))

    def _tournament_selection(self):
        """
        A helper method used to select a random chromosome from the
        population using a tournament selection algorithm.
        """
        genIdx = randint(0, int(round(self.elitism*(len(self.population) - 1))))

        """best = choice(self.population)"""
        best = self.population[genIdx]
        for i in range(Population._tournamentSize):
            """cont = choice(self.population)"""
            genIdx2 = randint(0, int(round(self.elitism*(len(self.population) - 1))))
            cont = self.population[genIdx2]
            if (cont.fitness < best.fitness): best = cont

        return best

    def _selectParents(self):
        """
        A helper method used to select two parents from the population using a
        tournament selection algorithm.
        """

        return (self._tournament_selection(), self._tournament_selection())

    def evolve(self):
        """
        Method to evolve the population of chromosomes.
        """
        size = len(self.population)
        idx = int(round(size * self.elitism))
        buf = self.population[:idx]

        while (idx < size):
            if (random() <= self.crossover):
                (p1, p2) = self._selectParents()
                children = p1.mate(p2)
                for c in children:
                    if random() <= self.mutation:
                        buf.append(c.mutate())
                    else:
                        buf.append(c)
                idx += 2
            else:
                if random() <= self.mutation:
                    buf.append(self.population[idx].mutate())
                else:
                    buf.append(self.population[idx])
                idx += 1

        self.population = list(sorted(buf[:size],key=lambda x: x.fitness))

if __name__ == "__main__":
    maxGenerations = 200
    pop = Population(size=200000, crossover=0.8, elitism=0.001, mutation=0.3)

    """for i in range(1, maxGenerations + 1):

        print("\nGeneration %d: %s" % (i, pop.population[0].gene))
        print("Best fitness is: ", pop.population[0].fitness)
        pop.population[0].maze.display()
        print("Worst fitness is:",pop.population[19999].fitness)

        if(pop.population[0].fitness == pop.population[19999]):
            pop.mutation = 0.3
        for j in range(0,len(pop.population)):
                    pop.population[j].maze.resetPlayer()
        if pop.population[0].fitness == 0: break
        else:pop.evolve()
    else:
        print("Maximum generations reached without success.")
        """
    i = 1
    while(1):
        print("\nGeneration: ",i)
        pop.population[0].maze.display(pop.population[0].gene)
        print("Best Fitness: ",pop.population[0].fitness)
        print("Worst Fitness: ",pop.population[len(pop.population) - 1].fitness)
        print("Gene: ", pop.population[0].gene)
        if (pop.population[0].fitness <= 2): break
        else:
            pop.evolve()
            i = i + 1