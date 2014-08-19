#include "bc246t.h"

int main() {
  char ret;

  USART_init(51);

  USART_printstr("\r\n");
  USART_println("Initializing");
  USART_printstr(" SPI...");
  SPI_init();
  USART_println("done");

  USART_printstr(" SD...");
  if ((ret = SD_init())) {
    USART_printstr("error: ");
    USART_printhex(ret);
    USART_printstr("\r\n");
    return -1;
  }
  USART_println("done");

  USART_printstr(" FAT16...");
  if ((ret = FAT16_init())) {
    USART_printstr("error: ");
    USART_printhex(ret);
    USART_printstr("\r\n");
    return -1;
  }
  USART_println("done");

  return 0;
}
