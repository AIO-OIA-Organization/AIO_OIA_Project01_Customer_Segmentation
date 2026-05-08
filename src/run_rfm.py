from pathlib import Path

from src.rfm_segmentation import RFMSegmentationPipeline

PROJECT_ROOT = Path(__file__).resolve().parents[1]
INPUT_PATH = str(PROJECT_ROOT / "data/raw/online_retail.csv")
OUTPUT_PATH = str(PROJECT_ROOT / "data/processed/rfm_segments.csv")
RFM_TABLE_PATH = str(PROJECT_ROOT / "data/processed/rfm_table.csv")
N_CLUSTERS = 4

if __name__ == "__main__":
    pipeline = RFMSegmentationPipeline(
        input_path=INPUT_PATH,
        output_path=OUTPUT_PATH,
        n_clusters=N_CLUSTERS,
        rfm_table_path=RFM_TABLE_PATH,
    )
    rfm = pipeline.run()
    print(rfm.head())
