# Raport optymalizacji energetycznej

## Projekt: /home/tom/github/infrash/embedded/examples/../../../zlecenia/maski/Programator_2025

**Znalezione problemy:** 235
**Zmodyfikowane pliki:** 17
**Dodane komentarze:** 36

## Podsumowanie według typu problemu

| Typ problemu | Liczba wystąpień | Średni wpływ | Średni potencjalny zysk |
|--------------|-----------------|-------------|-------------------------|
| peripheral_not_disabled | 149 | 0.70 | 0.05 |
| inefficient_loop | 38 | 0.60 | 0.03 |
| unnecessary_loop_operations | 20 | 0.70 | 0.02 |
| busy_wait_pattern | 8 | 0.75 | 0.15 |
| unused_clocks_enabled | 6 | 0.60 | 0.10 |
| suboptimal_adc_pattern | 5 | 0.45 | 0.03 |
| unused_clock_pattern | 4 | 0.60 | 0.10 |
| high_frequency_pattern | 2 | 0.60 | 0.20 |
| incomplete_port_config | 1 | 0.40 | 0.01 |
| unconfigured_pins_pattern | 1 | 0.40 | 0.01 |
| delay_loop_pattern | 1 | 0.65 | 0.08 |

## Szczegóły według plików

### /home/tom/github/zlecenia/maski/Programator_2025/TMC_V200/main.c

| Linia | Typ problemu | Opis | Sugestia | Wpływ | Zysk |
|-------|-------------|------|----------|-------|------|
| 38 | peripheral_not_disabled | Timer peripheral may not be properly disabled when not in use | Ensure Timer is properly disabled when not needed to save power | 0.70 | 0.05 |
| 59 | peripheral_not_disabled | Timer peripheral may not be properly disabled when not in use | Ensure Timer is properly disabled when not needed to save power | 0.70 | 0.05 |
| 61 | peripheral_not_disabled | Timer peripheral may not be properly disabled when not in use | Ensure Timer is properly disabled when not needed to save power | 0.70 | 0.05 |
| 66 | peripheral_not_disabled | Timer peripheral may not be properly disabled when not in use | Ensure Timer is properly disabled when not needed to save power | 0.70 | 0.05 |
| 67 | peripheral_not_disabled | Timer peripheral may not be properly disabled when not in use | Ensure Timer is properly disabled when not needed to save power | 0.70 | 0.05 |
| 192 | inefficient_loop | Inefficient loop pattern detected - function calls or complex calculations in loop condition | Move function calls and calculations outside the loop or use simpler conditions | 0.60 | 0.03 |
| 232 | peripheral_not_disabled | Timer peripheral may not be properly disabled when not in use | Ensure Timer is properly disabled when not needed to save power | 0.70 | 0.05 |
| 270 | inefficient_loop | Inefficient loop pattern detected - function calls or complex calculations in loop condition | Move function calls and calculations outside the loop or use simpler conditions | 0.60 | 0.03 |
| 291 | unnecessary_loop_operations | Loop may contain operations that could be moved outside the loop | Identify and move loop-invariant operations outside the loop | 0.70 | 0.02 |
| 291 | inefficient_loop | Inefficient loop pattern detected - function calls or complex calculations in loop condition | Move function calls and calculations outside the loop or use simpler conditions | 0.60 | 0.03 |
| 319 | inefficient_loop | Inefficient loop pattern detected - function calls or complex calculations in loop condition | Move function calls and calculations outside the loop or use simpler conditions | 0.60 | 0.03 |
| 376 | peripheral_not_disabled | Timer peripheral may not be properly disabled when not in use | Ensure Timer is properly disabled when not needed to save power | 0.70 | 0.05 |
| 377 | peripheral_not_disabled | Timer peripheral may not be properly disabled when not in use | Ensure Timer is properly disabled when not needed to save power | 0.70 | 0.05 |
| 378 | peripheral_not_disabled | Timer peripheral may not be properly disabled when not in use | Ensure Timer is properly disabled when not needed to save power | 0.70 | 0.05 |
| 380 | peripheral_not_disabled | Timer peripheral may not be properly disabled when not in use | Ensure Timer is properly disabled when not needed to save power | 0.70 | 0.05 |
| 383 | peripheral_not_disabled | Timer peripheral may not be properly disabled when not in use | Ensure Timer is properly disabled when not needed to save power | 0.70 | 0.05 |
| 386 | peripheral_not_disabled | Timer peripheral may not be properly disabled when not in use | Ensure Timer is properly disabled when not needed to save power | 0.70 | 0.05 |
| 389 | peripheral_not_disabled | Timer peripheral may not be properly disabled when not in use | Ensure Timer is properly disabled when not needed to save power | 0.70 | 0.05 |
| 393 | peripheral_not_disabled | UART peripheral may not be properly disabled when not in use | Ensure UART is properly disabled when not needed to save power | 0.70 | 0.05 |
| 395 | peripheral_not_disabled | UART peripheral may not be properly disabled when not in use | Ensure UART is properly disabled when not needed to save power | 0.70 | 0.05 |
| 430 | peripheral_not_disabled | UART peripheral may not be properly disabled when not in use | Ensure UART is properly disabled when not needed to save power | 0.70 | 0.05 |
| 433 | peripheral_not_disabled | UART peripheral may not be properly disabled when not in use | Ensure UART is properly disabled when not needed to save power | 0.70 | 0.05 |
| 446 | peripheral_not_disabled | GPIO peripheral may not be properly disabled when not in use | Ensure GPIO is properly disabled when not needed to save power | 0.70 | 0.05 |
| 449 | peripheral_not_disabled | UART peripheral may not be properly disabled when not in use | Ensure UART is properly disabled when not needed to save power | 0.70 | 0.05 |
| 449 | peripheral_not_disabled | UART peripheral may not be properly disabled when not in use | Ensure UART is properly disabled when not needed to save power | 0.70 | 0.05 |

### /home/tom/github/zlecenia/maski/Programator_2025/TMC_V200/my_config.h

