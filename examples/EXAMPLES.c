/**
* Przykłady poprawek do najczęstszych problemów energetycznych znalezionych przez narzędzie.
* Zawiera oryginalne fragmenty kodu oraz ich poprawione wersje.
  */

////////////////////////////////////////////////////////////////////////////////
// Przykład 1: Zamiana pętli busy-wait na podejście oparte na przerwaniach
////////////////////////////////////////////////////////////////////////////////

// KOD ORYGINALNY:
while(1) { // ENERGY: Busy-wait pattern detected - wastes energy by keeping CPU active
if(data_ready) {
process_data();
}
}

// POPRAWIONY KOD:
// 1. Konfiguracja przerwania dla sygnału data_ready
void setup() {
// Konfiguracja GPIO dla data_ready jako źródła przerwania
P1IE |= DATA_READY_PIN;  // Włącz przerwanie dla pinu data_ready
P1IES |= DATA_READY_PIN; // Przerwanie na zboczu opadającym
P1IFG &= ~DATA_READY_PIN; // Wyczyść flagę przerwania

// Włącz przerwania ogólnie i wejdź w tryb niskiego poboru energii
__bis_SR_register(LPM3_bits + GIE);
}

// 2. Procedura obsługi przerwania
#pragma vector=PORT1_VECTOR
__interrupt void Port_1(void) {
if (P1IFG & DATA_READY_PIN) {
// Obsługa danych
process_data();

    // Wyczyść flagę przerwania
    P1IFG &= ~DATA_READY_PIN;
}

// Procesor automatycznie wraca do trybu LPM3, który był aktywny przed przerwaniem
}

////////////////////////////////////////////////////////////////////////////////
// Przykład 2: Przeniesienie niezmiennych operacji poza pętlę
////////////////////////////////////////////////////////////////////////////////

// KOD ORYGINALNY:
for(i=0; i<count; i++) { // ENERGY: Loop may contain operations that could be moved outside
result = expensive_calculation(); // Ta operacja daje ten sam wynik w każdej iteracji
data[i] = result + i;
}

// POPRAWIONY KOD:
// Obliczenie wyniku raz przed pętlą
result = expensive_calculation();
// Użycie obliczonej wartości wewnątrz pętli
for(i=0; i<count; i++) {
data[i] = result + i;
}

////////////////////////////////////////////////////////////////////////////////
// Przykład 3: Poprawne zarządzanie peryferyjami (wyłączanie, gdy nie są używane)
////////////////////////////////////////////////////////////////////////////////

// KOD ORYGINALNY:
// Konfiguracja UART
UCA0CTL1 |= UCSSEL_2; // ENERGY: UART peripheral may not be properly disabled when not in use
UCA0BR0 = 104;
UCA0BR1 = 0;
UCA0MCTL = UCBRS0;

send_uart_data();
// UART pozostaje aktywny, zużywając energię, choć nie jest używany

// POPRAWIONY KOD:
// Funkcja włączająca UART
void uart_enable() {
UCA0CTL1 |= UCSWRST;      // Wstrzymaj UART podczas konfiguracji
UCA0CTL1 |= UCSSEL_2;     // Wybierz źródło zegara
UCA0BR0 = 104;            // Konfiguracja prędkości
UCA0BR1 = 0;
UCA0MCTL = UCBRS0;
UCA0CTL1 &= ~UCSWRST;     // Uruchom UART
}

// Funkcja wyłączająca UART
void uart_disable() {
UCA0CTL1 |= UCSWRST;      // Wstrzymaj UART
UCA0IE &= ~(UCRXIE + UCTXIE); // Wyłącz przerwania
// Opcjonalnie można również wyłączyć piny lub zegar
}

// Używanie UART tylko gdy potrzebne
uart_enable();
send_uart_data();
uart_disable();  // Wyłącz UART, gdy nie jest używany

