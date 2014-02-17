#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <stdint.h>
#include "rijndael.h"

#define KEYBITS 128
#define THRESHHOLD 15

//turn a digit into a hex character
char hexify(int d) {
  if(d < 10) {
    return '0' + d; 
  }
  else if (d < 16) {
    return 'A' + d - 10;
  }
  fprintf(stderr, "You done mathed wrong son.\n");
  exit(1);
}


//I spent many hours on sunday reading about ways to memory effeciently implement bit vectors in c
//in the end I gave up and just did char* (which the internet told me was bad)
//and due to my decision i have to have this horrible function
void keyBits(int intKey, unsigned char *realKey) {
  //we only want 30 bits
  int k = intKey << 2;
  
  int i;
  for (i = 0 ; i < 4; i++) {
    realKey[i] = (k >> (24 - (i * 8))) & 0x000000FF; //really clear
  }
}

//does the inverse of what is in the decrypt file (3 shots of whiskey required)
void keypass(char *key, char *password, int len) {
  int i;
  for(i = 0; i < len; i++) {
    password[2*i]   = hexify((key[i] >> 4) & 0x0000000F);
    password[2*i+1] = hexify(key[i] & 0x0000000F);
  }
}


//initially this was made to figure out if it a compressed file
//was looking at only the first 16 bits for 1f 8b
//still valid since I can look for ascii
//much of this code is taken or based off decrypt.c
int main(int argc, char **argv) {
  unsigned long rk[RKLENGTH(KEYBITS)];
  unsigned char ct[16];
  unsigned char pt[17];//+1 for \0 since we need to print it
  int nrounds;
  FILE* input;

  unsigned char key[KEYLENGTH(KEYBITS)];
  unsigned char password[4*KEYLENGTH(KEYBITS)];
  unsigned int candidateKey = 0;

  //init key stuff
  int i;
  for (i = 0 ; i < 4*KEYLENGTH(KEYBITS) ; i++) {
    password[i] = 0;
    if (i < KEYLENGTH(KEYBITS)) {
      key[i] = 0;
    }
  }


  //read file supplied (lifted from decrypt.c)
  input = fopen(argv[1], "rb");
  if (input == NULL) {
    fputs("File read error", stderr);
    return 1;
  }

  //try reading the beginning of the ciphertext
  if (fread(ct, sizeof ct, 1, input) != 1) {
    fprintf(stderr, "Read failed\n");
    return 1;
  }

  //prepare ciphretext and iv (from decrypt.c)
  for (i = 0 ; i < sizeof ct ; i++) {
    pt[i] = 0;
  }
  pt[17] = '\0';
  //since you made it 30 bits like a nice teacher an unsigned int should be large enough to hold the counter
  unsigned int count = 0; 
  //30 bits
  while (candidateKey < 0x3FFFFFFF) {
    count++;
    //keep on generating passwords and trying them
    if (count % 4473924 == 0) {
      keypass(key, password, KEYLENGTH(KEYBITS));
      printf("key %s\n", password);
    }
    keyBits(candidateKey++, key);
    nrounds = rijndaelSetupDecrypt(rk, key, KEYBITS);
    rijndaelDecrypt(rk, nrounds, ct, pt);


    //try and detect some ascii in the generated plaintext
    int ascii = 0;
    for (i = 0 ; i < 16 ; i++) {
      char c = pt[i];
      //A-z covers most ascii we would expect to see in text plus a couple others I think would be common
      if ( (c >= 'A' && c <= 'z') || c == ' ' || c == '.' || c == ',') {
	ascii++;
      }
    }
    if (ascii > THRESHHOLD) {
      printf("\tPlaintext exeeds threshold: %s\n", pt);
      //need to give password to work with decrypt
      keypass(key, password, KEYLENGTH(KEYBITS));
      printf("\tPassword: %s\n", password);
    }
    
  }

  return 0;
}

