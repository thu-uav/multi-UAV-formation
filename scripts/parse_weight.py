import glob
from wandb.proto import wandb_internal_pb2
from wandb.sdk.internal import datastore
import csv

with open('points.csv', 'w') as csvfile:
    writer = csv.writer(csvfile)

    for filepath in glob.iglob('OmniDrones/scripts/wandb/run-*/*.wandb'):
        ds = datastore.DataStore()
        ds.open_for_scan(filepath)
        is_ratio = False
        ratio1 = 1
        ratio2 = 1
        ratio3 = 1
        w1 = 1
        w2 = 1
        w3 = 1
        w4 = 1
        v1 = 0
        v2 = 0
        v3 = 0
        v4 = 0

        while True:
            try:
                data = ds.scan_data()
                pb = wandb_internal_pb2.Record()
                pb.ParseFromString(data)  
                record_type = pb.WhichOneof("record_type")

                if record_type == "run":
                    for u in pb.run.config.update:
                        if u.key == "task.ratio1":
                            ratio1 = float(u.value_json)
                            is_ratio = True
                        if u.key == "task.ratio2":
                            ratio2 = float(u.value_json)
                        if u.key == "task.ratio3":
                            ratio3 = float(u.value_json)

                if record_type == "summary":
                    for u in pb.summary.update:
                        if u.key == "eval/stats.morl_smooth":
                            v1 = float(u.value_json)
                        if u.key == "eval/stats.morl_formation":
                            v2 = float(u.value_json)
                        if u.key == "eval/stats.morl_obstacle":
                            v3 = float(u.value_json)
                        if u.key == "eval/stats.morl_forward":
                            v4 = float(u.value_json)
            except:
                break

        if is_ratio:
            w1 = ratio1*ratio2
            w2 = ratio1*(1-ratio2)
            w3 = (1-ratio1)*ratio3
            w4 = (1-ratio1)*(1-ratio3)

        writer.writerow([ratio1, ratio2, ratio3, w1, w2, w3, w4, v1, v2, v3, v4])
    
