def tourism_summary(zone_summary):
    if zone_summary.empty:
        return "No site data available."
    busiest = zone_summary.iloc[0]
    return (f"Heritage-site overview: the highest recorded zone is {busiest['zone']} "
            f"with peak count {int(busiest['peak_people'])}. This is a threshold-based "
            f"crowding indicator, not a calibrated capacity or visitor wait-time estimate.")
