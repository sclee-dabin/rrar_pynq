import spidev
from time import sleep

_lmk_regs_grp1 = [
#	([0x00, 0x00, 0x80]),
#	([0x00, 0x00, 0x00]),
#	([0x00, 0x00, 0x80]),
#	([0x00, 0x00, 0x00]),
#	([0x00, 0x00, 0x80]),
#	([0x00, 0x00, 0x00]),
#	([0x01, 0x4a, 0x03]),
#	([0x01, 0x4a, 0x33]),
#	([0x00, 0x00, 0x00]),
	([0x00, 0x02, 0x00]),
	([0x01, 0x00, 0x18]),
	([0x01, 0x00, 0x18]),
	([0x01, 0x00, 0x18]),
	([0x01, 0x01, 0x55]),
	([0x01, 0x01, 0x55]),
	([0x01, 0x03, 0x01]),
	([0x01, 0x03, 0x01]),
	([0x01, 0x03, 0x01]),
	([0x01, 0x04, 0x00]),
	([0x01, 0x04, 0x00]),
	([0x01, 0x04, 0x20]),
	([0x01, 0x04, 0x20]),
	([0x01, 0x05, 0x00]),
	([0x01, 0x05, 0x00]),
	([0x01, 0x06, 0x18]),
	([0x01, 0x06, 0x18]),
	([0x01, 0x06, 0x10]),
	([0x01, 0x06, 0x10]),
	([0x01, 0x06, 0x90]),
	([0x01, 0x06, 0xf0]),
	([0x01, 0x07, 0x01]),
	([0x01, 0x07, 0x01]),
	([0x01, 0x07, 0x11]),
	([0x01, 0x07, 0x11]),
	([0x01, 0x08, 0x06]),
	([0x01, 0x08, 0x26]),
	([0x01, 0x08, 0x66]),
	([0x01, 0x09, 0x55]),
	([0x01, 0x09, 0x55]),
	([0x01, 0x0b, 0x01]),
	([0x01, 0x0b, 0x01]),
	([0x01, 0x0b, 0x01]),
	([0x01, 0x0c, 0x00]),
	([0x01, 0x0c, 0x00]),
	([0x01, 0x0c, 0x20]),
	([0x01, 0x0c, 0x20]),
	([0x01, 0x0d, 0x00]),
	([0x01, 0x0d, 0x00]),
	([0x01, 0x0e, 0x18]),
	([0x01, 0x0e, 0x18]),
	([0x01, 0x0e, 0x10]),
	([0x01, 0x0e, 0x10]),
	([0x01, 0x0e, 0x90]),
	([0x01, 0x0e, 0xf0]),
	([0x01, 0x0f, 0x04]),
	([0x01, 0x0f, 0x04]),
	([0x01, 0x0f, 0x14]),
	([0x01, 0x0f, 0x14]),
	([0x01, 0x10, 0x08]),
	([0x01, 0x10, 0x08]),
	([0x01, 0x10, 0x08]),
	([0x01, 0x11, 0x55]),
	([0x01, 0x11, 0x55]),
	([0x01, 0x13, 0x00]),
	([0x01, 0x13, 0x00]),
	([0x01, 0x13, 0x00]),
	([0x01, 0x14, 0x00]),
	([0x01, 0x14, 0x00]),
	([0x01, 0x14, 0x00]),
	([0x01, 0x14, 0x00]),
	([0x01, 0x15, 0x00]),
	([0x01, 0x15, 0x00]),
	([0x01, 0x16, 0x11]),
	([0x01, 0x16, 0x11]),
	([0x01, 0x16, 0x19]),
	([0x01, 0x16, 0x19]),
	([0x01, 0x16, 0x99]),
	([0x01, 0x16, 0xf9]),
	([0x01, 0x17, 0x00]),
	([0x01, 0x17, 0x00]),
	([0x01, 0x17, 0x00]),
	([0x01, 0x17, 0x00]),
	([0x01, 0x18, 0x18]),
	([0x01, 0x18, 0x18]),
	([0x01, 0x18, 0x18]),
	([0x01, 0x19, 0x55]),
	([0x01, 0x19, 0x55]),
	([0x01, 0x1b, 0x00]),
	([0x01, 0x1b, 0x00]),
	([0x01, 0x1b, 0x00]),
	([0x01, 0x1c, 0x00]),
	([0x01, 0x1c, 0x00]),
	([0x01, 0x1c, 0x20]),
	([0x01, 0x1c, 0x20]),
	([0x01, 0x1d, 0x00]),
	([0x01, 0x1d, 0x00]),
	([0x01, 0x1e, 0x11]),
	([0x01, 0x1e, 0x11]),
	([0x01, 0x1e, 0x19]),
	([0x01, 0x1e, 0x19]),
	([0x01, 0x1e, 0x99]),
	([0x01, 0x1e, 0xf9]),
	([0x01, 0x1f, 0x00]),
	([0x01, 0x1f, 0x00]),
	([0x01, 0x1f, 0x00]),
	([0x01, 0x1f, 0x00]),
	([0x01, 0x20, 0x0c]),
	([0x01, 0x20, 0x0c]),
	([0x01, 0x20, 0x0c]),
	([0x01, 0x21, 0x55]),
	([0x01, 0x21, 0x55]),
	([0x01, 0x23, 0x00]),
	([0x01, 0x23, 0x00]),
	([0x01, 0x23, 0x00]),
	([0x01, 0x24, 0x00]),
	([0x01, 0x24, 0x00]),
	([0x01, 0x24, 0x00]),
	([0x01, 0x24, 0x00]),
	([0x01, 0x25, 0x00]),
	([0x01, 0x25, 0x00]),
	([0x01, 0x26, 0x11]),
	([0x01, 0x26, 0x11]),
	([0x01, 0x26, 0x19]),
	([0x01, 0x26, 0x19]),
	([0x01, 0x26, 0x99]),
	([0x01, 0x26, 0xf9]),
	([0x01, 0x27, 0x01]),
	([0x01, 0x27, 0x01]),
	([0x01, 0x27, 0x11]),
	([0x01, 0x27, 0x11]),
	([0x01, 0x28, 0x08]),
	([0x01, 0x28, 0x08]),
	([0x01, 0x28, 0x08]),
	([0x01, 0x29, 0x55]),
	([0x01, 0x29, 0x55]),
	([0x01, 0x2b, 0x00]),
	([0x01, 0x2b, 0x00]),
	([0x01, 0x2b, 0x00]),
	([0x01, 0x2c, 0x00]),
	([0x01, 0x2c, 0x00]),
	([0x01, 0x2c, 0x00]),
	([0x01, 0x2c, 0x00]),
	([0x01, 0x2d, 0x00]),
	([0x01, 0x2d, 0x00]),
	([0x01, 0x2e, 0x11]),
	([0x01, 0x2e, 0x11]),
	([0x01, 0x2e, 0x19]),
	([0x01, 0x2e, 0x19]),
	([0x01, 0x2e, 0x99]),
	([0x01, 0x2e, 0xf9]),
	([0x01, 0x2f, 0x00]),
	([0x01, 0x2f, 0x00]),
	([0x01, 0x2f, 0x00]),
	([0x01, 0x2f, 0x00]),
	([0x01, 0x30, 0x18]),
	([0x01, 0x30, 0x18]),
	([0x01, 0x30, 0x18]),
	([0x01, 0x31, 0x55]),
	([0x01, 0x31, 0x55]),
	([0x01, 0x33, 0x01]),
	([0x01, 0x33, 0x01]),
	([0x01, 0x34, 0x00]),
	([0x01, 0x34, 0x00]),
	([0x01, 0x34, 0x20]),
	([0x01, 0x34, 0x20]),
	([0x01, 0x35, 0x00]),
	([0x01, 0x35, 0x00]),
	([0x01, 0x36, 0x19]),
	([0x01, 0x36, 0x19]),
	([0x01, 0x36, 0x11]),
	([0x01, 0x36, 0x11]),
	([0x01, 0x36, 0x91]),
	([0x01, 0x36, 0xf1]),
	([0x01, 0x37, 0x01]),
	([0x01, 0x37, 0x01]),
	([0x01, 0x37, 0x01]),
	([0x01, 0x37, 0x01]),
	([0x01, 0x38, 0x00]),
	([0x01, 0x38, 0x00]),
	([0x01, 0x38, 0x20]),
	([0x01, 0x39, 0x03]),
	([0x01, 0x39, 0x03]),
	([0x01, 0x3b, 0x00]),
	([0x01, 0x3a, 0x03]),
	([0x01, 0x3d, 0x08]),
	([0x01, 0x3c, 0x00]),
	([0x01, 0x3e, 0x03]),
	([0x01, 0x3f, 0x00]),
	([0x01, 0x3f, 0x00]),
	([0x01, 0x3f, 0x00]),
	([0x01, 0x3f, 0x00]),
	([0x01, 0x40, 0x06]),
	([0x01, 0x40, 0x04]),
	([0x01, 0x40, 0x00]),
	([0x01, 0x40, 0x00]),
	([0x01, 0x40, 0x00]),
	([0x01, 0x40, 0x00]),
	([0x01, 0x40, 0x00]),
	([0x01, 0x40, 0x00]),
	([0x01, 0x41, 0x00]),
	([0x01, 0x41, 0x00]),
	([0x01, 0x41, 0x00]),
	([0x01, 0x41, 0x00]),
	([0x01, 0x41, 0x00]),
	([0x01, 0x41, 0x00]),
	([0x01, 0x41, 0x00]),
	([0x01, 0x41, 0x00]),
	([0x01, 0x42, 0x00]),
	([0x01, 0x43, 0x92]),
	([0x01, 0x43, 0x92]),
	([0x01, 0x43, 0x92]),
	([0x01, 0x43, 0x92]),
	([0x01, 0x43, 0x92]),
	([0x01, 0x43, 0x92]),
	([0x01, 0x43, 0x12]),
	([0x01, 0x44, 0x01]),
	([0x01, 0x44, 0x03]),
	([0x01, 0x44, 0x07]),
	([0x01, 0x44, 0x0f]),
	([0x01, 0x44, 0x1f]),
	([0x01, 0x44, 0x3f]),
	([0x01, 0x44, 0x7f]),
	([0x01, 0x44, 0xff]),
	([0x01, 0x46, 0x18]),
	([0x01, 0x46, 0x18]),
	([0x01, 0x46, 0x18]),
	([0x01, 0x46, 0x10]),
	([0x01, 0x46, 0x10]),
	([0x01, 0x46, 0x10]),
	([0x01, 0x47, 0x3a]),
	([0x01, 0x47, 0x3a]),
	([0x01, 0x47, 0x1a]),
	([0x01, 0x47, 0x1a]),
	([0x01, 0x48, 0x02]),
	([0x01, 0x48, 0x02]),
	([0x01, 0x49, 0x42]),
	([0x01, 0x49, 0x42]),
	([0x01, 0x49, 0x42]),
	([0x01, 0x4c, 0x00]),
	([0x01, 0x4b, 0x16]),
	([0x01, 0x4b, 0x16]),
	([0x01, 0x4b, 0x16]),
	([0x01, 0x4b, 0x16]),
	([0x01, 0x4b, 0x16]),
	([0x01, 0x4b, 0x16]),
	([0x01, 0x4d, 0x00]),
	([0x01, 0x4e, 0x00]),
	([0x01, 0x4e, 0xc0]),
	([0x01, 0x4f, 0x7f]),
	([0x01, 0x50, 0x03]),
	([0x01, 0x50, 0x03]),
	([0x01, 0x50, 0x03]),
	([0x01, 0x50, 0x03]),
	([0x01, 0x50, 0x03]),
	([0x01, 0x50, 0x43]),
	([0x01, 0x52, 0x00]),
	([0x01, 0x51, 0x02]),
	([0x01, 0x54, 0x78]),
	([0x01, 0x53, 0x00]),
	([0x01, 0x56, 0x7d]),
	([0x01, 0x55, 0x00]),
	([0x01, 0x58, 0x96]),
	([0x01, 0x57, 0x00]),
	([0x01, 0x5a, 0x00]),
	([0x01, 0x59, 0x06]),
	([0x01, 0x5b, 0xd4]),
	([0x01, 0x5b, 0xd4]),
	([0x01, 0x5b, 0xd4]),
	([0x01, 0x5b, 0xd4]),
	([0x01, 0x5d, 0x00]),
	([0x01, 0x5c, 0x20]),
	([0x01, 0x5e, 0x00]),
	([0x01, 0x5e, 0x00]),
	([0x01, 0x5f, 0x0b]),
	([0x01, 0x5f, 0x0b]),
	([0x01, 0x61, 0x01]),
	([0x01, 0x60, 0x00]),
	([0x01, 0x62, 0x5c]),
	([0x01, 0x62, 0x5c]),
	([0x01, 0x62, 0x44]),
	([0x01, 0x62, 0x44]),
	([0x01, 0x65, 0x0c]),
	([0x01, 0x64, 0x00]),
	([0x01, 0x63, 0x00]),
	([0x01, 0x66, 0x00]),
	([0x01, 0x68, 0x0c]),
	([0x01, 0x67, 0x00]),
	([0x01, 0x66, 0x00]),
	([0x01, 0x69, 0x59]),
	([0x01, 0x69, 0x59]),
	([0x01, 0x69, 0x59]),
	([0x01, 0x69, 0x59]),
	([0x01, 0x69, 0x59]),
	([0x01, 0x6b, 0x00]),
	([0x01, 0x6a, 0x20]),
	([0x01, 0x6c, 0x00]),
	([0x01, 0x6c, 0x00]),
	([0x01, 0x6d, 0x00]),
	([0x01, 0x6d, 0x00]),
	([0x01, 0x6e, 0x13]),
	([0x01, 0x6e, 0x13]),
	([0x01, 0x7c, 0x15]),
	([0x01, 0x7d, 0x0f]),
    ([0x80, 0x03, 0x00]),
    ([0x80, 0x04, 0x00]),
    ([0x80, 0x05, 0x00])    
    ]


