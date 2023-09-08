import gym
from gym import error, spaces, utils
from gym.utils import seeding

import math
import numpy as np
#from statistics import mean
from numpy import mean


class scheduler(gym.Env):
    """Custom Environment that follows gym interface"""
    metadata = {'render.modes': ['console']}

    def __init__(self):
        super(scheduler, self).__init__()
        # Define action and observation space (gym.spaces objects)
        np.random.seed(0)
        print("Select numerology for FR1: 0->15 kHz, 1->30 kHz, 2->60 kHz")
        num = int(input())
        print("Select bandwidth (MHz): 0->5, 1->10, 2->15, 3->20, 4->25, 5->30, 6->40, 7->50, 8->60, 9->80, 10->90, 11->100")
        band = int(input())
        #Number of RBs
        N_RBs = [[25,52,79,102,133,160,216,270,0,0,0,0 ], [11,24,38,51,65,78,106,133,162,217,245,273], [0,11,18,24,31,38,51,65,79,107,121,135]]
        #Select number of UEs---> Assume 1 RB per UE
        self.RBs = N_RBs[num][band]
        print("RBs used:", self.RBs)
        # Max Ptx
        Tx_power = self.CalcPtx()  # dBm
        bandwidth_Hz = band*1000000 # MHz
        self.bandwidth_RBs_Hz = 0.9*(bandwidth_Hz/self.RBs)
        UEs = self.RBs
        self.Ptx = []
        for i in range(UEs):
            self.Ptx.append(Tx_power)  # Tx_power in dBm, set initially to max

        print("Initial Ptx: ", self.Ptx)

        # Action space
        low = np.zeros((self.RBs,), dtype=np.float32)
        high = np.full((self.RBs,), Tx_power)
        self.action_space = spaces.Box(low, high, dtype=np.float32)

        # Observation space
        self.observation_space = gym.spaces.Discrete(self.RBs+1)  # state: number of RBGs in state S0

    def CalcPtx(self):
        Ptx_max=46 #dBm
        print("Max Ptx in gNB (dBm):", Ptx_max)
        if (self.RBs>Ptx_max):
            Tx_power = round(Ptx_max/self.RBs,1)
        else:
            Tx_power = math.floor(Ptx_max/self.RBs)

        return Tx_power

    def CalcSNR(self):
        Gtx = 15  # dBi
        dist = 300  # m
        PL = 128.1 + 37.6 * math.log10(dist / 1000)  # d in km
        Nth = -174  # dBm/Hz
        NF = 5  # dB
        # FL fading losses
        mu = 0
        sigma = 8 # dB
        FLsample = np.random.lognormal(mu, sigma)
        FL = np.log(FLsample)
        signal_attenuation = Gtx - PL - NF - (Nth + 10*np.log10(self.bandwidth_RBs_Hz)) - FL
        snr = np.zeros((len(self.Ptx),))
        for i in range(len(self.Ptx)):
            #print(">>>>> self.Ptx[i] in dBm", self.Ptx[i])
            snr[i] = self.Ptx[i]*0.1 + signal_attenuation  # add atten. only to non -1 elements
            #print(">>>>> snr[i] in dB", snr[i])
            snr[i] = pow(10, (snr[i] / 10))
            #print(">>>>> snr[i]", snr[i])
        return snr

    def CalcPC(self):
        kappa = 0.38 # considering DL only
        N = len(self.Ptx) # assume 1 RB per UE
        P_UE_circuit = 0.1 # Watt
        P_gNB_circuit = 1 # Watt
        pc_Watt = pow(10, ((sum(self.Ptx)/10-30) / 10))
        pc = (N*pc_Watt)/kappa + N*P_UE_circuit + P_gNB_circuit
        #print(">>>>> pc", pc)
        return pc


    def reset(self):
        self.state = 0
        return self.state

    def take_step(self, action):
        Ptx_max = int(self.action_space.high[action])
        if (self.Ptx[action] < Ptx_max):
            self.Ptx[action] = self.Ptx[action] + 1

    def step(self, action):
        # State =  SNR level above or below threshold
        SNRthres_dB = 20
        SNRthres = pow(10, (SNRthres_dB / 10))

        self.take_step(action)

        RBG_count = 0
        SNRs = self.CalcSNR()
        for i in SNRs:
            if (i > SNRthres):
                RBG_count = RBG_count + 1

        self.state = RBG_count # state = number of RBs with SNR<threshold
        sum_C = 0;
        for i in range(len(SNRs)):
            if SNRs[i]== 0:
                snr_log = 0
            else:
                snr_log = np.log2(1 + SNRs[i])
            sum_C = sum_C + self.bandwidth_RBs_Hz * snr_log # Capacity in bps

        # Reward = Energy efficiency Mbits/Joule
        sum_P = self.CalcPC()
        EE_reward = (sum_C/sum_P)/1000000

        if (self.state == self.RBs):
            rew = 0.0
            done = True
        else:
            rew = EE_reward
            done = False

        obs = self.state
        return obs, rew, done, {}


    def render(self):
        # Render to screen, return super(scheduler, self).reset()
        pass