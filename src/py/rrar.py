import matplotlib.pyplot as plt
import numpy as np
from IPython.display import clear_output

from pynq import Overlay, GPIO, allocate, MMIO
from time import sleep

# custom python module
from init_reg import _set_default
from capt_test import _capt_test, _sa_dma_reset
from lmksetup import _lmksetup
from afesetup import rrar_afe
from glbvar import *

__author__  = "Sangcheol Lee"
__contact__ = "sangcheol.lee@dabinsystems.com"
__date__    = "2024/11/21"

BitStream   = '/home/xilinx/bit/bn017/rrarcvr_top.bit' 
SampleLen   = 32768
Chnum       = 2
src         = 0
bytelen     = SampleLen*Chnum*4
wordlen     = np.uint32(bytelen/4)
tpg         = 0
DebugPrint  = 0

class rrar():
    
    """Driver for RRAR core.
  
    Method of RRAR list
    --------------------
    _setup_clock      : setup LMK04828 clock device
    _setup_afe        : setup AFE7903 transcevier
    _set_LED          : set board ACT,ERR LED
    _init_jesdlink    : initialize FPGA Jesd link 
    _setup_pl_default : set PL registers to default
    _capture_once     : single capture for demo
    _plot_rx(ch)      : plot capture data , ch=1,2 or 12
    _m_capt           : capture/plot loop operation -- test2
    
    Attributes:
    ----------
        
    """    
    
    
    def __init__(self):
        print('==== Initialize RRAR Test program ====')
        ol = Overlay(BitStream)
        self.pl = ol.rrarcvr_core_0 
        self.dma = ol.capt_dma
        self.sadma_reg = MMIO(SADMA_BASE_ADDRESS, SADMA_ADDRESS_RANGE)
        self.rxbuf = allocate(shape=(wordlen,),dtype=np.uint32) 
        
        # Check board ID
        fpgaver=self.pl.read(FPGA_VERSION)
        board_id = (fpgaver >> 16) & 0xffff
        print('0x%08x, board:0x%04x'%(fpgaver, board_id))
        if (board_id != 0x7903):
            raise Exception("[ERROR]FPGA Board Version is Not Macthed!!")
        
    def _setup_clock(self):
        _lmksetup()
        print('==== Setup LMK Finished ====')
    
    def _setup_afe(self):
        # AFE7903 Power ON
        output = GPIO(361,'out')
        output.write(1)

        # AFE7903 reset/release
        self.pl.write(0x04,0x40)
        sleep(0.1)
        self.pl.write(0x04,0x00)

        afe=rrar_afe()
        afe._setup()
        afe._setnormal()
        print('==== Setup AFE Finished ====')
    
    def _set_LED(self):
        act_led_red = GPIO(366,'out')
        act_led_red.write(0)
        act_led_green = GPIO(367,'out')
        act_led_green.write(1)
        err_led_red = GPIO(368,'out')
        err_led_red.write(0)
        err_led_green = GPIO(369,'out')
        err_led_green.write(1)
        print('==== Set ACT,ERR LED Green ====')     
        
    def _init_jesdlink(self):
        # JESD Reset/Release
        reg=self.pl.read(0x0)
        print('Before mainstat', hex(reg))
        self.pl.write(0x04,0x07)
        sleep(0.1)
        self.pl.write(0x04,0x00)
        reg=self.pl.read(0x4)
        #print('mainctrl', hex(reg))
        sleep(0.1)
        reg=self.pl.read(0x0)
        print('After mainstat', hex(reg)) 
        
    def _setup_pl_default(self):
        _set_default(self.pl)
        
    def _capture_once(self, debug=1):
        _capt_test(self.pl,src,bytelen,self.dma,self.rxbuf,self.sadma_reg,tpg,debug)
        
    def _plot_rx(self,ch=1):
        """A plot method for capture data
        Select channel number to plot 
        1  = channel 1 (default)
        2  = channel 2
        12 = both channel 1,2
        """        
        #Seperate Rx1, Rx2 data
        rx2c=np.reshape(self.rxbuf,(np.uint32(self.rxbuf.size/2),2))
        rxch1=rx2c[:,0]
        rxch2=rx2c[:,1]
        
        if ((ch==1) or (ch==12)):
            #Plot Rx1 data
            rxch1q=np.int16((rxch1>>16)&0xffff)
            rxch1i=np.int16(rxch1&0xffff)
            plt.figure(figsize=(20,10))
            plt.plot(rxch1q,'r', linewidth=1)
            plt.plot(rxch1i,'b', linewidth=1)
            plt.title('RX1 I/Q signal')
            plt.show()        

            # Plot Rx1 spectrum
            rxch1c = rxch1i + 1j*rxch1q
            rx1fft = np.fft.fftshift(np.fft.fft(rxch1c))
            spec_rx1 = 10*np.log10(np.abs(rx1fft)**2)
            plt.figure(figsize=(20,10))
            plt.plot(spec_rx1)
            plt.title('RX1 spectrum')
            plt.show()
            
        if ((ch==2) or (ch==12)):
            #Plot Rx2 data
            rxch2q=np.int16((rxch2>>16)&0xffff)
            rxch2i=np.int16(rxch2&0xffff)
            plt.figure(figsize=(20,10))
            plt.plot(rxch2q,'r', linewidth=1)
            plt.plot(rxch2i,'b', linewidth=1)
            plt.title('RX2 I/Q signal')
            plt.show()        

            # Plot Rx2 spectrum
            rxch2c = rxch2i + 1j*rxch2q
            rx2fft = np.fft.fftshift(np.fft.fft(rxch2c))
            spec_rx2 = 10*np.log10(np.abs(rx2fft)**2)
            plt.figure(figsize=(20,10))
            plt.plot(spec_rx2)
            plt.title('RX2 spectrum')
            plt.show()
            
        if ( (ch!=1) and (ch!=2) and (ch!=12)):
            print("Unknown channel parameter!--Use 1,2 or12")

    #time domain signal
    def live_plot(self,i, q, title='IQ Signal'):
        plt.figure(figsize=(20,10))
        plt.plot(i, 'b', linewidth=1)
        plt.plot(q, 'r', linewidth=1)
        plt.grid(True)
        plt.title(title)
        plt.show();            

    #power spectrum     
    def live_plot_psd(self, psd, title='Spectrum'):
        plt.figure(figsize=(20,10))
        plt.plot(psd,'b', linewidth=1)
        plt.grid(True)
        plt.title(title)
        plt.show();          
        
    def _m_captplot(self, ch=1, domain='time', m_src=CAPT_SEL_CDC, m_sample=1024, loop=10):
        m_rxbuf = allocate(shape=(m_sample*2,),dtype=np.uint32)
        for f in range(loop):
            _capt_test(self.pl, m_src, (m_sample*8), self.dma, m_rxbuf, self.sadma_reg, 0, 0)
            #Seperate Rx1, Rx2 data
            rx2c=np.reshape(m_rxbuf,(np.uint32(m_rxbuf.size/2),2))
            if(ch==1):
                rxch=rx2c[:,0]
            elif(ch==2):
                rxch=rx2c[:,1]
            else:
                raise Exception("[ERROR]Invalid Channel Number!!", ch)
            #Plot Rx1 data
            rxq=np.int16((rxch>>16)&0xffff)
            rxi=np.int16(rxch&0xffff)
            clear_output(wait=True)
            if (domain=='time'):
                title='Rx'+str(ch)+' IQ signal ' +str(f+1)
                self.live_plot(rxi, rxq, title)
            elif (domain=='freq'):
                rxc = rxi + 1j*rxq
                rxfft = np.fft.fftshift(np.fft.fft(rxc))
                spec_rx = 10*np.log10(np.abs(rxfft)**2)
                title='Rx'+str(ch)+' Spectrum ' +str(f+1)
                self.live_plot_psd(spec_rx, title)
            else:
                raise Exception("[ERROR]Invalid domain argument!!")
            sleep(0.1)        

        plt.close()            
            
            
######################################################################################

def main():
    
    ro = rrar()
    ro._setup_clock()
    ro._set_LED()
    ro._setup_afe()
    ro._init_jesdlink()
    ro._setup_pl_default()
    ro._capture_once()
    ro._plot_rx1()

if __name__ == "__main__":
    main()