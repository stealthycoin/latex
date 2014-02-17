import getopt,sys,re
from ga-2 import *

def analyzeSlice(size, datum):
    """calculate coincidence index"""
    cols = []
    for i in range(size):
        col = ""
        while i < len(datum):
            col += datum[i]
            i += size
        cols.append(col)

    for col in cols:
        n = len(col)
        numerator = 0
        freq = {}
        for l in col:
            try: 
                freq[l] += 1
            except KeyError:
                freq[l] = 1
        for l in "ABCDEFGHIJKLMNOPQRSTUVWXYZ":
            try:
                numerator += freq[l] * (freq[l] - 1)
            except KeyError:
                pass #wasnt in the string so just ignore it
        denominator = n * (n + 1) / 26.0

    return float(numerator) / denominator
    

def keyLength(filename, keyrange):
    """try and find the key length using the magic of statistics"""
    with open(filename) as f:
        data = f.read()
    
    data = re.sub('[^A-Z]','',data.upper())

    beg, end = keyrange.split(":")

    results = []
    for i in range(int(beg),int(end)):
        results.append((i,analyzeSlice(i, data)))

    results = sorted(results, key=lambda x: x[1], reverse=True)
    for result in results:
        print result
                       

def sovle(filename, keylength):
    """Try keys with given length and evolve a correct one"""
    

def main():
    """Main function. What do you want from me?"""
    opts, args = getopt.getopt(sys.argv[1:], "k:l")
    flags = [o for o,a in opts]
    
    filename = args[0]

    if "-k" in flags:
        #find key length
        keyLength(filename, opts[0][1])
    elif "-l" in flags:
        #we know the key length
        solve(filename, int(opts[0][1]))
        

if __name__ == '__main__':
    main()
