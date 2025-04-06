"""Test configuration and fixtures for pytest."""

import os
import sys
import tempfile

import pytest

# Add the src directory to the path so we can import the package
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../src')))


@pytest.fixture
def temp_project_dir():
    """Create a temporary directory for test projects."""
    with tempfile.TemporaryDirectory() as temp_dir:
        yield temp_dir


@pytest.fixture
def sample_c_file(temp_project_dir):
    """Create a sample C file for testing."""
    file_path = os.path.join(temp_project_dir, "sample.c")

    with open(file_path, 'w') as f:
        f.write("""
#include <msp430.h>

// Main function
int main(void) {
    // Stop watchdog timer
    WDTCTL = WDTPW | WDTHOLD;
    
    // Configure clock
    BCSCTL1 = CALBC1_16MHZ;
    DCOCTL = CALDCO_16MHZ;
    
    // Configure LED on P1.0
    P1OUT = 0x00;
    P1DIR = 0x01;
    
    // Main loop
    while(1) {
        // Toggle LED
        P1OUT ^= 0x01;
        
        // Delay
        volatile unsigned int i;
        for(i=0; i<50000; i++);
        
        // Enter LPM0 with interrupts enabled
        _BIS_SR(LPM0_bits + GIE);
    }
}

// Timer A0 interrupt service routine
#pragma vector=TIMER0_A0_VECTOR
__interrupt void Timer_A (void) {
    // Wake up from LPM0
    _BIC_SR_IRQ(LPM0_bits);
}
""")

    return file_path


@pytest.fixture
def sample_header_file(temp_project_dir):
    """Create a sample header file for testing."""
    file_path = os.path.join(temp_project_dir, "config.h")

    with open(file_path, 'w') as f:
        f.write("""
#ifndef CONFIG_H
#define CONFIG_H

// Clock configuration
#define CLOCK_FREQ_MHZ 16
#define USE_DCO 1

// Low power mode configuration
#define DEFAULT_SLEEP_MODE LPM0
#define ENABLE_DEEP_SLEEP 0

// Peripheral configuration
#define ENABLE_ADC 1
#define ENABLE_UART 1
#define ENABLE_SPI 0
#define ENABLE_I2C 0

#endif // CONFIG_H
""")

    return file_path


@pytest.fixture
def sample_project(temp_project_dir, sample_c_file, sample_header_file):
    """Create a sample project with multiple files for testing."""
    return temp_project_dir