| Linia | Typ problemu | Opis | Sugestia | Wpływ | Zysk |
|-------|-------------|------|----------|-------|------|
| 16 | unused_clocks_enabled | Unused clocks may be enabled | Disable unused clock sources to save power | 0.60 | 0.10 |
| 19 | unused_clocks_enabled | Unused clocks may be enabled | Disable unused clock sources to save power | 0.60 | 0.10 |
| 41 | peripheral_not_disabled | SPI peripheral may not be properly disabled when not in use | Ensure SPI is properly disabled when not needed to save power | 0.70 | 0.05 |
| 45 | peripheral_not_disabled | UART peripheral may not be properly disabled when not in use | Ensure UART is properly disabled when not needed to save power | 0.70 | 0.05 |
| 48 | peripheral_not_disabled | UART peripheral may not be properly disabled when not in use | Ensure UART is properly disabled when not needed to save power | 0.70 | 0.05 |
| 49 | peripheral_not_disabled | UART peripheral may not be properly disabled when not in use | Ensure UART is properly disabled when not needed to save power | 0.70 | 0.05 |
| 51 | peripheral_not_disabled | UART peripheral may not be properly disabled when not in use | Ensure UART is properly disabled when not needed to save power | 0.70 | 0.05 |
| 52 | peripheral_not_disabled | UART peripheral may not be properly disabled when not in use | Ensure UART is properly disabled when not needed to save power | 0.70 | 0.05 |
| 58 | peripheral_not_disabled | UART peripheral may not be properly disabled when not in use | Ensure UART is properly disabled when not needed to save power | 0.70 | 0.05 |
| 59 | peripheral_not_disabled | UART peripheral may not be properly disabled when not in use | Ensure UART is properly disabled when not needed to save power | 0.70 | 0.05 |
| 65 | peripheral_not_disabled | UART peripheral may not be properly disabled when not in use | Ensure UART is properly disabled when not needed to save power | 0.70 | 0.05 |
| 66 | peripheral_not_disabled | UART peripheral may not be properly disabled when not in use | Ensure UART is properly disabled when not needed to save power | 0.70 | 0.05 |
| 71 | peripheral_not_disabled | UART peripheral may not be properly disabled when not in use | Ensure UART is properly disabled when not needed to save power | 0.70 | 0.05 |
| 72 | peripheral_not_disabled | UART peripheral may not be properly disabled when not in use | Ensure UART is properly disabled when not needed to save power | 0.70 | 0.05 |
| 73 | peripheral_not_disabled | UART peripheral may not be properly disabled when not in use | Ensure UART is properly disabled when not needed to save power | 0.70 | 0.05 |
| 74 | peripheral_not_disabled | UART peripheral may not be properly disabled when not in use | Ensure UART is properly disabled when not needed to save power | 0.70 | 0.05 |
| 75 | peripheral_not_disabled | UART peripheral may not be properly disabled when not in use | Ensure UART is properly disabled when not needed to save power | 0.70 | 0.05 |

### /home/tom/github/zlecenia/maski/Programator_2025/TMD_V100/main.c

| Linia | Typ problemu | Opis | Sugestia | Wpływ | Zysk |
|-------|-------------|------|----------|-------|------|
| 30 | peripheral_not_disabled | Timer peripheral may not be properly disabled when not in use | Ensure Timer is properly disabled when not needed to save power | 0.70 | 0.05 |
| 55 | peripheral_not_disabled | Timer peripheral may not be properly disabled when not in use | Ensure Timer is properly disabled when not needed to save power | 0.70 | 0.05 |
| 59 | peripheral_not_disabled | Timer peripheral may not be properly disabled when not in use | Ensure Timer is properly disabled when not needed to save power | 0.70 | 0.05 |
| 60 | peripheral_not_disabled | Timer peripheral may not be properly disabled when not in use | Ensure Timer is properly disabled when not needed to save power | 0.70 | 0.05 |
| 98 | unnecessary_loop_operations | Loop may contain operations that could be moved outside the loop | Identify and move loop-invariant operations outside the loop | 0.70 | 0.02 |
| 98 | inefficient_loop | Inefficient loop pattern detected - function calls or complex calculations in loop condition | Move function calls and calculations outside the loop or use simpler conditions | 0.60 | 0.03 |
| 244 | peripheral_not_disabled | UART peripheral may not be properly disabled when not in use | Ensure UART is properly disabled when not needed to save power | 0.70 | 0.05 |
| 266 | peripheral_not_disabled | UART peripheral may not be properly disabled when not in use | Ensure UART is properly disabled when not needed to save power | 0.70 | 0.05 |
| 271 | unnecessary_loop_operations | Loop may contain operations that could be moved outside the loop | Identify and move loop-invariant operations outside the loop | 0.70 | 0.02 |
| 277 | peripheral_not_disabled | UART peripheral may not be properly disabled when not in use | Ensure UART is properly disabled when not needed to save power | 0.70 | 0.05 |
| 286 | unnecessary_loop_operations | Loop may contain operations that could be moved outside the loop | Identify and move loop-invariant operations outside the loop | 0.70 | 0.02 |

### /home/tom/github/zlecenia/maski/Programator_2025/TMD_V100/my_config.h

| Linia | Typ problemu | Opis | Sugestia | Wpływ | Zysk |
|-------|-------------|------|----------|-------|------|
| 21 | peripheral_not_disabled | UART peripheral may not be properly disabled when not in use | Ensure UART is properly disabled when not needed to save power | 0.70 | 0.05 |
| 24 | peripheral_not_disabled | UART peripheral may not be properly disabled when not in use | Ensure UART is properly disabled when not needed to save power | 0.70 | 0.05 |
| 26 | peripheral_not_disabled | UART peripheral may not be properly disabled when not in use | Ensure UART is properly disabled when not needed to save power | 0.70 | 0.05 |
| 27 | peripheral_not_disabled | UART peripheral may not be properly disabled when not in use | Ensure UART is properly disabled when not needed to save power | 0.70 | 0.05 |
| 28 | peripheral_not_disabled | UART peripheral may not be properly disabled when not in use | Ensure UART is properly disabled when not needed to save power | 0.70 | 0.05 |

### /home/tom/github/zlecenia/maski/Programator_2025/lib/Boards/TMC_V200/HAL_Board.c

