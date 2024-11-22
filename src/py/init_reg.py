from time import sleep
from glbvar import *

#-------------------------------------
# PL register access
#-------------------------------------
def PL_CTRL_Write(pl, addr, val):
    pl.write(addr,val)

def PL_CTRL_Read(pl, addr):
    tmp=pl.read(addr)
    return tmp

#-------------------------------------
# Control Delay Register
#-------------------------------------
def idly_ctrl(pl, rx, idly):
    print('[INFO] idly_ctrl rx %d , delay %d'%(rx, idly))
    tmp = 0

    if ((idly < 0) or (idly > 511)):
        print('[ERROR] Invalid Range [0~511]:%d'%idly)
        return False

    if (rx == RX1):
        tmp = PL_CTRL_Read(pl, DLY_CTRL1)
    if (rx == RX2):
        tmp = PL_CTRL_Read(pl, DLY_CTRL2)

    tmp = ((tmp & 0xffff0000) | (idly & 0x3FF))

    if (rx == RX1):
        PL_CTRL_Write(pl, DLY_CTRL1, tmp)
        PL_CTRL_Write(pl, DLY_CTRL1, (IDLY_RST | tmp))
        PL_CTRL_Write(pl, DLY_CTRL1, tmp)
    elif (rx == RX2):
        PL_CTRL_Write(pl, DLY_CTRL2, tmp)
        PL_CTRL_Write(pl, DLY_CTRL2, (IDLY_RST | tmp))
        PL_CTRL_Write(pl, DLY_CTRL2, tmp)
    else:
        print('[ERROR] Unknown RX path %d'%rx)

    return True


def fdly_ctrl(pl, rx, fdly):
    print('[INFO] fdly_ctrl rx %d , delay %d'%(rx,fdly))
    tmp = 0

    if ((fdly < 0) or (fdly > 255)):
        print('[ERROR] Invalid Range FDLY=%d [0~255]'%fdly)
        return False

    if (rx == RX1):
        tmp = PL_CTRL_Read(pl, DLY_CTRL1)
    if (rx == RX2):
        tmp = PL_CTRL_Read(pl, DLY_CTRL2)

    tmp = ((tmp & 0xffff) | ((fdly & 0xFF) << 16))

    if (rx == RX1):
        PL_CTRL_Write(pl, DLY_CTRL1, tmp)
        PL_CTRL_Write(pl, DLY_CTRL1, (FDLY_RELOAD | tmp))
        PL_CTRL_Write(pl, DLY_CTRL1, tmp)
    elif (rx == RX2):
        PL_CTRL_Write(pl, DLY_CTRL2, tmp)
        PL_CTRL_Write(pl, DLY_CTRL2, (FDLY_RELOAD | tmp))
        PL_CTRL_Write(pl, DLY_CTRL2, tmp)
    else:
        print('[ERROR] Unknown RX path %d'%rx)

    return True

