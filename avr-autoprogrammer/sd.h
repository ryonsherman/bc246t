#ifndef __SD_H
#define __SD_H

unsigned char SD_command(unsigned char cmd, unsigned long arg,
                         unsigned char crc, unsigned char read);
char SD_init(void);

#endif
