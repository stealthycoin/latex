#
# Makefile for Rijndael (AES) code.
#
# $Id: Makefile,v 1.1 2005/01/28 21:50:14 elm Exp $
# NOTE: has GNU make specific stuff

SRCS = encrypt.c decrypt.c jcdecrypt.c rijndael.c
INCS = rijndael.h
PROGS = decrypt encrypt jcdecrypt
OTHERS = testfile Makefile
DIR = $(notdir $(PWD))
TAR = tar
TARFILE = aes.tgz

COBJS = rijndael.o
CFLAGS = -O3 -g

all: $(PROGS)
#added this
jcdecrypt: jcdecrypt.o $(OBJS) $(INCS)
	$(CC) $(CFLAGS) -o $@ jcdecrypt.o $(COBJS)

encrypt: encrypt.o $(COBJS) $(INCS)
	$(CC) $(CFLAGS) -o $@ encrypt.o $(COBJS)

decrypt: decrypt.o $(COBJS) $(INCS)
	$(CC) $(CFLAGS) -o $@ decrypt.o $(COBJS)

# NOTE: bruteforce is not distributed with the problem set, but you're
#       probably going to want to write it....
bruteforce: bruteforce.o  $(OBJS) $(INCS)
	$(CC) $(CFLAGS) -o $@ bruteforce.o $(OBJS)

rijndael.o: rijndael.h

tarball:
	cd .. ; $(TAR) cvf - $(addprefix $(DIR)/, $(SRCS) $(INCS) $(OTHERS)) | gzip - > $(TARFILE)

test: all
	@echo "NOTE: a difference in the last line is probably OK---It's"
	@echo "      due to padding the last block encrypted."
	@echo
	./encrypt abcd - < testfile | ./decrypt abcd - | diff - testfile
	./encrypt 123456 - < testfile | ./decrypt 123456 - | diff - testfile
	./encrypt 98765432 - < testfile | ./decrypt 98765432 - | diff - testfile

clean:
	$(RM) *~ *.o

spotless: clean
	$(RM) $(PROGS)
