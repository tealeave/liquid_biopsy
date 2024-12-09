import argparse
import yaml
import os
from pipeline import alignment, qc, variant_calling, ml_filter, reporting

def main() -> None:
    """
    Main driver function for the liquid biopsy pipeline.
    """
    parser = argparse.ArgumentParser(description="Liquid Biopsy Pipeline")
    parser.add_argument("--config", required=True, help="Path to config YAML")
    args = parser.parse_args()

    with open(args.config, 'r') as f:
        config = yaml.safe_load(f)

    os.makedirs(config["output_dir"], exist_ok=True)

    alignment.run_alignment(config)
    qc.run_qc(config)
    variant_calling.run_variant_calling(config)
    ml_filter.apply_ml_filter(config)
    reporting.generate_report(config)

    print("Pipeline completed successfully.")

if __name__ == "__main__":
    main()
