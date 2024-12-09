import subprocess
from typing import Dict

def run_qc(config: Dict[str, str]) -> None:
    """
    Perform QC on deduplicated BAM using samtools stats as an example.
    """
    deduped_bam = config["deduped_bam"]
    qc_report = f"{config['output_dir']}/qc_stats.txt"

    with open(qc_report, "w") as out:
        subprocess.check_call(["samtools", "stats", deduped_bam], stdout=out)

    print("[QC] QC metrics generated (samtools stats).")