#-------------------------------------
# Set registers as Default value
#-------------------------------------
def _set_default(pl):
    print('Set PL Register as Default value')
    
    """// Set Main control register
    31-20 	reserved
    19-18 	RSMP_CTRL2 		Re-Sampler Path2 Control
                            0 245.76Msps
                            1 122.88Msps
                            2 61.44Msps
                            3 30.72Msps
    17-16 	RSMP_CTRL1 		Re-Sampler Path1 Control
                            0 245.76Msps
                            1 122.88Msps
                            2 61.44Msps
                            3 30.72Msps
    15-10 	reserved						
    9 		TRIG_MODE 		Timing Reference Counter Mode
                            0 : Internal
                            1 : External
    8 		CORR_MODE 		Select Correlation Mode
                            0 : Run Auto Correlation mode
                            1 : Run Downlink TCB/FCB mode
    7-5  	reserved
    4 		CDC_RST
    3 		AFE_RST
    2-0  	reserved
    """

    PL_CTRL_Write(pl, MAIN_CTRL, 0xF0000)

    # Bypass Control 
    PL_CTRL_Write(pl, BYPASS_CTRL, 0)

    # Timing reference period
    PL_CTRL_Write(pl, TREF_CTRL, PERIOD_1MSEC)

    # phase control 
    PL_CTRL_Write(pl, PHAZ_CTRL1, RX1_PHAZ)
    PL_CTRL_Write(pl, PHAZ_CTRL2, RX2_PHAZ)

    # gain control 
    PL_CTRL_Write(pl, GAIN_CTRL1, UNITY_GAIN)
    PL_CTRL_Write(pl, GAIN_CTRL2, UNITY_GAIN)	

    idly_ctrl(pl, RX1, 0)  #// rx1, i delay = 0
    idly_ctrl(pl, RX2, 0)  #// rx2, i delay = 0
    fdly_ctrl(pl, RX1, 0)  #// rx1, f delay = 0
    fdly_ctrl(pl, RX2, 0)  #// rx2, f delay = 0

    #// Correlation block 
    PL_CTRL_Write(pl, CORR_CTRL1, 0)
    PL_CTRL_Write(pl, CORR_CTRL2, 0)
    PL_CTRL_Write(pl, CORR_CTRL3, 0)

    #// Dump Registers
    print('[INFO] Dump Registers')
    print('MAIN_STAT    :' , hex(MAIN_STAT) ,   hex(PL_CTRL_Read(pl, MAIN_STAT)		))
    print('MAIN_CTRL    :' , hex(MAIN_CTRL) ,   hex(PL_CTRL_Read(pl, MAIN_CTRL)		))
    print('FPGA_VERSION :' , hex(FPGA_VERSION), hex(PL_CTRL_Read(pl, FPGA_VERSION)	))
    print('BYPASS_CTRL  :' , hex(BYPASS_CTRL),  hex(PL_CTRL_Read(pl, BYPASS_CTRL)	))
    print('TREF_CTRL    :' , hex(TREF_CTRL),    hex(PL_CTRL_Read(pl, TREF_CTRL)		))
    print('PERI_CTRL    :' , hex(PERI_CTRL),    hex(PL_CTRL_Read(pl, PERI_CTRL)		))
    print('CAPT_STAT    :' , hex(CAPT_STAT),    hex(PL_CTRL_Read(pl, CAPT_STAT)		))
    print('PHAZ_CTRL1   :' , hex(PHAZ_CTRL1),   hex(PL_CTRL_Read(pl, PHAZ_CTRL1)	))
    print('PHAZ_CTRL2   :' , hex(PHAZ_CTRL2),   hex(PL_CTRL_Read(pl, PHAZ_CTRL2)	))
    print('GAIN_CTRL1   :' , hex(GAIN_CTRL1),   hex(PL_CTRL_Read(pl, GAIN_CTRL1)	))
    print('GAIN_CTRL2   :' , hex(GAIN_CTRL2),   hex(PL_CTRL_Read(pl, GAIN_CTRL2)	))
    print('DLY_CTRL1    :' , hex(DLY_CTRL1),    hex(PL_CTRL_Read(pl, DLY_CTRL1)		))
    print('DLY_CTRL2    :' , hex(DLY_CTRL2),    hex(PL_CTRL_Read(pl, DLY_CTRL2)		))
    print('CAPT_CTRL1   :' , hex(CAPT_CTRL1),   hex(PL_CTRL_Read(pl, CAPT_CTRL1)	))
    print('CAPT_CTRL2   :' , hex(CAPT_CTRL2),   hex(PL_CTRL_Read(pl, CAPT_CTRL2)	))
    print('CORR_CTRL1   :' , hex(CORR_CTRL1),   hex(PL_CTRL_Read(pl, CORR_CTRL1)	))
    print('CORR_CTRL2   :' , hex(CORR_CTRL2),   hex(PL_CTRL_Read(pl, CORR_CTRL2)	))
    print('CORR_CTRL3   :' , hex(CORR_CTRL3),   hex(PL_CTRL_Read(pl, CORR_CTRL3)	))
    print('CORR_STAT1   :' , hex(CORR_STAT1),   hex(PL_CTRL_Read(pl, CORR_STAT1)	))
    print('CORR_STAT2   :' , hex(CORR_STAT2),   hex(PL_CTRL_Read(pl, CORR_STAT2)	))

