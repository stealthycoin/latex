import random,sys,re,pickle,getopt,math

POPULATION = 1000
TOURNAMENT = 20
CROSSOVER = 5
MUTATION = .2
PROBABILITY = .75
NGRAMS = 3
CAP = 101

trainingData = {}
sys.setrecursionlimit(2000)

class Individual:
    """An individual is a key with some added functions to deal with genetic training"""    
    def decrypt(self, ciphertext):
        """Takes a ciphertext and returns a potential plaintext"""
        plaintext = ""
        for letter in ciphertext:
            if re.match('[A-Z]', letter):
                plaintext += self.key[ord(letter)-65] #ascii man      
            else:
                plaintext += letter

        return plaintext

    def setFitness(self,fitness):
        """Sets the fitness of the chromsome"""
        self.fitness = fitness

    def __init__(self, key):
        self.key = key
        self.fitness = None

    def __str__(self):
        return self.key + ": " + str(self.fitness)

def superLeetWrite(string):
    """Formats in blocks of 5 characters"""
    spaces = 0
    result = ""
    for i in range(len(string)):
        result += string[i]
        if (i+1) % 5 == 0:
            if spaces == 12:
                spaces = 0
                result += "\n"
            else:
                spaces += 1
                result += " "

    return result
                
def randomKey():
    """Generates a random key"""
    sigma = bytearray("ABCDEFGHIJKLMNOPQRSTUVWXYZ")
    random.shuffle(sigma)
    return str(sigma)
    
def generatePopulation():
    """Fills a population array with Individual instances"""
    pop = []
    for x in range(POPULATION):
        pop.append(Individual(randomKey()))
    return pop


def ngrams(text, n):
    """Takes in a text and returns the ngram frequencies"""
    pivot1 = 0
    pivot2 = n
    
    ngramsD = {}
    total = 0

    while pivot2 < len(text):
        ngram = text[pivot1:pivot2]
        try:
            ngramsD[ngram] += 1
        except KeyError:
            ngramsD[ngram] = 1
        pivot1 += 1
        pivot2 += 1
        total += 1
        
    return ngramsD
    

def fitness(plaintext, T):
    """Takes in a plaintext and returns a fitness score for it"""
    F = ngrams(plaintext, NGRAMS)
    
    fitness = 0
    for x in iter(F):
        try:
            fitness += F[x] * math.log(T[x],2)
        except KeyError:
            pass #trigram did not appear in english... so clearly no increase in fitness

    return fitness

def train(trainingset):
    """calculate ngrams and save it for later"""
    probs = ngrams(trainingset,NGRAMS) 
    with open('training.pkl','wb') as f:
        pickle.dump(probs,f, pickle.HIGHEST_PROTOCOL) #write as a binary file

def cross(a,b):
    """Crosses a and b returning a tuple of their children"""
    #crossover points
    choices = [x for x in range(26)]
    points = []

    indicies = random.sample(choices,CROSSOVER)
    result = bytearray(" " * 26)

    for i in indicies:
        result[i] = a.key[i]

    j = 0
    try:
        for i in range(len(result)):
            while b.key[j] in result:
                j += 1 # we already have this letter move along
            if result[i] ==  32:
                result[i] = b.key[j] #if we have a blank fill it in
    except IndexError:
        pass #my lazy way of bounds checking
        
    return Individual(str(result))
        
    
def mutate(child):
    """Mutations!!!"""
    if random.random() < MUTATION:
        i2 = i1 = random.randint(0,len(child.key)-1)
        while i2 == i1:
            i2 = random.randint(0,len(child.key)-1)

        a = bytearray(child.key)
        a[i1],a[i2] = a[i2],a[i1]
        return Individual(str(a))
    return child

def breed(parenta, parentb):
    """Two parents breed to make two children"""
    childa = cross(parenta,parentb)    
    childb = cross(parentb,parenta)    

    childa = mutate(childa)
    childb = mutate(childb)

    return [childa,childb]

def runTournament(pop):
    """Run a tournament on the pop with size size and prob as the probability of most fit individual winning"""

    tournament = random.sample(pop,TOURNAMENT)

    #select winner
    tournament = sorted(tournament, key=lambda x: x.fitness, reverse=True)
    
    # winning chances p, p(1-p), p(1-p)^2 ...
    r = random.random()
    mark = PROBABILITY
    i = 0
    while r > mark and i < TOURNAMENT - 1:
        mark *= (1 - PROBABILITY)
        i += 1

    return tournament[i]
    

def iterate(population, ciphertext, g):
    """one generation -> second generation"""

    if g == CAP: #limit to 10 generations atm
        return

    #loop through all chromosomes decrypting the text with them
    #then excitingly enough we score them and attach the score to
    #each chromosome. Throw out the plaintext so we don't have to keep it around in mem

    for chrom in population:
        plaintext = chrom.decrypt(ciphertext)
        chrom.setFitness(fitness(plaintext,trainingData))

    #selection of fitmost individuals
    #sort population based on fitness
    population = sorted(population, key=lambda x: x.fitness, reverse=True)
    
    nextGen = []

    #elitism (top 15%)
    cutoff = int(len(population)*.15)
    nextGen += population[:cutoff]

    while len(nextGen) < len(population):
        #parent a and parent b
        pa, pb = runTournament(population), runTournament(population) #would be nice if I knew how to parallelize this
        nextGen += breed(pa,pb) #each pair makes two children    

    while len(nextGen) > len(population):
        nextGen = nextGen[:-2]
    

    print "Geneation %d best individual: %f" % (g,population[0].fitness)

    with open('gen%d'%g, 'w') as f:
        strong = population[:10]
        for chrom in strong:
            f.write(str(chrom))
            f.write('\n')
            f.write(superLeetWrite(chrom.decrypt(ciphertext)))
            f.write("\n\n")


    iterate(nextGen, ciphertext, g+1)


def decrypt(ciphertext):
    """Runs the GA to try and decrypt the ciphertext"""
    #load training data
    global trainingData
    with open('training.pkl', 'r') as f:
        trainingData = pickle.load(f)
    #start simulations
    population = generatePopulation()
    iterate(population, ciphertext, 1)

def main():
    """Assumes the ciphertext is in a file passed as an argument"""
    #are we training or not?
    opts, args = getopt.getopt(sys.argv[1:], "tk:")
    flags = [o for o,a in opts]

    #we always need a file, what its for is unknown
    filename = args[0] #firsts thing is filename always because I am lazy
    with open(filename, 'r') as f:
        d = f.read()
        data = re.sub('[^A-Z]','',d.upper()) #always need to remove all the bullshit
        
    if '-t' in flags:
        #we are training
        train(data)
    elif '-k' in flags:
        #known key
        print Individual(opts[0][1]).decrypt(d.upper())

    else:
        #decrypting not training
        decrypt(data)
    
if __name__ =='__main__':
    main()
