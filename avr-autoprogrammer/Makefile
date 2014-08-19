TARGET=bc246t
SRC=$(TARGET).o spi.o fat16.o

PRG_DEV=/dev/ttyS0
PRG_TYPE=usbasp
CFLAGS=-g -Wall -Os -Werror -Wextra -mmcu=attiny2313

$(TARGET).elf: $(SRC)
	avr-gcc $(CFLAGS) *.o -o $@	

flash: $(TARGET).flash

%.flash: %.hex
	avrdude -P $(PRG_DEV) -c $(PRG_TYPE) -p t2313 -v -e -U flash:w:$*.hex

%.hex: %.elf
	avr-objcopy -j .text -j .data -O ihex $< $@

%.o: %.c
	avr-gcc $(CFLAGS) -Wa,-ahlmns=$(TARGET).lst -c $< -o $@

clean:
	rm -f *.hex *.obj *.o *.lst *.elf
