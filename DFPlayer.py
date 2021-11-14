from machine import Pin, SPI, I2C, UART
import utime

class dfplayer(): 
    # [$S,VER,Len,CMD,Feedback,para1,para2,checksum,$0] */    
    
    def __init__(self, TX=Pin(0), RX=Pin(1)):
        self.uart = UART(0, baudrate=9600, tx=TX, rx=RX)
        #utime.sleep(100)
        #isConnected: boolean = false
        self.package = bytearray(b'\x7E\xFF\x06\x00\x00\x00\x00\x00\x00\xEF')      
        
    def checkSum(self):
        total = 0
        for i in range(1,7):
            total += self.package[i]        
        total = 65536 - total
        self.package[7] = total >> 8
        self.package[8] = total & 0xFF
    

    def sendData(self):        
        self.uart.write(self.package)
        
    def command(self, CMD, para1, para2):
        self.package[3] = CMD
        self.package[5] = para1
        self.package[6] = para2
        self.checkSum()
        self.sendData()
        utime.sleep_ms(150)
        
    def play(self):
        self.command(13,0,0)
        
    def stop(self):
        self.command(22,0,0)
        
    def play_next(self):
        self.command(1,0,0)
        
    def play_previous(self):
        self.command(2,0,0)
        
    def play_track(self, track):
        th = track // 256
        tl = track % 256
        self.command(3,th,tl)
        
    def get_status(self):
        status = bytearray(10)
        self.command(66,0,0)
        while self.uart.any() == 0:
            pass
        #if self.uart.any() > 0:    
        self.uart.readinto(status)
        if status[6] == 0:
            return 'STOPED'
        elif status[6] == 1:
            return 'PLAYING'
        elif status[6] == 2:
            return 'PAUSED'
        return 'N/A'
        
        
if __name__ == "__main__":        
    df = dfplayer(Pin(0), Pin(1))

    df.play_track(1)
    print(df.get_status())
    utime.sleep(3)
    df.stop()
    #utime.sleep(1)
    print(df.get_status())



        
