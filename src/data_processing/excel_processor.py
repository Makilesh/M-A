"""
Excel processor using pandas + openpyxl.

Extracts sheets, detects tables, normalizes with ExcelNormalizer,
and generates 4 representations via FinancialTableConverter.
"""

from pathlib import Path
from dataclasses import dataclass, field

import pandas as pd

from src.data_processing.excel_normalizer import ExcelNormalizer, TableNormalizationMeta
from src.data_processing.financial_table_converter import FinancialTableConverter
from src.utils.logger import setup_logger

logger = setup_logger(__name__)


@dataclass
class ExcelSheet:
    """Extracted content from a single Excel sheet."""
    sheet_name: str
    dataframe: pd.DataFrame = None
    normalization_meta: TableNormalizationMeta = None
    representations: dict = field(default_factory=dict)
    header_rows: list[str] = field(default_factory=list)


class ExcelProcessor:
    """
    Processes Excel files into structured, normalized table data.

    Pipeline:
    1. Read each sheet with pandas
    2. Detect and extract header rows
    3. Normalize scale/currency via ExcelNormalizer
    4. Generate 4 representations via FinancialTableConverter
    """

    def __init__(self):
        self._normalizer = ExcelNormalizer()
        self._converter = FinancialTableConverter()

    def process(self, excel_path: str, doc_id: str) -> list[ExcelSheet]:
        """
        Processes an Excel file into structured sheet objects.

        Args:
            excel_path: Absolute path to the Excel file.
            doc_id: Document identifier for metadata.

        Returns:
            List of ExcelSheet objects with normalized data and representations.

        Raises:
            FileNotFoundError: If excel_path does not exist.
            ValueError: If file contains no readable sheets.
        """
        path = Path(excel_path)
        if not path.exists():
            raise FileNotFoundError(f"Excel file not found: {excel_path}")

        logger.info(
            "Processing Excel file",
            extra={"path": excel_path, "doc_id": doc_id},
        )

        # Read all sheets
        xl = pd.ExcelFile(excel_path, engine="openpyxl")
        sheets: list[ExcelSheet] = []

        for sheet_name in xl.sheet_names:
            try:
                sheet = self._process_sheet(xl, sheet_name, doc_id)
                if sheet is not None:
                    sheets.append(sheet)
            except Exception as e:
                logger.warning(
                    f"Failed to process sheet '{sheet_name}'",
                    extra={"error": str(e), "doc_id": doc_id},
                )
                continue

        logger.info(
            "Excel processing complete",
            extra={
                "doc_id": doc_id,
                "total_sheets": len(sheets),
                "sheet_names": [s.sheet_name for s in sheets],
            },
        )

        return sheets

    def _process_sheet(
        self,
        xl: pd.ExcelFile,
        sheet_name: str,
        doc_id: str,
    ) -> ExcelSheet | None:
        """
        Processes a single sheet.

        Args:
            xl: Open ExcelFile object.
            sheet_name: Name of the sheet to process.
            doc_id: Document identifier.

        Returns:
            ExcelSheet object or None if sheet is empty.
        """
        # Read with all data as strings first to detect headers
        df_raw = pd.read_excel(xl, sheet_name=sheet_name, header=None, dtype=str)

        if df_raw.empty:
            return None

        # Find header row — first row with > 50% non-null string values
        header_row_idx = 0
        for idx in range(min(10, len(df_raw))):
            row = df_raw.iloc[idx]
            non_null = row.notna().sum()
            if non_null > len(row) * 0.5:
                # Check if values look like headers (non-numeric)
                str_count = sum(
                    1 for v in row if pd.notna(v) and not self._is_numeric(str(v))
                )
                if str_count > non_null * 0.5:
                    header_row_idx = idx
                    break

        # Re-read with detected header row
        df = pd.read_excel(
            xl, sheet_name=sheet_name, header=header_row_idx, engine="openpyxl"
        )

        # Drop completely empty rows/columns
        df = df.dropna(how="all").dropna(axis=1, how="all")

        if df.empty:
            return None

        # Extract header cells for normalization
        header_cells = [str(c) for c in df.columns.tolist()]

        # Also check first few rows above header for scale indicators
        pre_header_text = []
        if header_row_idx > 0:
            for idx in range(header_row_idx):
                row_text = " ".join(str(v) for v in df_raw.iloc[idx] if pd.notna(v))
                if row_text.strip():
                    pre_header_text.append(row_text)

        all_header_context = header_cells + pre_header_text

        # Normalize scale and currency
        norm_meta = self._normalizer.detect_scale(all_header_context)

        # Generate 4 representations
        representations = self._converter.convert(
            df=df,
            sheet_name=sheet_name,
            normalization_meta=norm_meta,
            doc_id=doc_id,
        )

        return ExcelSheet(
            sheet_name=sheet_name,
            dataframe=df,
            normalization_meta=norm_meta,
            representations=representations,
            header_rows=header_cells,
        )

    @staticmethod
    def _is_numeric(value: str) -> bool:
        """Check if a string value looks numeric."""
        try:
            cleaned = value.replace(",", "").replace("$", "").replace("%", "").strip()
            if cleaned in ("", "-", "—", "–", "N/A", "n/a"):
                return False
            float(cleaned)
            return True
        except (ValueError, TypeError):
            return False

    def to_chunks(self, sheets: list[ExcelSheet]) -> list[dict]:
        """
        Converts ExcelSheet objects to chunks for the ingestion pipeline.
        Each representation becomes a separate chunk with shared table_id.

        Args:
            sheets: List of ExcelSheet from process().

        Returns:
            List of chunk dicts ready for embedding and indexing.
        """
        chunks = []
        for sheet in sheets:
            for rep_type, rep_text in sheet.representations.items():
                if not rep_text:
                    continue
                chunks.append({
                    "text": rep_text,
                    "sheet_name": sheet.sheet_name,
                    "content_type": f"table_{rep_type}",
                    "is_table": 1,
                    "currency": (
                        sheet.normalization_meta.currency
                        if sheet.normalization_meta else "UNKNOWN"
                    ),
                    "scale_factor": (
                        sheet.normalization_meta.scale_factor
                        if sheet.normalization_meta else 1.0
                    ),
                    "scale_label": (
                        sheet.normalization_meta.scale_label
                        if sheet.normalization_meta else "units"
                    ),
                })

        return chunks
