"""Évaluation de baselines de prévision (rolling one-step-ahead)."""
import math


def _linear_next(history):
    n = len(history)
    xs = list(range(n))
    mx, my = sum(xs) / n, sum(history) / n
    den = sum((x - mx) ** 2 for x in xs) or 1
    slope = sum((x - mx) * (y - my) for x, y in zip(xs, history)) / den
    return my + slope * (n - mx)


def evaluate_models(values, labels, n_test=3):
    if len(values) < n_test + 3:
        raise ValueError(f"Il faut au moins {n_test + 3} entrées pour évaluer (il y en a {len(values)}).")

    models = {
        "Naive (last value)": lambda h: h[-1],
        "3-point moving average": lambda h: sum(h[-3:]) / len(h[-3:]),
        "Linear trend": _linear_next,
    }
    rows = []
    for idx in range(len(values) - n_test, len(values)):
        history, actual = values[:idx], values[idx]
        for name, fn in models.items():
            pred = fn(history)
            err = actual - pred
            rows.append({"label": labels[idx], "model": name, "actual": actual,
                         "predicted": round(pred, 4), "abs_error": abs(err), "sq_error": err ** 2,
                         "abs_pct_error": abs(err) / abs(actual) * 100 if actual else None})

    metrics = []
    for name in models:
        r = [x for x in rows if x["model"] == name]
        pct = [x["abs_pct_error"] for x in r if x["abs_pct_error"] is not None]
        metrics.append({"model": name,
                        "MAE": round(sum(x["abs_error"] for x in r) / len(r), 4),
                        "RMSE": round(math.sqrt(sum(x["sq_error"] for x in r) / len(r)), 4),
                        "MAPE": round(sum(pct) / len(pct), 4) if pct else None})
    metrics.sort(key=lambda m: m["MAE"])
    return {"n_test": n_test, "n_observations": len(values), "metrics": metrics, "predictions": rows,
            "caution": "Échantillon très petit : résultats préliminaires, non généralisables."}