| Linia | Typ problemu | Opis | Sugestia | Wpływ | Zysk |
|-------|-------------|------|----------|-------|------|
| 166 | peripheral_not_disabled | Timer peripheral may not be properly disabled when not in use | Ensure Timer is properly disabled when not needed to save power | 0.70 | 0.05 |
| 170 | peripheral_not_disabled | Timer peripheral may not be properly disabled when not in use | Ensure Timer is properly disabled when not needed to save power | 0.70 | 0.05 |
| 202 | peripheral_not_disabled | Timer peripheral may not be properly disabled when not in use | Ensure Timer is properly disabled when not needed to save power | 0.70 | 0.05 |
| 208 | peripheral_not_disabled | Timer peripheral may not be properly disabled when not in use | Ensure Timer is properly disabled when not needed to save power | 0.70 | 0.05 |
| 209 | peripheral_not_disabled | Timer peripheral may not be properly disabled when not in use | Ensure Timer is properly disabled when not needed to save power | 0.70 | 0.05 |
| 213 | peripheral_not_disabled | Timer peripheral may not be properly disabled when not in use | Ensure Timer is properly disabled when not needed to save power | 0.70 | 0.05 |
| 223 | peripheral_not_disabled | Timer peripheral may not be properly disabled when not in use | Ensure Timer is properly disabled when not needed to save power | 0.70 | 0.05 |
| 224 | peripheral_not_disabled | Timer peripheral may not be properly disabled when not in use | Ensure Timer is properly disabled when not needed to save power | 0.70 | 0.05 |
| 262 | peripheral_not_disabled | GPIO peripheral may not be properly disabled when not in use | Ensure GPIO is properly disabled when not needed to save power | 0.70 | 0.05 |

### /home/tom/github/zlecenia/maski/Programator_2025/lib/Boards/TMC_V200/HAL_Board.h

| Linia | Typ problemu | Opis | Sugestia | Wpływ | Zysk |
|-------|-------------|------|----------|-------|------|
| 17 | peripheral_not_disabled | Timer peripheral may not be properly disabled when not in use | Ensure Timer is properly disabled when not needed to save power | 0.70 | 0.05 |
| 21 | peripheral_not_disabled | SPI peripheral may not be properly disabled when not in use | Ensure SPI is properly disabled when not needed to save power | 0.70 | 0.05 |
| 23 | peripheral_not_disabled | SPI peripheral may not be properly disabled when not in use | Ensure SPI is properly disabled when not needed to save power | 0.70 | 0.05 |
| 27 | peripheral_not_disabled | SPI peripheral may not be properly disabled when not in use | Ensure SPI is properly disabled when not needed to save power | 0.70 | 0.05 |
| 28 | peripheral_not_disabled | SPI peripheral may not be properly disabled when not in use | Ensure SPI is properly disabled when not needed to save power | 0.70 | 0.05 |
| 35 | peripheral_not_disabled | UART peripheral may not be properly disabled when not in use | Ensure UART is properly disabled when not needed to save power | 0.70 | 0.05 |
| 42 | peripheral_not_disabled | UART peripheral may not be properly disabled when not in use | Ensure UART is properly disabled when not needed to save power | 0.70 | 0.05 |
| 47 | peripheral_not_disabled | UART peripheral may not be properly disabled when not in use | Ensure UART is properly disabled when not needed to save power | 0.70 | 0.05 |
| 48 | peripheral_not_disabled | UART peripheral may not be properly disabled when not in use | Ensure UART is properly disabled when not needed to save power | 0.70 | 0.05 |
| 52 | peripheral_not_disabled | UART peripheral may not be properly disabled when not in use | Ensure UART is properly disabled when not needed to save power | 0.70 | 0.05 |
| 53 | peripheral_not_disabled | UART peripheral may not be properly disabled when not in use | Ensure UART is properly disabled when not needed to save power | 0.70 | 0.05 |
| 102 | unused_clocks_enabled | Unused clocks may be enabled | Disable unused clock sources to save power | 0.60 | 0.10 |
| 153 | unused_clocks_enabled | Unused clocks may be enabled | Disable unused clock sources to save power | 0.60 | 0.10 |
| 174 | peripheral_not_disabled | Timer peripheral may not be properly disabled when not in use | Ensure Timer is properly disabled when not needed to save power | 0.70 | 0.05 |

### /home/tom/github/zlecenia/maski/Programator_2025/lib/Boards/TMD_V100/HAL_Board.c

| Linia | Typ problemu | Opis | Sugestia | Wpływ | Zysk |
|-------|-------------|------|----------|-------|------|
| 62 | peripheral_not_disabled | GPIO peripheral may not be properly disabled when not in use | Ensure GPIO is properly disabled when not needed to save power | 0.70 | 0.05 |
| 71 | peripheral_not_disabled | Timer peripheral may not be properly disabled when not in use | Ensure Timer is properly disabled when not needed to save power | 0.70 | 0.05 |

### /home/tom/github/zlecenia/maski/Programator_2025/lib/Boards/TMD_V100/HAL_Board.h

| Linia | Typ problemu | Opis | Sugestia | Wpływ | Zysk |
|-------|-------------|------|----------|-------|------|
| 11 | peripheral_not_disabled | Timer peripheral may not be properly disabled when not in use | Ensure Timer is properly disabled when not needed to save power | 0.70 | 0.05 |
| 12 | peripheral_not_disabled | Timer peripheral may not be properly disabled when not in use | Ensure Timer is properly disabled when not needed to save power | 0.70 | 0.05 |
| 33 | peripheral_not_disabled | UART peripheral may not be properly disabled when not in use | Ensure UART is properly disabled when not needed to save power | 0.70 | 0.05 |
| 47 | incomplete_port_config | Port output set without configuring direction | Configure port direction before setting output | 0.40 | 0.01 |

### /home/tom/github/zlecenia/maski/Programator_2025/lib/Display/WH4004A/WH4004A.c

| Linia | Typ problemu | Opis | Sugestia | Wpływ | Zysk |
|-------|-------------|------|----------|-------|------|
| 140 | unnecessary_loop_operations | Loop may contain operations that could be moved outside the loop | Identify and move loop-invariant operations outside the loop | 0.70 | 0.02 |
| 140 | inefficient_loop | Inefficient loop pattern detected - function calls or complex calculations in loop condition | Move function calls and calculations outside the loop or use simpler conditions | 0.60 | 0.03 |

