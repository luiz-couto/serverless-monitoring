from typing import Dict, Any

N_MIN = 12
N_HOUR = 720

def getCPUandMemory(data: dict):
    cpus_percent = []
    memory_percent = 0
    for key in data.keys():
        if "cpu_percent" in key:
            cpus_percent.append(data[key])
        
        if "virtual_memory-percent" in key:
            memory_percent = data[key]

    return cpus_percent, memory_percent


def handler(data: dict, context: object) -> Dict[str, Any]:
    
    cpus_percent, memory_percent = getCPUandMemory(data)
    output = {}

    if getattr(context.env, "counter", None) is None:
        
        context.env["counter"] = 1
        print("PASSOU AQ:", context.env["counter"])
        
        for idx, cpu in enumerate(cpus_percent):
            label_min = "mvg_avg_cpu_" + str(idx) + "_last_minute"
            context.env[label_min] = cpu
            output[label_min] = cpu

            label_hour = "mvg_avg_cpu_" + str(idx) + "_last_hour"
            context.env[label_hour] = cpu
            output[label_hour] = cpu

        label_memory = "mvg_avg_memory_last_min" 
        context.env[label_memory] = memory_percent
        output[label_memory] = memory_percent

        return output

    
    context.env["counter"] += 1
    counter = context.env["counter"]

    n_min = N_MIN
    n_hour = N_HOUR

    if counter < N_MIN:
        n_min = counter
    
    if counter < N_HOUR:
        n_hour = counter


    for idx, cpu in enumerate(cpus_percent):
        label_min = "mvg_avg_cpu_" + str(idx) + "_last_minute"
        last_mvg_avg_min = context.env[label_min]
        new_mvg_avg_min = (last_mvg_avg_min * (n_min - 1) + cpu) / n_min
        context.env[label_min] = new_mvg_avg_min
        output[label_min] = new_mvg_avg_min

        label_hour = "mvg_avg_cpu_" + str(idx) + "_last_hour"
        last_mvg_avg_hour = context.env[label_hour]
        new_mvg_avg_hour = (last_mvg_avg_hour * (n_hour - 1) + cpu) / n_hour
        context.env[label_hour] = new_mvg_avg_hour
        output[label_hour] = new_mvg_avg_hour

    label_memory = "mvg_avg_memory_last_min"
    last_mvg_avg_memory = context.env[label_memory]
    new_mvg_avg_memory = (last_mvg_avg_memory * (n_min - 1) + cpu) / n_min
    context.env[label_memory] = new_mvg_avg_memory
    output[label_memory] = new_mvg_avg_memory

    print(output)
    return output
