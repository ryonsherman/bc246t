#include "bc246t.h"

void USART_init(unsigned int ubrr) {
  UBRRH = (unsigned char) (ubrr >> 8);
  UBRRL = (unsigned char) (ubrr & 255);
  UCSRC = (1 << UCSZ1) | (1 << UCSZ0);
  UCSRB = (1 << RXEN)  | (1 << TXEN);
}

void printch(char ch) {
  while (!(UCSRA & (1 << UDRE))) {}
  UDR=ch;
}

void printhex(unsigned char n) {
  if (((n >> 4) & 15) < 10)
    printch('0' + ((n >> 4) & 15));
  else
    printch('A' + ((n >> 4) & 15) - 10);
  n <<= 4;
  if (((n >> 4) & 15) < 10)
    printch('0' + ((n >> 4) & 15));
  else
    printch('A' + ((n >> 4) & 15) - 10);
}

void print(char *str) {
  int i;
  for (i = 0; str[i]; i++)
    printch(str[i]);
}

void println(char *str) {
  print(str);
  print("\r\n");
}

unsigned char SD_command(unsigned char cmd, unsigned long arg,
                         unsigned char crc, unsigned char read) {
  unsigned char i, buffer[8], ret = 0xFF;

  print("CMD ");
  printhex(cmd);

  CS_ENABLE();

  SPI_transfer(cmd);
  SPI_transfer(arg >> 24);
  SPI_transfer(arg >> 16);
  SPI_transfer(arg >> 8);
  SPI_transfer(arg);
  SPI_transfer(crc);

  for (i = 0; i < read; i++)
    buffer[i] = SPI_transfer(0xFF);

  CS_DISABLE();  

  for (i = 0; i < read; i++) {
    printch(' ');
    printhex(buffer[i]);
    if (buffer[i] != 0xFF)
      ret = buffer[i];
  }

  println("");

  return ret;
}

char SD_init() {
  char i;

  CS_DISABLE();
  
  for (i = 0; i < 10; i++)    
    SPI_transfer(0xFF);

  for (i = 0; i < 10 && SD_command(0x40, 0x00000000, 0x95, 8) != 1; i++)
    _delay_ms(100);
  if (i == 10) return -1;

  for (i = 0; i < 10 && SD_command(0x41, 0x00000000, 0xFF, 8) != 0; i++)
    _delay_ms(100);
  if (i == 10) return -2;

  SD_command(0x50, 0x00000200, 0xFF, 8);

  return 0;
}


int main() {
  char ret;

  USART_init(51);

  println("");
  println("Initializing SPI...");
  SPI_init();
  
  println("Initializing SD...");
  if ((ret = SD_init())) {
    print("SD error: ");
    printhex(ret);
    println("");
    return -1;
  }

  println("Initializing FAT16...");
  if ((ret = FAT16_init())) {
    print("FAT16 error: ");
    printhex(ret);
    println("");
    return -1;
  }

  return 0;
}
