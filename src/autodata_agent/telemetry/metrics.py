from prometheus_client import Counter, Histogram

accepted_counter = Counter("autodata_accepted_total", "Accepted synthetic examples")
rejected_counter = Counter("autodata_rejected_total", "Rejected synthetic examples")
round_latency = Histogram("autodata_round_latency_seconds", "Inner-loop round latency")
