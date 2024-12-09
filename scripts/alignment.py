import subprocess
from typing import Dict

def run_alignment(config: Dict[str, str]) -> None:
    """
    Perform alignment and deduplication using Sentieon BWA MEM and Dedup.
    """
    ref = config["reference"]
    r1 = config["fastq_r1"]
    r2 = config["fastq_r2"]
    sample = config["sample_name"]
    sorted_bam = config["sorted_bam"]
    deduped_bam = config["deduped_bam"]
    lc_metrics = config["lc_metrics"]
    dedup_metrics = config["dedup_metrics"]

    read_group = f"@RG\\tID:{sample}\\tSM:{sample}\\tLB:lib1\\tPL:ILLUMINA"

    # Run alignment and sorting
    align_cmd = [
        "sentieon", "bwa", "mem", "-R", read_group, ref, r1, r2
    ]
    sort_cmd = [
        "sentieon", "util", "sort", "-o", sorted_bam, "-t", "8", "--sam2bam"
    ]

    p1 = subprocess.Popen(align_cmd, stdout=subprocess.PIPE)
    subprocess.check_call(sort_cmd, stdin=p1.stdout)
    p1.wait()

    # LocusCollector step
    subprocess.check_call([
        "sentieon", "driver", "-r", ref, "-i", sorted_bam,
        "--algo", "LocusCollector",
        lc_metrics
    ])

    # Deduplication step
    subprocess.check_call([
        "sentieon", "driver", "-r", ref, "-i", sorted_bam,
        "--algo", "Dedup", "--rmdup",
        "--metrics", dedup_metrics,
        deduped_bam
    ])

    print("[Alignment] Alignment, sorting, and deduplication completed.")
