def crowd_summary(zone_summary):
    if zone_summary.empty:
        return "No zone data available."
    busiest = zone_summary.iloc[0]
    return (f"Busiest zone in the supplied records: {busiest['zone']} "
            f"(peak visible/recorded count: {int(busiest['peak_people'])}). "
            f"Zones are flagged based on the configured threshold.")