_lmk_regs_grp3 = [
	([0x80, 0x03, 0x00]),
	([0x80, 0x04, 0x00]),
    ([0x80, 0x05, 0x00])
	]

"""
class rrar_lmk():
    
    def __init__(self):
        self._open()
        
    def _setup(self):
        print('Init LMK registers Group1')
        for reg in _lmk_regs_grp1:
            #print(reg)
            sdo=self.spi.xfer(reg)
            print(sdo)
            #sleep(0.01)
        
    def _open(self):
        print('Open LMK SPI device')
        self.spi=spidev.SpiDev()
        self.spi.open(2,0)
        print('Reset LMK/Disable 3-wire SPI mode')
        reg0x000 =[0x00,0x00,0x90]
        self.spi.xfer(reg0x000)
        sleep(0.01)

        print('Set RESET pin as SPI readback output')
        reg0x14a =[0x01,0x4a,0x33]
        self.spi.xfer(reg0x14a)

        print('Read reg3,4,5 -- ID registers to test SPI access')
        reg0x003 =[0x80,0x03,0x00]
        sdo=self.spi.xfer(reg0x003)
        print(sdo)

        reg0x004 =[0x80,0x04,0x00]
        sdo=self.spi.xfer(reg0x004)
        print(sdo)

        reg0x005 =[0x80,0x05,0x00]
        sdo=self.spi.xfer(reg0x005)
        print(sdo)        

    def _close(self):
         print('Close SPI device')
        self.spi.close()
   
"""   

