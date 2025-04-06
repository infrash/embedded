#!/usr/bin/env python3
"""
Helper functions for generating context-aware energy optimization comments.

This module provides improved functions for generating more specific and actionable
energy optimization comments based on issue type and code context.
"""

import re
import logging
from typing import Optional, Dict, Any

# Set up logging
logger = logging.getLogger("energy-optimizer.comment-helpers")

def generate_inline_comment(issue: Any, line: str) -> str:
    """
    Generate a more specific inline comment based on the issue type and code context.

    Args:
        issue: Energy issue object with information about the detected issue
        line: The line of code where the issue was detected

    Returns:
        A context-aware energy optimization comment for inline insertion
    """
    desc = getattr(issue, 'description', "Energy issue detected")
    suggestion = getattr(issue, 'suggestion', "")
    impact = getattr(issue, 'impact', 0.0)
    gain = getattr(issue, 'optimization_gain', 0.0)

    # Start with basic comment
    comment = f"ENERGY: {desc}"

    # Add more specific information based on issue type and code context
    issue_type = getattr(issue, 'issue_type', "")

    if "busy_wait" in issue_type or "busy_wait_pattern" in issue_type:
        if "while (1)" in line or "while(1)" in line:
            comment += f" - {suggestion} (zastąp: _BIS_SR(LPM3_bits + GIE); // CPU śpi, przerwania wybudzają)"
        elif "for" in line and "delay" in line.lower():
            comment += f" - {suggestion} (użyj Timer_A z przerwaniem zamiast aktywnego oczekiwania)"
        else:
            comment += f" - {suggestion} (użyj _BIS_SR(LPM3_bits + GIE))"

    elif "sleep_mode" in issue_type:
        if "LPM0" in line:
            comment += f" - {suggestion} (zastosuj _BIS_SR(LPM3_bits) zamiast LPM0 dla dłuższych okresów bezczynności)"
        else:
            comment += f" - {suggestion} (zastosuj głębszy tryb uśpienia)"

    elif "loop" in issue_type and ("unnecessary" in issue_type or "inefficient" in issue_type):
        invariant_op = find_invariant_operation(line)
        if invariant_op:
            comment += f" - {suggestion} (przenieś operację '{invariant_op}' przed pętlę)"
        else:
            comment += f" - {suggestion} (przenieś niezmienne obliczenia poza pętlę)"

    elif "adc" in issue_type.lower() or "suboptimal_adc" in issue_type:
        if "ADC12CTL0 =" in line or "ADC12CTL0 |=" in line:
            comment += f" - {suggestion} (użyj ADC12SHT_0 dla krótszego czasu próbkowania gdy to możliwe)"
        else:
            comment += f" - {suggestion} (zoptymalizuj konfigurację ADC)"

    elif "peripheral_not_disabled" in issue_type:
        peripheral_type = detect_peripheral_type(line)
        comment += f" - {suggestion} (wyłącz {peripheral_type} po użyciu: {peripheral_type}_disable())"

    elif "clock" in issue_type.lower():
        if "BCSCTL" in line or "DCOCTL" in line:
            comment += f" - {suggestion} (obniż częstotliwość zegara gdy nie jest potrzebna wysoka wydajność)"
        else:
            comment += f" - {suggestion} (wyłącz nieużywane zegary)"

    elif "pin" in issue_type or "port" in issue_type or "gpio" in issue_type:
        if "OUT" in line and "DIR" not in line:
            comment += f" - {suggestion} (najpierw skonfiguruj kierunek PIN_DIR, potem ustaw wartość PIN_OUT)"
        else:
            comment += f" - {suggestion} (popraw konfigurację portów GPIO)"

    elif impact >= 0.7:  # Wysokie znaczenie
        comment += f" - {suggestion} (Impact: {impact:.2f}, Szacowane oszczędności: {gain*100:.0f}%)"
    else:
        comment += f" - {suggestion}"

    return comment


