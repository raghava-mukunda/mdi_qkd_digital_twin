from config.system_params import SystemParameters

p = SystemParameters()

print()
print("Linewidth (Hz):", p.laser_linewidth_hz)
print("Coherence time (ps):", p.coherence_time_ps)
print("Bin spacing (ps):", p.time_bin_spacing_ps)