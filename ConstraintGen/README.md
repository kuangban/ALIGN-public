## Dependencies

- Python 3.6
- networkx
    For graph data processing/manipulation
    https://networkx.github.io/
    Open source 3-clause BSD license
- pyspice
    For spice netlist parsing
    https://pyspice.fabrice-salvaire.fr/
    GPLv3

To install:
````
pip install networkx
pip install wheel pyspice
````

## Run example

````
cd ./sandbox
python ../src/python/cgraph.py ../../Database/netlists_wo_sizing/gondi_jssc2007_ctle.sp --plot --with_label --dir_graph_out=./
python ../src/python/cgraph.py ../../Database/netlists_wo_sizing/gondi_jssc2007_ctle.sp --plot --with_label --dir_graph_out=./ --add_edge_annotation
````

## List of Circuit Classes to Cover
````
Serial IO (embedded clock architecture)
    TX
        LE/FFE
        Serializer | Multiplexer
            Quarter | Half | Full-rate
        Driver
            Single-ended | Differential
            Current-mode | voltage mode
        Duty cycle corrector
        Clock encoder
    RX
        LE
            CTLE + [LFEQ]
            VGA
        DFE
            Summer
            Slicer
            DAC
        Slicer/Sampler
            strongARM
            CML
        T/H, Buffer
        CDR
            PFD, LF, VCO, DIV
        DLL+PI | VCO
        Deserializer

Parallel Interface (forwarded clock architecture)
    TX
        Similar to Serial IO TX
    RX
        Similar to Serial IO RX except CDR
    DLL | PLL
        Phase interpolator
    Equalizer to suppress coupled signal

Clock synthesizer
    PLL

Clock distribution

Reference clock generation

ESD/termination/output pad network

Phase locked loop (PLL)
    PFD
    CP
    TDC
    LF
    VCO
    DCO
    DIV

Delay locked loop (DLL)
    VCDL
    PFD
    CP
    Bias

Phase interpolator

Clock data recovery (CDR)

Voltage regulator
    LDO
    Switching DC-DC
        Switched cap
        Inductor based …
    Bandgap reference 

RF
    TX
        Power amplifier
    PLL
    RX
        Mixer
        LNA
        ADC
        AGC

ADC
    Delta-sigma 
    SAR
    Flash
    Pipeline
    Dual-slope

DAC

SRAM
    Memory cell
    Sense amplifer

Sensors
    Temperature
    Current
        Resistor+opamp
    Voltage
        Ring-osc based
````