def generate_todo_comment(issue: Any, line: str, fix_example: str = "") -> str:
    """
    Generate a detailed TODO comment with specific fix suggestions based on code context.

    Args:
        issue: Energy issue object with information about the detected issue
        line: The line of code where the issue was detected
        fix_example: Optional example code showing how to fix the issue

    Returns:
        A multi-line TODO comment with detailed suggestions
    """
    desc = getattr(issue, 'description', "Energy issue detected")
    suggestion = getattr(issue, 'suggestion', "")
    impact = getattr(issue, 'impact', 0.0)
    gain = getattr(issue, 'optimization_gain', 0.0)
    issue_type = getattr(issue, 'issue_type', "")

    comment = f"// TODO ENERGY OPTIMIZATION: {desc}\n"

    # Add context-specific suggestions
    if "busy_wait" in issue_type or "busy_wait_pattern" in issue_type:
        if "while (1)" in line or "while(1)" in line:
            comment += f"// Zalecenie: {suggestion}\n"
            comment += "// Użyj trybu niskiego poboru mocy z przerwaniami zamiast aktywnego oczekiwania:\n"
            comment += "// _BIS_SR(LPM3_bits + GIE); // CPU śpi, przerwania wybudzają\n"
        elif "for" in line and "delay" in line.lower():
            comment += f"// Zalecenie: {suggestion}\n"
            comment += "// Użyj Timer_A z przerwaniem zamiast aktywnego oczekiwania:\n"
            comment += "// TA0CCR0 = 1000; // Ustaw timer\n"
            comment += "// TA0CCTL0 = CCIE; // Włącz przerwanie\n"
            comment += "// TA0CTL = TASSEL_2 + MC_1 + ID_3; // Uruchom timer\n"
            comment += "// _BIS_SR(LPM3_bits + GIE); // CPU śpi, timer wybudzi przez przerwanie\n"
        else:
            comment += f"// Zalecenie: {suggestion}\n"

    elif "adc" in issue_type.lower():
        comment += f"// Zalecenie: {suggestion}\n"
        comment += "// Optymalizuj konfigurację ADC dla oszczędności energii:\n"
        comment += "// ADC12CTL0 = ADC12SHT_0 + ADC12ON; // Najkrótszy czas próbkowania\n"
        comment += "// ADC12CTL1 = ADC12SHP; // Timer próbkowania\n"
        comment += "// ADC12CTL2 = ADC12RES_1; // 10-bit dla mniejszego zużycia energii gdy wystarczy\n"

    elif "peripheral_not_disabled" in issue_type:
        peripheral_type = detect_peripheral_type(line)
        comment += f"// Zalecenie: {suggestion}\n"
        comment += f"// Wyłącz {peripheral_type} po użyciu, aby zmniejszyć zużycie energii:\n"
        if "UART" in peripheral_type or "UCA" in peripheral_type:
            comment += "// UCA0CTL1 |= UCSWRST; // Reset modułu UART\n"
            comment += "// UCA0IE &= ~(UCRXIE + UCTXIE); // Wyłącz przerwania UART\n"
        elif "SPI" in peripheral_type or "UCB" in peripheral_type:
            comment += "// UCB0CTL1 |= UCSWRST; // Reset modułu SPI\n"
        elif "ADC" in peripheral_type:
            comment += "// ADC12CTL0 &= ~ADC12ON; // Wyłącz ADC\n"
        elif "Timer" in peripheral_type:
            comment += "// TA0CTL &= ~MC_3; // Zatrzymaj timer\n"

    elif "clock" in issue_type.lower():
        comment += f"// Zalecenie: {suggestion}\n"
        comment += "// Dostosuj częstotliwość zegara do wymagań:\n"
        comment += "// if (!high_performance_needed) {\n"
        comment += "//   BCSCTL1 = CALBC1_1MHZ; // Użyj 1MHz zamiast wyższych częstotliwości\n"
        comment += "//   DCOCTL = CALDCO_1MHZ;\n"
        comment += "// }\n"

    # Add technical details if available
    if hasattr(issue, 'technical_details') and issue.technical_details:
        comment += f"// Szczegóły techniczne: {issue.technical_details}\n"

    # Add impact and potential gain
    if impact > 0 or gain > 0:
        comment += f"// Wpływ: {impact:.2f}, Potencjalne oszczędności energii: {gain*100:.1f}%\n"

    # Add custom fix example if provided or use the default one
    if fix_example:
        comment += f"// Przykład poprawki:\n// {fix_example}\n"

    # Add references if available
    if hasattr(issue, 'references') and issue.references:
        comment += f"// Referencje: {', '.join(issue.references)}\n"

    return comment


