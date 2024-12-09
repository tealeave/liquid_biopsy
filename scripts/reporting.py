import pysam
from typing import Dict

def generate_report(config: Dict[str, str]) -> None:
    """
    Generate a simple report summarizing the number of variants in the filtered VCF.
    """
    filtered_vcf = config["filtered_vcf"]
    report_file = config["final_report"]

    count = 0
    with pysam.VariantFile(filtered_vcf) as vcf:
        for _ in vcf:
            count += 1

    with open(report_file, "w") as f:
        f.write(f"Final filtered variants: {count}\n")

    print("[Reporting] Final report generated.")
