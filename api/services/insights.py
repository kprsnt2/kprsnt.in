"""
Services for generating narrative insights from job data.
Extracted from index.py for maintainability.
"""
import re


def generate_jobs_insight(all_jobs, daily_snapshots, grade_counts, dimension_avgs, score_distribution):
    """Generate a daily narrative insight summary from jobs pipeline data."""
    if not all_jobs:
        return "No job data available yet. The pipeline runs daily at 8:00 AM IST."

    total = len(all_jobs)
    top_matches = sum(1 for j in all_jobs if j.get('evaluation', {}).get('overall_score', 0) >= 3.5)
    applied = sum(1 for j in all_jobs if j.get('status') == 'applied')
    verified = sum(1 for j in all_jobs if j.get('verified'))
    avg_score = round(sum(j.get('evaluation', {}).get('overall_score', 0) for j in all_jobs if j.get('evaluation')) / max(sum(1 for j in all_jobs if j.get('evaluation')), 1), 2)

    # Best job
    best = max(all_jobs, key=lambda j: j.get('evaluation', {}).get('overall_score', 0)) if all_jobs else None
    best_ev = best.get('evaluation', {}) if best else {}

    # Grade-A count
    a_count = sum(v for k, v in grade_counts.items() if k.startswith('A'))

    parts = []
    parts.append(f"🎯 **Pipeline Summary** — {total} jobs evaluated, {top_matches} top matches (≥3.5/5), avg score {avg_score}/5.")

    if a_count > 0:
        parts.append(f"🏆 **{a_count} Grade-A** opportunities identified.")

    if best and best_ev:
        parts.append(f"⭐ Best match: **{best.get('title', '?')}** at {best.get('company', '?')} ({best_ev.get('overall_score', 0)}/5, Grade {best_ev.get('grade', '?')}).")

    if applied > 0:
        parts.append(f"📤 Applied to {applied} position{'s' if applied != 1 else ''}.")
    if verified > 0:
        pct = round(verified / total * 100)
        parts.append(f"✅ {verified} verified ({pct}% verification rate).")

    # Dimension strength
    if dimension_avgs:
        strongest = max(dimension_avgs.items(), key=lambda x: x[1])
        weakest = min(dimension_avgs.items(), key=lambda x: x[1])
        dim_labels = {'cv_match': 'CV Match', 'archetype_fit': 'Archetype Fit', 'comp_analysis': 'Compensation', 'culture_signals': 'Culture Fit'}
        parts.append(f"💪 Strongest dimension: **{dim_labels.get(strongest[0], strongest[0])}** ({strongest[1]}/5). Focus area: **{dim_labels.get(weakest[0], weakest[0])}** ({weakest[1]}/5).")

    # Trend from snapshots
    if len(daily_snapshots) >= 2:
        prev_count = daily_snapshots[-2].get('total_jobs', 0) if len(daily_snapshots) >= 2 else 0
        curr_count = daily_snapshots[-1].get('total_jobs', 0)
        delta = curr_count - prev_count
        if delta > 0:
            parts.append(f"📈 +{delta} new jobs compared to previous run.")
        elif delta < 0:
            parts.append(f"📉 {delta} fewer jobs vs previous run.")

    result = " ".join(parts)
    result = re.sub(r'\*\*(.+?)\*\*', r'<strong>\1</strong>', result)
    return result