def _lmksetup():
    print('Open LMK SPI device')
    spi=spidev.SpiDev()
    spi.open(2,0)

    print('Reset LMK/Disable 3-wire SPI mode')
    reg0x000 =[0x00,0x00,0x90]
    spi.xfer(reg0x000)
    sleep(0.01)

    print('Set RESET pin as SPI readback output')
    reg0x14a =[0x01,0x4a,0x33]
    spi.xfer(reg0x14a)

    reg0x003 =[0x80,0x03,0x00]
    sdo=spi.xfer(reg0x003)
    if (sdo[2] != 6):
        raise Exception("[ERROR] Unknown LMK ID!!")
    print('Read ID register(0x3): ', sdo[2])        
    
    """
    reg0x005 =[0x80,0x05,0x00]
    sdo=spi.xfer(reg0x005)
    print(sdo)

    reg0x004 =[0x80,0x04,0x00]
    sdo=spi.xfer(reg0x004)
    print(sdo)
    """  
    print('Init LMK registers Group1')
    for reg in _lmk_regs_grp1:
        #print(reg)
        tx_data = reg.copy()
        #print(tx_data[0])
        if tx_data[0]==128:
            WrRd='Read'
        else:
            WrRd='Write'
            
        #print(WrRd)    
        rd_addr = tx_data[1]
        sdo=spi.xfer(tx_data)
        if WrRd=='Read':
            #print(rd_addr)
            if ((rd_addr==3) and (sdo[2] !=6)):
                    raise Exception("[ERROR] LMK Unexpected LMK Reg3 Readout value!!")
            if ((rd_addr==4) and (sdo[2] !=208)):
                    raise Exception("[ERROR] LMK Unexpected LMK Reg3 Readout value!!")
            if ((rd_addr==5) and (sdo[2] !=91)):
                    raise Exception("[ERROR] LMK Unexpected LMK Reg3 Readout value!!")
            
            #print(sdo)
        #sleep(0.01)

    print('Close SPI device')
    spi.close()
    
