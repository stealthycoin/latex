import cPickle as pickle
import hashlib   #free bulitin sha1 from python. Woo.
m = hashlib.sha1()

hashes = {}

#generate hash for legit message
# I James Smith authorize the sale of 1800 West Cliff Drive in Santa Cruz to John Carlyle for 1.5 million dollars on Febuary 2-8 2014.
cmps = [["I", ""],
        ["J", "james", "James", "mr", "Mr", "mr.", "Mr."] ,
        ["smith", "Smith",],
        ["authorize", "agree to", "endorse"],
        ["the sale"],
        ["of"],
        ["1800 West Cliff", "1800 west cliff", "1800 West cliff", "1800 west Cliff"],
        ["Drive", "Dr.", "dr.", "Dr", "dr"],
        ["in"],
        ["Santa Cruz", "S.C.", "Santa Cruz California"],
        ["to"],
        ["John Carlyle", "John William Carlyle", "J Carlyle", "J W Carlyle", "J. W. Carlyle", "John W. Carlyle", "John W Carlyle"],
        ["for"],
        ["1.5 Million dollars", "one million fivehundred thousand dollars", "1.5 million dollars", "$1.5 million", "$1.5 Million"],
        ["on"],
        ["Feb.", "Febuary", "Feb"],
        ["2","3","4","5","6","7","8"],
        ["2014"]]


#This is my worst crime. Including the programs I wrote in 7th grade.
for a in cmps[0]:
    for b in cmps[1]:
        for c in cmps[2]:
            for d in cmps[3]:
                for e in cmps[4]:
                    for f in cmps[5]:
                        for g in cmps[6]:
                            for h in cmps[7]:
                                for i in cmps[8]:
                                    for j in cmps[9]:
                                        for k in cmps[10]:
                                            for l in cmps[11]:
                                                for m in cmps[12]:
                                                    for n in cmps[13]:
                                                        for o in cmps[14]:
                                                            for p in cmps[15]:
                                                                for q in cmps[16]:
                                                                    for r in cmps[17]:
                                                                        msg = "%s %s %s %s %s %s %s %s %s %s %s %s %s %s %s %s %s %s" % (a,b,c,d,e,f,g,h,i,j,k,l,m,n,o,p,q,r)
                                                                        hashes[hashlib.sha1(msg).hexdigest()[-10:]] = msg


pickle.dump(hashes, open('save.p', 'wb'))
