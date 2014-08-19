#include "bc246t.h"

unsigned char SD_command(unsigned char cmd, unsigned long arg,
                         unsigned char crc, unsigned char read) {
  unsigned char i, buffer[8], ret = 0xFF;

  #ifdef DEBUG
    USART_printstr(" CMD ");
    USART_printhex(cmd);
  #endif

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
    #ifdef DEBUG
      USART_printch(' ');
      USART_printhex(buffer[i]);
    #endif

    if (buffer[i] != 0xFF)
      ret = buffer[i];
  }

  #ifdef DEBUG
    USART_printstr("\r\n");
  #endif

  return ret;
}

char SD_init() {
  char i;

  CS_DISABLE();
  
  for (i = 0; i < 10; i++)    
    SPI_transfer(0xFF);

  #ifdef DEBUG
    USART_printstr("\r\n");
  #endif
  for (i = 0; i < 10 && SD_command(0x40, 0x00000000, 0x95, 8) != 1; i++) {
    #ifndef DEBUG
      USART_printch('.');
      _delay_ms(100);
    #endif    
  }
  if (i == 10) return -1;

  for (i = 0; i < 10 && SD_command(0x41, 0x00000000, 0xFF, 8) != 0; i++)
    _delay_ms(100);
  if (i == 10) return -2;

  SD_command(0x50, 0x00000200, 0xFF, 8);

  return 0;
}
