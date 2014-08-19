#include "bc246t.h"

void SPI_init() {
  DDRB  &= ~DI;
  DDRB  |=  CS + DO + SCK;
  PORTB |=  DI;
}

unsigned char SPI_transfer(unsigned char ch) {
  USIDR = ch;
  USISR = (1 << USIOIF);
  
  do {
    USICR = (1 << USIWM0) | (1 << USICS1) | 
            (1 << USICLK) | (1 << USITC)  ;
    _delay_us(100);
  } while (!(USISR & (1 << USIOIF)));
  
  return USIDR;
}
