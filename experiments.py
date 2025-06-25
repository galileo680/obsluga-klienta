"""Uruchamia serię scenariuszy symulacji i porównuje z wzorami analitycznymi."""
import pandas as pd
from simulation import MMSSimulator
from models import mm1, mms
from analytics import ttest, regression

def run():
    configs = [
        dict(lambda_rate=2.0, mu=3.0, n_servers=1),
        dict(lambda_rate=2.5, mu=3.0, n_servers=1),
        dict(lambda_rate=2.5, mu=3.0, n_servers=2)
    ]
    rows = []
    for cfg in configs:
        sim = MMSSimulator(cfg["lambda_rate"], cfg["mu"], cfg["n_servers"], seed=42)
        df = sim.run(sim_time=8*60)
        wait_mean = df["wait_time"].mean()
        theo = mm1(cfg["lambda_rate"], cfg["mu"]) if cfg["n_servers"]==1 else mms(cfg["lambda_rate"], cfg["mu"], cfg["n_servers"])
        rows.append({**cfg, "wait_sim": wait_mean, "wait_theory": theo["Wq"]})

    summary = pd.DataFrame(rows)
    print("=== PODSUMOWANIE ===")
    print(summary.to_string(index=False))

    # Porównanie między pierwszymi dwoma konfiguracjami
    # sim1 = MMSSimulator(**configs[0], seed=123).run(8*60)["wait_time"]
    # sim2 = MMSSimulator(**configs[1], seed=123).run(8*60)["wait_time"]
    sim1 = MMSSimulator(configs[0]["lambda_rate"], configs[0]["mu"], configs[0]["n_servers"], seed=123)\
        .run(8*60)["wait_time"]
    sim2 = MMSSimulator(configs[1]["lambda_rate"], configs[1]["mu"], configs[1]["n_servers"], seed=123)\
        .run(8*60)["wait_time"]

    print("\nT‑test:", ttest(sim1, sim2))

    # Regresja
    summary["rho"] = summary["lambda_rate"]/(summary["n_servers"]*summary["mu"])
    model = regression("wait_sim ~ lambda_rate + mu + n_servers + rho", summary)
    print("\n=== REGRESJA ===")
    print(model.summary())

if __name__ == "__main__":
    run()
