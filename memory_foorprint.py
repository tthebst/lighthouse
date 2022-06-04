import sys
import dateparser
from matplotlib import pyplot as plt
import pandas as pd

plt.close("all")

print(sys.argv[1:])

io_log = sys.argv[1]
freezer_log = sys.argv[2]
chain_log = sys.argv[3]

print("IO ANALYSIS")

io_wkb = {"Date": [],"wkb":[]}
io_phys_mem = {"Date": [],"phys_kb":[]}
with open(io_log) as file:
    lines = file.readlines()
    for l in lines:
        # Select datalines
        # [Time (0) UID (1) PID(2) minflt/s(3) majflt/s(4) VSZ(5) RSS(6) %MEM(7) kB_rd/s(8) kB_wr/s(9) kB_ccwr/s(10) iodelay(11) Command(12)]i
        # SAMPLE:  19:57:31     1000     17798 196641.50     23.50 11819768 1768756   5.39   3198.00      0.00      0.00       0  lighthouse
        # https://man7.org/linux/man-pages/man1/pidstat.1.html
        if "lighthouse" in l:
            data = [x.strip() for x in l.split()]
            time = pd.Timestamp(dateparser.parse(data[0]))
            wkb = int(float(data[9]))
            # To mb
            phys_mem_kb = int(data[6])/1024
            io_wkb["Date"].append(time)
            io_wkb["wkb"].append(wkb)
            io_phys_mem["phys_kb"].append(phys_mem_kb)
            io_phys_mem["Date"].append(time)

io_wkb = pd.DataFrame(io_wkb).set_index("Date")
io_phys_mem = pd.DataFrame(io_phys_mem).set_index("Date")

print("FREEZER")
freezer= {"Date": [],"freezer_bytes":[]}
with open(freezer_log) as file:
    lines = file.readlines()
    for l in lines:
        # Select datalines
        # SAMPLE: Jun(0) 04(1) 19:56:50(2) 4451276(3)    /home/tim/nfs/beacon_chain/beacon/freezer_db/(4)
        if "freezer" in l:
            data = [x.strip() for x in l.split()]
            time = pd.Timestamp(dateparser.parse(data[2]))
            freezer["Date"].append(time)
            # Store in Mb
            freezer["freezer_bytes"].append(int(data[3])/(1024*1024))

freezer= pd.DataFrame(freezer).set_index("Date")


print("CHAIN")
chain= {"Date": [],"chain_bytes":[]}
with open(chain_log) as file:
    lines = file.readlines()
    for l in lines:
        # Select datalines
        # SAMPLE: Jun(0) 04(1) 19:56:50(2) 4451276(3)    /home/tim/nfs/beacon_chain/beacon/chaindb/(4)
        if "chain_db" in l:
            data = [x.strip() for x in l.split()]
            time = pd.Timestamp(dateparser.parse(data[2]))
            chain["Date"].append(time)
            # Store in Mb
            chain["chain_bytes"].append(int(data[3])/(1024*1024))


chain= pd.DataFrame(chain).set_index("Date")

# Set first row to zero for correct filling and then ffill all NAN using the last valid value
join_table = pd.concat([io_wkb, io_phys_mem,freezer,chain], axis=1)
join_table = join_table.fillna(method='ffill').fillna(0)
print(join_table)





# Plot
print("Plotting... wbk 60s avg")
x=io_wkb.rolling(60).sum().fillna(0)
x.plot(title="60s rolling avg Write IO [kb]").get_figure().savefig("w_kb_60s.png");
plt.close("all")
print("Plotting... wbk 60s avg zoom")
x=io_wkb.rolling(60).sum().fillna(0)
x.plot(title="60s rolling avg Write IO zoom [kb]", ylim=(0,2000000)).get_figure().savefig("w_kb_60s_zoom.png");
plt.close("all")
print("Plotting... MEM 60s avg")
x=io_phys_mem.rolling(60).sum().fillna(0)
x.plot(title="Physical memory [Mb]").get_figure().savefig("io_phys_60s.png");
plt.close("all")
# Plot
print("Plotting... freezer ")
x=join_table["freezer_bytes"]
x.plot(title="Freezer DB size [Gb]").get_figure().savefig("freezer.png");
plt.close("all")
print("Plotting... chaindb")
x=join_table["chain_bytes"]
x.plot(title="Chain db size [Gb]").get_figure().savefig("chaindb.png");
plt.close("all")