////////////////////////////////////////////////////////////////////////////////
// Przykład 4: Optymalizacja konfiguracji ADC
////////////////////////////////////////////////////////////////////////////////

// KOD ORYGINALNY:
ADC10CTL0 |= ADC10SHT_2 + ADC10ON; // ENERGY: Suboptimal ADC configuration detected

// POPRAWIONY KOD:
// Użyj najkrótszego czasu próbkowania, jeśli warunki sygnału na to pozwalają
ADC10CTL0 |= ADC10SHT_0 + ADC10ON; // Najkrótszy czas próbkowania

// Lub dynamicznie dostosuj czas próbkowania w zależności od potrzeb
if (needs_longer_sampling) {
ADC10CTL0 |= ADC10SHT_2 + ADC10ON; // Dłuższy czas dla trudnych sygnałów
} else {
ADC10CTL0 |= ADC10SHT_0 + ADC10ON; // Krótszy czas dla typowych sygnałów
}

////////////////////////////////////////////////////////////////////////////////
// Przykład 5: Zastąpienie pętli opóźniających timerami
////////////////////////////////////////////////////////////////////////////////

// KOD ORYGINALNY:
// Opóźnienie za pomocą pętli
for(uint16_t i=0; i<1000; i++); // ENERGY: Delay loop detected - inefficient way to create delays

// POPRAWIONY KOD:
// Konfiguracja timera do generowania opóźnienia
void setup_delay_timer() {
TA0CCR0 = 1000;                // Wartość timera określająca opóźnienie
TA0CTL = TASSEL_2 + MC_1 + TAIE; // Skonfiguruj timer (SMCLK, up mode, przerwanie)
__bis_SR_register(LPM0_bits);   // Wejdź w tryb niskiego poboru energii
}

// Procedura obsługi przerwania timera
#pragma vector=TIMER0_A1_VECTOR
__interrupt void Timer_A(void) {
switch(TA0IV) {
case 10:  // Przerwanie przepełnienia
TA0CTL &= ~MC_1;  // Zatrzymaj timer
__bic_SR_register_on_exit(LPM0_bits);  // Wyjdź z trybu LPM0
break;
}
}

////////////////////////////////////////////////////////////////////////////////
// Przykład 6: Poprawna konfiguracja portów GPIO
////////////////////////////////////////////////////////////////////////////////

// KOD ORYGINALNY:
P1OUT |= BIT0; // ENERGY: Port output set without configuring direction

// POPRAWIONY KOD:
// Najpierw skonfiguruj kierunek pinu jako wyjście
P1DIR |= BIT0;  // Ustaw pin jako wyjście
P1OUT |= BIT0;  // Następnie ustaw wartość wyjściową

////////////////////////////////////////////////////////////////////////////////
// Przykład 7: Zarządzanie częstotliwością zegara
////////////////////////////////////////////////////////////////////////////////

// KOD ORYGINALNY:
BCSCTL1 = CALBC1_16MHZ; // ENERGY: High frequency clock configuration
DCOCTL = CALDCO_16MHZ;  // Zawsze używa wysokiej częstotliwości

// POPRAWIONY KOD:
// Dynamiczne zarządzanie częstotliwością
void set_cpu_speed(uint8_t high_speed) {
if (high_speed) {
// Wysoka wydajność, gdy potrzebna
BCSCTL1 = CALBC1_16MHZ;
DCOCTL = CALDCO_16MHZ;
} else {
// Niższe zużycie energii, gdy nie potrzeba pełnej wydajności
BCSCTL1 = CALBC1_1MHZ;
DCOCTL = CALDCO_1MHZ;
}
}

// Używanie wysokiej częstotliwości tylko gdy potrzebna
set_cpu_speed(0);  // Domyślnie niska częstotliwość
// ...
set_cpu_speed(1);  // Przełącz na wysoką częstotliwość przed intensywnymi obliczeniami
perform_complex_task();
set_cpu_speed(0);  // Wróć do niskiej częstotliwości po zakończeniu