def generate_fix_suggestion(issue: Any, line: str) -> str:
    """
    Generate more specific fix suggestion based on issue type and line of code.

    Args:
        issue: Energy issue object with information about the detected issue
        line: The line of code where the issue was detected

    Returns:
        A context-specific fix suggestion
    """
    issue_type = getattr(issue, 'issue_type', "")

    if "busy_wait" in issue_type or "polling" in issue_type:
        if "while" in line and ("1" in line or "true" in line.lower()):
            return "Zastąp aktywne oczekiwanie trybem LPM z przerwaniami:\n// /* Przygotuj obsługę przerwania */\n// __bis_SR_register(LPM3_bits + GIE); // Przejdź w tryb LPM3 z włączonymi przerwaniami"
        elif "for" in line and "delay" in line.lower():
            return "Zastąp pętlę opóźniającą timerem z przerwaniem:\n// TA0CCR0 = 1000; // Ustaw timer\n// TA0CCTL0 = CCIE; // Włącz przerwanie\n// TA0CTL = TASSEL_2 + MC_1; // Uruchom timer\n// __bis_SR_register(LPM3_bits + GIE); // Przejdź w tryb LPM3, timer wybudzi przez przerwanie"
        else:
            return "Zamień aktywne oczekiwanie na tryb LPM z przerwaniami:\n// __bis_SR_register(LPM3_bits + GIE); // Użyj trybu LPM3 z włączonymi przerwaniami"

    elif "sleep_mode" in issue_type:
        if "LPM0" in line:
            return "Zastosuj głębszy tryb uśpienia:\n// __bis_SR_register(LPM3_bits); // Użyj LPM3 zamiast LPM0 dla znaczących oszczędności energii"
        else:
            return "Zastosuj głębszy tryb uśpienia:\n// __bis_SR_register(LPM3_bits); // LPM3 zużywa znacząco mniej energii niż LPM0/LPM1"

    elif "loop" in issue_type and ("unnecessary" in issue_type or "inefficient" in issue_type):
        invariant = find_invariant_operation(line)
        if invariant:
            return f"Przenieś niezmienne operacje poza pętlę:\n// {invariant} = obliczenie(); // Oblicz raz przed pętlą\n// for(...) {{ użyj {invariant} zamiast powtarzać obliczenia }}"
        else:
            return "Przenieś niezmienne operacje i obliczenia poza pętlę:\n// wynik = obliczenie(); // Oblicz raz przed pętlę\n// for(i=0; i<n; i++) { użyj 'wynik' }"

    elif "peripheral_not_disabled" in issue_type:
        peripheral = detect_peripheral_type(line)
        if "UART" in peripheral or "UCA" in peripheral:
            return f"Po zakończeniu użytkowania {peripheral}:\n// UCA0CTL1 |= UCSWRST; // Zresetuj {peripheral}\n// UCA0IE &= ~(UCRXIE + UCTXIE); // Wyłącz przerwania {peripheral}"
        elif "SPI" in peripheral or "UCB" in peripheral:
            return f"Po zakończeniu użytkowania {peripheral}:\n// UCB0CTL1 |= UCSWRST; // Zresetuj {peripheral}\n// UCB0IE &= ~UCRXIE; // Wyłącz przerwania {peripheral}"
        elif "ADC" in peripheral:
            return f"Po zakończeniu użytkowania {peripheral}:\n// ADC12CTL0 &= ~ADC12ON; // Wyłącz {peripheral} gdy nie jest używane"
        elif "Timer" in peripheral:
            return f"Po zakończeniu użytkowania {peripheral}:\n// TA0CTL &= ~MC_3; // Zatrzymaj {peripheral}\n// TA0IE &= ~TAIE; // Wyłącz przerwania {peripheral}"
        else:
            return f"Po zakończeniu użytkowania {peripheral}:\n// {peripheral}_disable(); // Wyłącz {peripheral} gdy nie jest używane"

    elif "adc" in issue_type.lower() or "suboptimal_adc" in issue_type:
        return "Zoptymalizuj konfigurację ADC dla oszczędności energii:\n// ADC12CTL0 = ADC12SHT_0 + ADC12ON; // Użyj najkrótszego czasu próbkowania gdy pozwala na to sygnał\n// ADC12CTL2 = ADC12RES_1; // Użyj 10-bit rozdzielczości gdy wystarczy"

    elif "clock" in issue_type:
        if "BCSCTL" in line or "DCOCTL" in line:
            return "Dostosuj częstotliwość zegara do potrzeb:\n// if (!high_performance_needed) {\n//   BCSCTL1 = CALBC1_1MHZ; // Użyj niższej częstotliwości gdy to możliwe\n//   DCOCTL = CALDCO_1MHZ;\n// }"
        else:
            return "Wyłącz nieużywane zegary:\n// BCSCTL2 &= ~SELS; // Wyłącz nieużywane źródło zegara\n// BCSCTL3 |= LFXT1S_0; // Wyłącz oscylator kryształu gdy nie jest potrzebny"

    elif "pin" in issue_type or "port" in issue_type or "gpio" in issue_type:
        return "Poprawnie skonfiguruj piny GPIO:\n// P1DIR |= BIT0; // Najpierw ustaw kierunek\n// P1OUT |= BIT0; // Potem ustaw wartość\n// P1REN |= BIT1; // Włącz rezystor podciągający/ściągający dla wejść"

    else:
        return getattr(issue, 'suggestion', "Zoptymalizuj ten fragment kodu pod kątem zużycia energii")


