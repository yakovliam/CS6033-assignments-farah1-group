
def time_repeated(
    runs: int,
    fn: callable,
    *args,
    **kwargs
) -> dict:
    """
    Calls `fn(*args, **kwargs)` `runs` times.
    Assumes fn returns (path, metrics_dict) where metrics_dict has "time_sec".
    Returns summary stats for your report.
    """
    total_time = 0.0
    found_any = False
    last_path: Optional[List[str]] = None
    sums = {
        "expanded": 0,
        "visited": 0,
        "enqueued": 0,
        "max_frontier": 0,  # track max across runs
    }

    for _ in range(runs):
        path, m = fn(*args, **kwargs, return_metrics=True)
        last_path = path
        found_any = found_any or m["found"]
        total_time += m["time_sec"]
        sums["expanded"] += m["expanded"]
        sums["visited"] += m["visited"]
        sums["enqueued"] += m["enqueued"]
        sums["max_frontier"] = max(sums["max_frontier"], m["max_frontier"])

    return {
        "found_in_any_run": found_any,
        "last_path": last_path,
        "avg_time_sec": total_time / runs,
        "avg_expanded": sums["expanded"] / runs,
        "avg_visited": sums["visited"] / runs,
        "avg_enqueued": sums["enqueued"] / runs,
        "max_frontier_overall": sums["max_frontier"],
        "runs": runs,
    }
