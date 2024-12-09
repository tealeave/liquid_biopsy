import yaml
from my_pipeline.alignment import run_alignment
from my_pipeline.qc import run_qc
from my_pipeline.variant_calling import run_variant_calling
from my_pipeline.ml_filter import apply_ml_filter
from my_pipeline.reporting import generate_report

configfile: "config.yaml"

rule all:
    input:
        config["final_report"]

rule alignment:
    input:
        ref=config["reference"],
        r1=config["fastq_r1"],
        r2=config["fastq_r2"]
    output:
        bam=config["deduped_bam"],
        lc=config["lc_metrics"],
        dm=config["dedup_metrics"]
    run:
        run_alignment(config)

rule qc:
    input:
        bam=config["deduped_bam"]
    output:
        qc=config["qc_stats"]
    run:
        run_qc(config)

rule variant_calling:
    input:
        bam=config["deduped_bam"],
        ref=config["reference"]
    output:
        vcf=config["raw_vcf"]
    run:
        run_variant_calling(config)

rule ml_filter:
    input:
        vcf=config["raw_vcf"],
        model=config["ml_model"]
    output:
        filtered=config["filtered_vcf"]
    run:
        apply_ml_filter(config)

rule reporting:
    input:
        filtered=config["filtered_vcf"]
    output:
        report=config["final_report"]
    run:
        generate_report(config)