def find_invariant_operation(line: str) -> Optional[str]:
    """
    Try to identify potential loop-invariant operations in the code line.

    Args:
        line: The line of code to analyze

    Returns:
        The identified invariant operation or None if none found
    """
    # Look for function calls that might be invariant
    function_match = re.search(r'(\w+)\s*\([^)]*\)', line)
    if function_match:
        return function_match.group(1) + "()"

    # Look for variable assignments that might involve invariant computations
    assignment_match = re.search(r'(\w+)\s*=\s*[^;]+', line)
    if assignment_match:
        return assignment_match.group(1)

    # Look for arithmetic operations that might be invariant
    math_op_match = re.search(r'(\w+)\s*[\+\-\*\/]\s*\w+', line)
    if math_op_match:
        return math_op_match.group(0)

    return None


def detect_peripheral_type(line: str) -> str:
    """
    Detect the peripheral type from the code line.

    Args:
        line: The line of code to analyze

    Returns:
        The detected peripheral type
    """
    if re.search(r'U[CS]A\d|UART', line, re.IGNORECASE):
        return "UART"
    elif re.search(r'UCB\d|SPI', line, re.IGNORECASE):
        return "SPI"
    elif re.search(r'ADC', line, re.IGNORECASE):
        return "ADC"
    elif re.search(r'TA\d|TB\d|Timer', line, re.IGNORECASE):
        return "Timer"
    elif re.search(r'P\d(OUT|DIR|REN)', line):
        return "GPIO"
    elif re.search(r'I2C', line, re.IGNORECASE):
        return "I2C"
    elif re.search(r'DMA', line, re.IGNORECASE):
        return "DMA"
    elif re.search(r'RTC', line, re.IGNORECASE):
        return "RTC"
    elif re.search(r'WDT', line, re.IGNORECASE):
        return "Watchdog"
    elif re.search(r'BCSCTL|DCOCTL|UCS', line, re.IGNORECASE):
        return "Clock"
    else:
        return "peryferia"


def match_code_pattern(pattern_type: str, line: str) -> bool:
    """
    Check if a line of code matches a specific energy pattern.

    Args:
        pattern_type: The type of pattern to check for
        line: The line of code to analyze

    Returns:
        True if the line matches the pattern, False otherwise
    """
    patterns = {
        'busy_wait': r'while\s*\(\s*1\s*\)|for\s*\([^;]*;[^;]*;[^)]*\)\s*;|while\s*\(.*?true.*?\)',
        'delay_loop': r'for\s*\(\s*\w+\s*=\s*0\s*;\s*\w+\s*<\s*[0-9]+\s*;\s*\w+\+\+\s*\)',
        'high_freq_config': r'(DCOCTL|BCSCTL|UCSCTL)\d*\s*=.*?(_16MHZ|_25MHZ|_20MHZ)',
        'missing_lpm': r'_BIS_SR\s*\(\s*[^L]',
        'polling': r'while\s*\(\s*!\s*\(\s*\w+\s*&\s*\w+\s*\)\s*\)',
        'unconfigured_pins': r'P\dOUT\s*[|&^]?=.*?(?![.\s\S]*?P\dDIR\s*[|&^]?=)',
        'adc_config': r'ADC12CTL0\s*[|]?=\s*(?!.*?ADC12SHT_0)',
        'uart_config': r'(UCA|UCB)\d(CTL1|IE)\s*[|]?=\s*UC(A|B)(\w+)(?![.\s\S]*?LPM[0-4])',
        'timer_config': r'TA\dCTL\s*=\s*(?!.*?MC__STOP)',
    }

    if pattern_type in patterns:
        return bool(re.search(patterns[pattern_type], line))
    return False