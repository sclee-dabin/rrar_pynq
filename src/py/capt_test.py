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


def _sa_dma_reset(dmareg):
    timeout = 10
    dmareg.write(0x30, 0x04)
    sleep(0.001)	# wait 1 msec
    while True:
        if ((dmareg.read(0x30) & 0x04) == 0): 
            print('[INFO] Reset SA DMA completed')
            break

        timeout -= 1
        if (timeout == 0):
            print('[ERROR] Reset SA DMA Timeout Error')
            break

        sleep(0.001)	# wait 1 msec

"""
#-------------------------------------
*
* Capture Test 
*
*	capt_stat(0)	: sa_capt_done
*	capt_stat(1)	: ddr_init_cal_done
*	capt_stat(2)	: dma_ready
*	capt_stat(3)	: rx_capt_done
*
#-------------------------------------
"""

def _capt_test(pl, src, len, dma, buf, dmareg, tpg, debug):
    if (debug): print('------ Call capt_test ------')
    ctrl1 = ((tpg & 1) << 16)| (src & 0xf)
    ctrl2 = (len & 0x3fffffff)

    #
    # 1. Set Capture Source
    #
    PL_CTRL_Write(pl, CAPT_CTRL1, ctrl1)
    PL_CTRL_Write(pl, CAPT_CTRL2, ctrl2)
    if (debug): print('Debug Pos 1 --- CAPT_CTRL2(0x%04x): 0x%08x'%(CAPT_CTRL2, PL_CTRL_Read(pl, CAPT_CTRL2)))

    #return False
    #sleep(0.000001)
    #
    # 2. SA data acquisition
    #
    PL_CTRL_Write(pl, CAPT_CTRL2, (SET_SA_START | ctrl2))
    if (debug): print('Debug Pos 2 --- CAPT_CTRL2(0x%04x): 0x%08x'%(CAPT_CTRL2, PL_CTRL_Read(pl, CAPT_CTRL2)))

    timeout = 10 	# 100 msec
    while True:
        sleep(0.01)	# wait 10 msec
        temp = PL_CTRL_Read(pl, CAPT_STAT)
        if (debug): print('CAPT_STATUS--1 0x%x'%(temp))
        if(temp & 0x1):     # check sa_capt_done flag 
            break
        if (debug): print('CAPT_STATUS--2 0x%x'%(temp))
        timeout -= 1
        if (timeout == 0):
            raise Exception('[ERROR]SA data acquisition Timeout')
            raise Exception('Clear SA_START before EXIT')
            PL_CTRL_Write(pl, CAPT_CTRL2, (ctrl2 & 0x3fffffff))
            return False

    # Wait 1 msec to give time saving data to DDR4 memory
    sleep(0.001) 		

    #
    # 3. RX DMA to transfer
    #
    PL_CTRL_Write(pl, CAPT_CTRL2, ctrl2)

    # kick off DMA 
    if (debug): print('3-1) Kick off DMA engine')
    dma.recvchannel.transfer(buf)
  
    if (debug): 
        print('0x%x=0x%08x'%(0x30, dmareg.read(0x30)))
        print('0x%x=0x%08x'%(0x34, dmareg.read(0x34)))
        print('0x%x=0x%08x'%(0x48, dmareg.read(0x48)))
        print('0x%x=0x%08x'%(0x4c, dmareg.read(0x4c)))
        print('0x%x=0x%08x'%(0x58, dmareg.read(0x58)))  
    
    if (debug): print('3-2) set PL RX DMA start')
    PL_CTRL_Write(pl, CAPT_CTRL2, (SET_RX_START | ctrl2))	# set RX DMA start 
    
    if (debug): print('3-3) wait DMA completed')
    dma.recvchannel.wait()
    
    # check DMA END flag 
    if (debug): print('After RX, CAPT_STAT register : 0x%x'%(PL_CTRL_Read(pl, CAPT_STAT)))

    # Clear registers 
    PL_CTRL_Write(pl, CAPT_CTRL2, 0)
    if (debug): print('Debug Pos 3 --- CAPT_CTRL2(0x%04x): 0x%08x'%(CAPT_CTRL2, PL_CTRL_Read(pl, CAPT_CTRL2)))
    #SA_DMA_Write(AXI_S2MM_DMA_LENGTH, 0)
    #SA_DMA_Write(AXI_S2MM_DMA_CTRL, 0)

    if (debug): print('SA DMA : %d bytes completed'%(len))

    return True

