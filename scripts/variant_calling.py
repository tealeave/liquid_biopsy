import subprocess
from typing import Dict

def run_variant_calling(config: Dict[str, str]) -> None:
    """
    Run Sentieon TNscope for somatic variant calling (tumor-only mode).
    """
    ref = config["reference"]
    deduped_bam = config["deduped_bam"]
    raw_vcf = config["raw_vcf"]
    sample = config["sample_name"]

    subprocess.check_call([
        "sentieon", "driver", "-r", ref, "-i", deduped_bam,
        "--algo", "TNscope",
        "--tumor_sample", sample,
        raw_vcf
    ])

    print("[Variant Calling] TNscope somatic variant calling completed.")