### /home/tom/github/zlecenia/maski/Programator_2025/lib/Interface_txt/fs/interface_fs.c

| Linia | Typ problemu | Opis | Sugestia | Wpływ | Zysk |
|-------|-------------|------|----------|-------|------|
| 155 | inefficient_loop | Inefficient loop pattern detected - function calls or complex calculations in loop condition | Move function calls and calculations outside the loop or use simpler conditions | 0.60 | 0.03 |

### /home/tom/github/zlecenia/maski/Programator_2025/lib/Interface_txt/interface.c

| Linia | Typ problemu | Opis | Sugestia | Wpływ | Zysk |
|-------|-------------|------|----------|-------|------|
| 91 | inefficient_loop | Inefficient loop pattern detected - function calls or complex calculations in loop condition | Move function calls and calculations outside the loop or use simpler conditions | 0.60 | 0.03 |
| 102 | unnecessary_loop_operations | Loop may contain operations that could be moved outside the loop | Identify and move loop-invariant operations outside the loop | 0.70 | 0.02 |
| 102 | inefficient_loop | Inefficient loop pattern detected - function calls or complex calculations in loop condition | Move function calls and calculations outside the loop or use simpler conditions | 0.60 | 0.03 |
| 257 | peripheral_not_disabled | UART peripheral may not be properly disabled when not in use | Ensure UART is properly disabled when not needed to save power | 0.70 | 0.05 |
| 268 | inefficient_loop | Inefficient loop pattern detected - function calls or complex calculations in loop condition | Move function calls and calculations outside the loop or use simpler conditions | 0.60 | 0.03 |

### /home/tom/github/zlecenia/maski/Programator_2025/lib/MSP430x5xx/Disk_IO/HAL_MMC.c

| Linia | Typ problemu | Opis | Sugestia | Wpływ | Zysk |
|-------|-------------|------|----------|-------|------|
| 6 | peripheral_not_disabled | SPI peripheral may not be properly disabled when not in use | Ensure SPI is properly disabled when not needed to save power | 0.70 | 0.05 |
| 12 | peripheral_not_disabled | SPI peripheral may not be properly disabled when not in use | Ensure SPI is properly disabled when not needed to save power | 0.70 | 0.05 |
| 152 | peripheral_not_disabled | UART peripheral may not be properly disabled when not in use | Ensure UART is properly disabled when not needed to save power | 0.70 | 0.05 |
| 165 | peripheral_not_disabled | SPI peripheral may not be properly disabled when not in use | Ensure SPI is properly disabled when not needed to save power | 0.70 | 0.05 |
| 165 | peripheral_not_disabled | SPI peripheral may not be properly disabled when not in use | Ensure SPI is properly disabled when not needed to save power | 0.70 | 0.05 |
| 193 | inefficient_loop | Inefficient loop pattern detected - function calls or complex calculations in loop condition | Move function calls and calculations outside the loop or use simpler conditions | 0.60 | 0.03 |
| 201 | unnecessary_loop_operations | Loop may contain operations that could be moved outside the loop | Identify and move loop-invariant operations outside the loop | 0.70 | 0.02 |
| 201 | inefficient_loop | Inefficient loop pattern detected - function calls or complex calculations in loop condition | Move function calls and calculations outside the loop or use simpler conditions | 0.60 | 0.03 |
| 216 | peripheral_not_disabled | SPI peripheral may not be properly disabled when not in use | Ensure SPI is properly disabled when not needed to save power | 0.70 | 0.05 |
| 253 | peripheral_not_disabled | UART peripheral may not be properly disabled when not in use | Ensure UART is properly disabled when not needed to save power | 0.70 | 0.05 |
| 256 | peripheral_not_disabled | UART peripheral may not be properly disabled when not in use | Ensure UART is properly disabled when not needed to save power | 0.70 | 0.05 |
| 278 | peripheral_not_disabled | SPI peripheral may not be properly disabled when not in use | Ensure SPI is properly disabled when not needed to save power | 0.70 | 0.05 |
| 298 | inefficient_loop | Inefficient loop pattern detected - function calls or complex calculations in loop condition | Move function calls and calculations outside the loop or use simpler conditions | 0.60 | 0.03 |
| 304 | inefficient_loop | Inefficient loop pattern detected - function calls or complex calculations in loop condition | Move function calls and calculations outside the loop or use simpler conditions | 0.60 | 0.03 |
| 416 | inefficient_loop | Inefficient loop pattern detected - function calls or complex calculations in loop condition | Move function calls and calculations outside the loop or use simpler conditions | 0.60 | 0.03 |
| 453 | unnecessary_loop_operations | Loop may contain operations that could be moved outside the loop | Identify and move loop-invariant operations outside the loop | 0.70 | 0.02 |
| 453 | inefficient_loop | Inefficient loop pattern detected - function calls or complex calculations in loop condition | Move function calls and calculations outside the loop or use simpler conditions | 0.60 | 0.03 |
| 578 | inefficient_loop | Inefficient loop pattern detected - function calls or complex calculations in loop condition | Move function calls and calculations outside the loop or use simpler conditions | 0.60 | 0.03 |
| 593 | inefficient_loop | Inefficient loop pattern detected - function calls or complex calculations in loop condition | Move function calls and calculations outside the loop or use simpler conditions | 0.60 | 0.03 |
| 620 | peripheral_not_disabled | SPI peripheral may not be properly disabled when not in use | Ensure SPI is properly disabled when not needed to save power | 0.70 | 0.05 |
| 624 | unnecessary_loop_operations | Loop may contain operations that could be moved outside the loop | Identify and move loop-invariant operations outside the loop | 0.70 | 0.02 |
| 624 | inefficient_loop | Inefficient loop pattern detected - function calls or complex calculations in loop condition | Move function calls and calculations outside the loop or use simpler conditions | 0.60 | 0.03 |
| 629 | unnecessary_loop_operations | Loop may contain operations that could be moved outside the loop | Identify and move loop-invariant operations outside the loop | 0.70 | 0.02 |
| 629 | inefficient_loop | Inefficient loop pattern detected - function calls or complex calculations in loop condition | Move function calls and calculations outside the loop or use simpler conditions | 0.60 | 0.03 |
| 1038 | inefficient_loop | Inefficient loop pattern detected - function calls or complex calculations in loop condition | Move function calls and calculations outside the loop or use simpler conditions | 0.60 | 0.03 |

