#define F_CPU 8000000UL

#include <avr/io.h>
#include <util/delay.h>

#define CS  (1 << PB4)
#define DI  (1 << PB5)
#define DO  (1 << PB6)
#define SCK (1 << PB7)

#define CS_ENABLE()  (PORTB &= ~CS)
#define CS_DISABLE() (PORTB |=  CS)

#include "usart.h"
#include "spi.h"
#include "sd.h"
#include "fat16.h"
