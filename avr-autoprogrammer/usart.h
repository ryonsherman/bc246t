#ifndef __USART_H
#define __USART_H

void USART_init(unsigned int ubrr);
void USART_printch(char ch);
void __USART_printhex(unsigned char n);
void USART_printhex(unsigned char n);
void USART_printstr(char *str);
void USART_println(char *str);

#endif