### /home/tom/github/zlecenia/maski/Programator_2025/lib/MSP430x5xx/Flash/HAL_FLASH.c

| Linia | Typ problemu | Opis | Sugestia | Wpływ | Zysk |
|-------|-------------|------|----------|-------|------|
| 80 | unnecessary_loop_operations | Loop may contain operations that could be moved outside the loop | Identify and move loop-invariant operations outside the loop | 0.70 | 0.02 |
| 80 | inefficient_loop | Inefficient loop pattern detected - function calls or complex calculations in loop condition | Move function calls and calculations outside the loop or use simpler conditions | 0.60 | 0.03 |
| 94 | unnecessary_loop_operations | Loop may contain operations that could be moved outside the loop | Identify and move loop-invariant operations outside the loop | 0.70 | 0.02 |
| 109 | unnecessary_loop_operations | Loop may contain operations that could be moved outside the loop | Identify and move loop-invariant operations outside the loop | 0.70 | 0.02 |
| 139 | unnecessary_loop_operations | Loop may contain operations that could be moved outside the loop | Identify and move loop-invariant operations outside the loop | 0.70 | 0.02 |

### /home/tom/github/zlecenia/maski/Programator_2025/lib/MSP430x5xx/UART/HAL_UART.h

| Linia | Typ problemu | Opis | Sugestia | Wpływ | Zysk |
|-------|-------------|------|----------|-------|------|
| 26 | peripheral_not_disabled | UART peripheral may not be properly disabled when not in use | Ensure UART is properly disabled when not needed to save power | 0.70 | 0.05 |
| 27 | peripheral_not_disabled | UART peripheral may not be properly disabled when not in use | Ensure UART is properly disabled when not needed to save power | 0.70 | 0.05 |
| 28 | peripheral_not_disabled | UART peripheral may not be properly disabled when not in use | Ensure UART is properly disabled when not needed to save power | 0.70 | 0.05 |
| 29 | peripheral_not_disabled | UART peripheral may not be properly disabled when not in use | Ensure UART is properly disabled when not needed to save power | 0.70 | 0.05 |
| 30 | peripheral_not_disabled | UART peripheral may not be properly disabled when not in use | Ensure UART is properly disabled when not needed to save power | 0.70 | 0.05 |
| 37 | peripheral_not_disabled | UART peripheral may not be properly disabled when not in use | Ensure UART is properly disabled when not needed to save power | 0.70 | 0.05 |
| 38 | peripheral_not_disabled | UART peripheral may not be properly disabled when not in use | Ensure UART is properly disabled when not needed to save power | 0.70 | 0.05 |
| 40 | peripheral_not_disabled | UART peripheral may not be properly disabled when not in use | Ensure UART is properly disabled when not needed to save power | 0.70 | 0.05 |
| 42 | peripheral_not_disabled | UART peripheral may not be properly disabled when not in use | Ensure UART is properly disabled when not needed to save power | 0.70 | 0.05 |
| 43 | peripheral_not_disabled | UART peripheral may not be properly disabled when not in use | Ensure UART is properly disabled when not needed to save power | 0.70 | 0.05 |
| 45 | peripheral_not_disabled | UART peripheral may not be properly disabled when not in use | Ensure UART is properly disabled when not needed to save power | 0.70 | 0.05 |
| 53 | peripheral_not_disabled | UART peripheral may not be properly disabled when not in use | Ensure UART is properly disabled when not needed to save power | 0.70 | 0.05 |
| 54 | peripheral_not_disabled | UART peripheral may not be properly disabled when not in use | Ensure UART is properly disabled when not needed to save power | 0.70 | 0.05 |
| 55 | peripheral_not_disabled | UART peripheral may not be properly disabled when not in use | Ensure UART is properly disabled when not needed to save power | 0.70 | 0.05 |
| 57 | peripheral_not_disabled | UART peripheral may not be properly disabled when not in use | Ensure UART is properly disabled when not needed to save power | 0.70 | 0.05 |
| 59 | peripheral_not_disabled | UART peripheral may not be properly disabled when not in use | Ensure UART is properly disabled when not needed to save power | 0.70 | 0.05 |
| 63 | peripheral_not_disabled | UART peripheral may not be properly disabled when not in use | Ensure UART is properly disabled when not needed to save power | 0.70 | 0.05 |
| 64 | peripheral_not_disabled | UART peripheral may not be properly disabled when not in use | Ensure UART is properly disabled when not needed to save power | 0.70 | 0.05 |
| 65 | peripheral_not_disabled | UART peripheral may not be properly disabled when not in use | Ensure UART is properly disabled when not needed to save power | 0.70 | 0.05 |
| 66 | peripheral_not_disabled | UART peripheral may not be properly disabled when not in use | Ensure UART is properly disabled when not needed to save power | 0.70 | 0.05 |
| 67 | peripheral_not_disabled | UART peripheral may not be properly disabled when not in use | Ensure UART is properly disabled when not needed to save power | 0.70 | 0.05 |
| 68 | peripheral_not_disabled | UART peripheral may not be properly disabled when not in use | Ensure UART is properly disabled when not needed to save power | 0.70 | 0.05 |
| 70 | peripheral_not_disabled | UART peripheral may not be properly disabled when not in use | Ensure UART is properly disabled when not needed to save power | 0.70 | 0.05 |
| 71 | peripheral_not_disabled | UART peripheral may not be properly disabled when not in use | Ensure UART is properly disabled when not needed to save power | 0.70 | 0.05 |
| 72 | peripheral_not_disabled | UART peripheral may not be properly disabled when not in use | Ensure UART is properly disabled when not needed to save power | 0.70 | 0.05 |

### /home/tom/github/zlecenia/maski/Programator_2025/lib/MSP430x5xx/UART/HAL_UART0.c

