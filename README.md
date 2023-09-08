# Summary

This is a simple 5G RAN scheduler that uses the `scheduler` environment build using OpenAI Gym [1]. The power consumption model used in this scheduler is described in [2]
and the design of the scheduler is inspired by [3].

# Requirements 

- `python 3.8.5.`
- `gym`
- `numpy`
- `math`

# Installation 
Run inside 5GRANSched folder:

`cd scheduler`

`pip install -e .`

# List of files 

- Sched_QL_SARSA.py allows the user to select between a simple Q-learning (off-policy) approach and the SARSA algorithm that aims to maximize the RAN energy efficiency by selecting the transmission power per resource block.
- cleanScheduler.bat deletes and re-registers the `scheduler` environment.

# License

5GRANSched is provided under GPLv2.

# References

[1] https://github.com/openai/gym

[2]. A. Khalili, S. Zarandi, M. Rasti and E. Hossain, "Multi-Objective Optimization for Energy- and Spectral-Efficiency Tradeoff in In-Band Full-Duplex (IBFD) Communication," 2019 IEEE Global Communications Conference (GLOBECOM), Waikoloa, HI, USA, 2019, pp. 1-6.

[3]. M. Elsayed and M. Erol-Kantarci, "AI-Enabled Radio Resource Allocation in 5G for URLLC and eMBB Users," 2019 IEEE 2nd 5G World Forum (5GWF), Dresden, Germany, 2019, pp. 590-595.