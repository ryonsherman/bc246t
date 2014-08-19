#include "main.h"

void USART_init(unsigned int ubrr) {
  UBRRH = (unsigned char) (ubrr >> 8);
  UBRRL = (unsigned char) (ubrr & 255);
  UCSRC = (1 << UCSZ1) | (1 << UCSZ0);
  UCSRB = (1 << RXEN)  | (1 << TXEN);
}

void USART_printch(char ch) {
  while (!(UCSRA & (1 << UDRE))) {}
  UDR=ch;
}

void __USART_printhex(unsigned char n) {
  if (((n >> 4) & 15) < 10)
    USART_printch('0' + ((n >> 4) & 15));
  else
    USART_printch('A' + ((n >> 4) & 15) - 10);
}

void USART_printhex(unsigned char n) {
  __USART_printhex(n);
  __USART_printhex(n << 4);
}

void USART_printstr(char *str) {
  while (*str) USART_printch(*str++);
}

void USART_println(char *str) {
  USART_printstr(str);
  USART_printstr("\r\n");
}