| Linia | Typ problemu | Opis | Sugestia | Wpływ | Zysk |
|-------|-------------|------|----------|-------|------|
| 19 | peripheral_not_disabled | UART peripheral may not be properly disabled when not in use | Ensure UART is properly disabled when not needed to save power | 0.70 | 0.05 |
| 20 | peripheral_not_disabled | UART peripheral may not be properly disabled when not in use | Ensure UART is properly disabled when not needed to save power | 0.70 | 0.05 |
| 22 | peripheral_not_disabled | UART peripheral may not be properly disabled when not in use | Ensure UART is properly disabled when not needed to save power | 0.70 | 0.05 |
| 22 | peripheral_not_disabled | UART peripheral may not be properly disabled when not in use | Ensure UART is properly disabled when not needed to save power | 0.70 | 0.05 |
| 26 | peripheral_not_disabled | UART peripheral may not be properly disabled when not in use | Ensure UART is properly disabled when not needed to save power | 0.70 | 0.05 |
| 28 | peripheral_not_disabled | UART peripheral may not be properly disabled when not in use | Ensure UART is properly disabled when not needed to save power | 0.70 | 0.05 |
| 29 | peripheral_not_disabled | UART peripheral may not be properly disabled when not in use | Ensure UART is properly disabled when not needed to save power | 0.70 | 0.05 |
| 37 | peripheral_not_disabled | UART peripheral may not be properly disabled when not in use | Ensure UART is properly disabled when not needed to save power | 0.70 | 0.05 |
| 43 | peripheral_not_disabled | UART peripheral may not be properly disabled when not in use | Ensure UART is properly disabled when not needed to save power | 0.70 | 0.05 |
| 44 | peripheral_not_disabled | UART peripheral may not be properly disabled when not in use | Ensure UART is properly disabled when not needed to save power | 0.70 | 0.05 |
| 51 | peripheral_not_disabled | UART peripheral may not be properly disabled when not in use | Ensure UART is properly disabled when not needed to save power | 0.70 | 0.05 |
| 55 | peripheral_not_disabled | UART peripheral may not be properly disabled when not in use | Ensure UART is properly disabled when not needed to save power | 0.70 | 0.05 |
| 56 | peripheral_not_disabled | UART peripheral may not be properly disabled when not in use | Ensure UART is properly disabled when not needed to save power | 0.70 | 0.05 |
| 57 | peripheral_not_disabled | UART peripheral may not be properly disabled when not in use | Ensure UART is properly disabled when not needed to save power | 0.70 | 0.05 |
| 61 | peripheral_not_disabled | UART peripheral may not be properly disabled when not in use | Ensure UART is properly disabled when not needed to save power | 0.70 | 0.05 |
| 65 | peripheral_not_disabled | UART peripheral may not be properly disabled when not in use | Ensure UART is properly disabled when not needed to save power | 0.70 | 0.05 |

### /home/tom/github/zlecenia/maski/Programator_2025/lib/MSP430x5xx/UART/HAL_UART3.c

| Linia | Typ problemu | Opis | Sugestia | Wpływ | Zysk |
|-------|-------------|------|----------|-------|------|
| 15 | peripheral_not_disabled | UART peripheral may not be properly disabled when not in use | Ensure UART is properly disabled when not needed to save power | 0.70 | 0.05 |
| 19 | peripheral_not_disabled | UART peripheral may not be properly disabled when not in use | Ensure UART is properly disabled when not needed to save power | 0.70 | 0.05 |
| 20 | peripheral_not_disabled | UART peripheral may not be properly disabled when not in use | Ensure UART is properly disabled when not needed to save power | 0.70 | 0.05 |
| 22 | peripheral_not_disabled | UART peripheral may not be properly disabled when not in use | Ensure UART is properly disabled when not needed to save power | 0.70 | 0.05 |
| 24 | peripheral_not_disabled | UART peripheral may not be properly disabled when not in use | Ensure UART is properly disabled when not needed to save power | 0.70 | 0.05 |
| 24 | peripheral_not_disabled | UART peripheral may not be properly disabled when not in use | Ensure UART is properly disabled when not needed to save power | 0.70 | 0.05 |
| 26 | peripheral_not_disabled | UART peripheral may not be properly disabled when not in use | Ensure UART is properly disabled when not needed to save power | 0.70 | 0.05 |
| 43 | peripheral_not_disabled | UART peripheral may not be properly disabled when not in use | Ensure UART is properly disabled when not needed to save power | 0.70 | 0.05 |
| 47 | peripheral_not_disabled | UART peripheral may not be properly disabled when not in use | Ensure UART is properly disabled when not needed to save power | 0.70 | 0.05 |
| 48 | peripheral_not_disabled | UART peripheral may not be properly disabled when not in use | Ensure UART is properly disabled when not needed to save power | 0.70 | 0.05 |
| 57 | peripheral_not_disabled | UART peripheral may not be properly disabled when not in use | Ensure UART is properly disabled when not needed to save power | 0.70 | 0.05 |
| 60 | peripheral_not_disabled | UART peripheral may not be properly disabled when not in use | Ensure UART is properly disabled when not needed to save power | 0.70 | 0.05 |
| 61 | peripheral_not_disabled | UART peripheral may not be properly disabled when not in use | Ensure UART is properly disabled when not needed to save power | 0.70 | 0.05 |
| 65 | peripheral_not_disabled | UART peripheral may not be properly disabled when not in use | Ensure UART is properly disabled when not needed to save power | 0.70 | 0.05 |
| 65 | peripheral_not_disabled | UART peripheral may not be properly disabled when not in use | Ensure UART is properly disabled when not needed to save power | 0.70 | 0.05 |
| 66 | peripheral_not_disabled | UART peripheral may not be properly disabled when not in use | Ensure UART is properly disabled when not needed to save power | 0.70 | 0.05 |

### /home/tom/github/zlecenia/maski/Programator_2025/lib/MSP430x5xx/UART/HAL_UART_Funct.h

