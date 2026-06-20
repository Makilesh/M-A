"""
Numerical registry utility — collects and compares financial values
across documents for the Financial Verification Agent.

Stores raw_value, normalized_value, currency, scale_factor per metric per source.
Used by Agent 4 to detect cross-document inconsistencies.
"""

from dataclasses import dataclass, field

from src.utils.logger import setup_logger

logger = setup_logger(__name__)


@dataclass
class NumericalEntry:
    """A single numerical value from a source document."""
    metric_name: str
    raw_value: float
    normalized_value: float
    currency: str = "USD"
    scale_factor: float = 1.0
    source_file: str = ""
    page_number: int = 0
    fiscal_year: str = ""
    is_computed: bool = False
    citation_chain: str = ""


@dataclass
class MetricComparison:
    """Comparison result for a metric across sources."""
    metric_name: str
    entries: list[NumericalEntry] = field(default_factory=list)
    is_consistent: bool = True
    max_deviation_pct: float = 0.0
    discrepancy_detail: str = ""


class NumericalRegistry:
    """
    Collects financial values from chunks and enables cross-document comparison.
    All comparisons use normalized_value to account for scale differences.

    CRITICAL: Compare normalized_value ONLY. Raw values across documents
    with different scale_factors will produce false inconsistencies.
    """

    def __init__(self):
        self._entries: dict[str, list[NumericalEntry]] = {}

    def register(self, entry: NumericalEntry) -> None:
        """
        Registers a numerical value for comparison.

        Args:
            entry: NumericalEntry to register.
        """
        if entry.metric_name not in self._entries:
            self._entries[entry.metric_name] = []
        self._entries[entry.metric_name].append(entry)

    def check_consistency(self, tolerance_pct: float = 1.0) -> list[MetricComparison]:
        """
        Checks all registered metrics for cross-document consistency.

        Args:
            tolerance_pct: Maximum allowed deviation percentage (default 1%).

        Returns:
            List of MetricComparison results for each registered metric.
        """
        results = []

        for metric_name, entries in self._entries.items():
            if len(entries) < 2:
                results.append(MetricComparison(
                    metric_name=metric_name,
                    entries=entries,
                    is_consistent=True,
                ))
                continue

            # Compare normalized values
            values = [e.normalized_value for e in entries if e.normalized_value != 0]
            if not values:
                continue

            ref_value = values[0]
            max_deviation = 0.0
            inconsistencies = []

            for i, val in enumerate(values[1:], 1):
                deviation = abs(val - ref_value) / abs(ref_value) * 100
                max_deviation = max(max_deviation, deviation)
                if deviation > tolerance_pct:
                    inconsistencies.append(
                        f"{entries[i].source_file}: {val} vs {entries[0].source_file}: {ref_value} "
                        f"({deviation:.1f}% deviation)"
                    )

            results.append(MetricComparison(
                metric_name=metric_name,
                entries=entries,
                is_consistent=len(inconsistencies) == 0,
                max_deviation_pct=max_deviation,
                discrepancy_detail="; ".join(inconsistencies) if inconsistencies else "",
            ))

        return results

    def to_dict(self) -> dict:
        """Serializes registry to dict for Agent 4 output."""
        return {
            metric: {
                "values": [
                    {
                        "source": e.source_file,
                        "raw_value": e.raw_value,
                        "normalized_value": e.normalized_value,
                        "currency": e.currency,
                        "fiscal_year": e.fiscal_year,
                    }
                    for e in entries
                ],
                "is_consistent": all(
                    abs(e.normalized_value - entries[0].normalized_value)
                    / max(abs(entries[0].normalized_value), 1e-9)
                    < 0.01
                    for e in entries[1:]
                ) if len(entries) > 1 else True,
            }
            for metric, entries in self._entries.items()
        }