| Linia | Typ problemu | Opis | Sugestia | Wpływ | Zysk |
|-------|-------------|------|----------|-------|------|
| 41 | inefficient_loop | Inefficient loop pattern detected - function calls or complex calculations in loop condition | Move function calls and calculations outside the loop or use simpler conditions | 0.60 | 0.03 |
| 57 | inefficient_loop | Inefficient loop pattern detected - function calls or complex calculations in loop condition | Move function calls and calculations outside the loop or use simpler conditions | 0.60 | 0.03 |
| 91 | unnecessary_loop_operations | Loop may contain operations that could be moved outside the loop | Identify and move loop-invariant operations outside the loop | 0.70 | 0.02 |
| 112 | inefficient_loop | Inefficient loop pattern detected - function calls or complex calculations in loop condition | Move function calls and calculations outside the loop or use simpler conditions | 0.60 | 0.03 |
| 195 | unnecessary_loop_operations | Loop may contain operations that could be moved outside the loop | Identify and move loop-invariant operations outside the loop | 0.70 | 0.02 |
| 195 | inefficient_loop | Inefficient loop pattern detected - function calls or complex calculations in loop condition | Move function calls and calculations outside the loop or use simpler conditions | 0.60 | 0.03 |
| 253 | inefficient_loop | Inefficient loop pattern detected - function calls or complex calculations in loop condition | Move function calls and calculations outside the loop or use simpler conditions | 0.60 | 0.03 |

### /home/tom/github/zlecenia/maski/Programator_2025/lib/MSP430x5xx/UCS/HAL_UCS.c

| Linia | Typ problemu | Opis | Sugestia | Wpływ | Zysk |
|-------|-------------|------|----------|-------|------|
| 119 | unnecessary_loop_operations | Loop may contain operations that could be moved outside the loop | Identify and move loop-invariant operations outside the loop | 0.70 | 0.02 |
| 216 | unnecessary_loop_operations | Loop may contain operations that could be moved outside the loop | Identify and move loop-invariant operations outside the loop | 0.70 | 0.02 |
| 268 | inefficient_loop | Inefficient loop pattern detected - function calls or complex calculations in loop condition | Move function calls and calculations outside the loop or use simpler conditions | 0.60 | 0.03 |
| 294 | inefficient_loop | Inefficient loop pattern detected - function calls or complex calculations in loop condition | Move function calls and calculations outside the loop or use simpler conditions | 0.60 | 0.03 |

### /home/tom/github/zlecenia/maski/Programator_2025/lib/MSP430x5xx/UCS/HAL_UCS.h

| Linia | Typ problemu | Opis | Sugestia | Wpływ | Zysk |
|-------|-------------|------|----------|-------|------|
| 63 | unused_clocks_enabled | Unused clocks may be enabled | Disable unused clock sources to save power | 0.60 | 0.10 |
| 63 | unused_clocks_enabled | Unused clocks may be enabled | Disable unused clock sources to save power | 0.60 | 0.10 |

### /home/tom/github/zlecenia/maski/Programator_2025/lib/my_lib/Fifo/fifo.c

| Linia | Typ problemu | Opis | Sugestia | Wpływ | Zysk |
|-------|-------------|------|----------|-------|------|
| 31 | inefficient_loop | Inefficient loop pattern detected - function calls or complex calculations in loop condition | Move function calls and calculations outside the loop or use simpler conditions | 0.60 | 0.03 |

### /home/tom/github/zlecenia/maski/Programator_2025/lib/my_lib/NumberFixedPoint/numberFixedPoint.c

| Linia | Typ problemu | Opis | Sugestia | Wpływ | Zysk |
|-------|-------------|------|----------|-------|------|
| 22 | inefficient_loop | Inefficient loop pattern detected - function calls or complex calculations in loop condition | Move function calls and calculations outside the loop or use simpler conditions | 0.60 | 0.03 |
| 44 | unnecessary_loop_operations | Loop may contain operations that could be moved outside the loop | Identify and move loop-invariant operations outside the loop | 0.70 | 0.02 |
| 44 | inefficient_loop | Inefficient loop pattern detected - function calls or complex calculations in loop condition | Move function calls and calculations outside the loop or use simpler conditions | 0.60 | 0.03 |
| 70 | inefficient_loop | Inefficient loop pattern detected - function calls or complex calculations in loop condition | Move function calls and calculations outside the loop or use simpler conditions | 0.60 | 0.03 |
| 110 | inefficient_loop | Inefficient loop pattern detected - function calls or complex calculations in loop condition | Move function calls and calculations outside the loop or use simpler conditions | 0.60 | 0.03 |

### /home/tom/github/zlecenia/maski/Programator_2025/lib/my_lib/String/my_string.c

| Linia | Typ problemu | Opis | Sugestia | Wpływ | Zysk |
|-------|-------------|------|----------|-------|------|
| 6 | inefficient_loop | Inefficient loop pattern detected - function calls or complex calculations in loop condition | Move function calls and calculations outside the loop or use simpler conditions | 0.60 | 0.03 |

### /home/tom/github/zlecenia/maski/Programator_2025/lib/my_lib/msbus/msbus.c

| Linia | Typ problemu | Opis | Sugestia | Wpływ | Zysk |
|-------|-------------|------|----------|-------|------|
| 82 | peripheral_not_disabled | UART peripheral may not be properly disabled when not in use | Ensure UART is properly disabled when not needed to save power | 0.70 | 0.05 |
| 85 | unnecessary_loop_operations | Loop may contain operations that could be moved outside the loop | Identify and move loop-invariant operations outside the loop | 0.70 | 0.02 |
| 85 | inefficient_loop | Inefficient loop pattern detected - function calls or complex calculations in loop condition | Move function calls and calculations outside the loop or use simpler conditions | 0.60 | 0.03 |
| 87 | peripheral_not_disabled | UART peripheral may not be properly disabled when not in use | Ensure UART is properly disabled when not needed to save power | 0.70 | 0.05 |
| 95 | peripheral_not_disabled | UART peripheral may not be properly disabled when not in use | Ensure UART is properly disabled when not needed to save power | 0.70 | 0.05 |
| 99 | peripheral_not_disabled | UART peripheral may not be properly disabled when not in use | Ensure UART is properly disabled when not needed to save power | 0.70 | 0.05 |
| 102 | inefficient_loop | Inefficient loop pattern detected - function calls or complex calculations in loop condition | Move function calls and calculations outside the loop or use simpler conditions | 0.60 | 0.03 |
| 107 | peripheral_not_disabled | UART peripheral may not be properly disabled when not in use | Ensure UART is properly disabled when not needed to save power | 0.70 | 0.05 |
| 118 | peripheral_not_disabled | UART peripheral may not be properly disabled when not in use | Ensure UART is properly disabled when not needed to save power | 0.70 | 0.05 |
| 122 | peripheral_not_disabled | UART peripheral may not be properly disabled when not in use | Ensure UART is properly disabled when not needed to save power | 0.70 | 0.05 |
| 125 | inefficient_loop | Inefficient loop pattern detected - function calls or complex calculations in loop condition | Move function calls and calculations outside the loop or use simpler conditions | 0.60 | 0.03 |
| 127 | peripheral_not_disabled | UART peripheral may not be properly disabled when not in use | Ensure UART is properly disabled when not needed to save power | 0.70 | 0.05 |

### TMC_V200/main.c

| Linia | Typ problemu | Opis | Sugestia | Wpływ | Zysk |
|-------|-------------|------|----------|-------|------|
| 417 | busy_wait_pattern | Busy-wait pattern detected - wastes energy by keeping CPU active | Replace busy-wait with low power mode and interrupts | 0.75 | 0.15 |

### TMD_V100/main.c

| Linia | Typ problemu | Opis | Sugestia | Wpływ | Zysk |
|-------|-------------|------|----------|-------|------|
| 253 | busy_wait_pattern | Busy-wait pattern detected - wastes energy by keeping CPU active | Replace busy-wait with low power mode and interrupts | 0.75 | 0.15 |
| 261 | busy_wait_pattern | Busy-wait pattern detected - wastes energy by keeping CPU active | Replace busy-wait with low power mode and interrupts | 0.75 | 0.15 |
| 264 | busy_wait_pattern | Busy-wait pattern detected - wastes energy by keeping CPU active | Replace busy-wait with low power mode and interrupts | 0.75 | 0.15 |
| 271 | busy_wait_pattern | Busy-wait pattern detected - wastes energy by keeping CPU active | Replace busy-wait with low power mode and interrupts | 0.75 | 0.15 |
| 286 | busy_wait_pattern | Busy-wait pattern detected - wastes energy by keeping CPU active | Replace busy-wait with low power mode and interrupts | 0.75 | 0.15 |

### TMD_V100/tmp.c

| Linia | Typ problemu | Opis | Sugestia | Wpływ | Zysk |
|-------|-------------|------|----------|-------|------|
| 68 | high_frequency_pattern | High frequency clock configuration - may consume unnecessary power | Use lower frequency when high performance not needed | 0.60 | 0.20 |
| 68 | unused_clock_pattern | Clock enabled but appears unused | Disable unused clocks to save power | 0.60 | 0.10 |
| 69 | high_frequency_pattern | High frequency clock configuration - may consume unnecessary power | Use lower frequency when high performance not needed | 0.60 | 0.20 |
| 71 | unused_clock_pattern | Clock enabled but appears unused | Disable unused clocks to save power | 0.60 | 0.10 |
| 74 | unused_clock_pattern | Clock enabled but appears unused | Disable unused clocks to save power | 0.60 | 0.10 |
| 77 | unused_clock_pattern | Clock enabled but appears unused | Disable unused clocks to save power | 0.60 | 0.10 |

### lib/Boards/TMC_V200/HAL_Board.c

| Linia | Typ problemu | Opis | Sugestia | Wpływ | Zysk |
|-------|-------------|------|----------|-------|------|
| 165 | suboptimal_adc_pattern | Suboptimal ADC configuration detected | Optimize ADC sampling time when appropriate | 0.45 | 0.03 |
| 178 | suboptimal_adc_pattern | Suboptimal ADC configuration detected | Optimize ADC sampling time when appropriate | 0.45 | 0.03 |

### lib/Boards/TMC_V200/HAL_Board.h

| Linia | Typ problemu | Opis | Sugestia | Wpływ | Zysk |
|-------|-------------|------|----------|-------|------|
| 181 | suboptimal_adc_pattern | Suboptimal ADC configuration detected | Optimize ADC sampling time when appropriate | 0.45 | 0.03 |
| 187 | suboptimal_adc_pattern | Suboptimal ADC configuration detected | Optimize ADC sampling time when appropriate | 0.45 | 0.03 |
| 194 | suboptimal_adc_pattern | Suboptimal ADC configuration detected | Optimize ADC sampling time when appropriate | 0.45 | 0.03 |

### lib/Boards/TMD_V100/HAL_Board.c

| Linia | Typ problemu | Opis | Sugestia | Wpływ | Zysk |
|-------|-------------|------|----------|-------|------|
| 20 | unconfigured_pins_pattern | Unconfigured GPIO pin directions | Configure pin directions explicitly | 0.40 | 0.01 |

### lib/MSP430x5xx/Disk_IO/HAL_MMC.c

| Linia | Typ problemu | Opis | Sugestia | Wpływ | Zysk |
|-------|-------------|------|----------|-------|------|
| 453 | delay_loop_pattern | Delay loop detected - inefficient way to create delays | Use timers instead of delay loops | 0.65 | 0.08 |

### lib/MSP430x5xx/UART/HAL_UART_Funct.h

| Linia | Typ problemu | Opis | Sugestia | Wpływ | Zysk |
|-------|-------------|------|----------|-------|------|
| 91 | busy_wait_pattern | Busy-wait pattern detected - wastes energy by keeping CPU active | Replace busy-wait with low power mode and interrupts | 0.75 | 0.15 |

### lib/my_lib/msbus/msbus.c

| Linia | Typ problemu | Opis | Sugestia | Wpływ | Zysk |
|-------|-------------|------|----------|-------|------|
| 41 | busy_wait_pattern | Busy-wait pattern detected - wastes energy by keeping CPU active | Replace busy-wait with low power mode and interrupts | 0.75 | 0.15 |

## Rekomendacje

1. **Priorytety optymalizacji**: Skup się najpierw na problemach o wysokim wpływie (> 0.7).
2. **Busy-wait i polling**: Zastąp aktywne oczekiwanie podejściem opartym na przerwaniach.
3. **Tryby uśpienia**: Wykorzystuj głębsze tryby uśpienia (LPM3/LPM4) zamiast LPM0.
4. **Zarządzanie peryferiami**: Wyłączaj nieużywane peryferia i zegary.
5. **Optymalizacja pętli**: Przenoś niezmienne operacje poza pętle.