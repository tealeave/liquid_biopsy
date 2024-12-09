import pysam
import pickle
import numpy as np
from typing import Dict

def apply_ml_filter(config: Dict[str, str]) -> None:
    """
    Load a pre-trained ML model and filter variants based on predictions.
    """
    raw_vcf = config["raw_vcf"]
    filtered_vcf = config["filtered_vcf"]
    model_path = config["ml_model"]
    min_qual = config["min_qual"]

    with open(model_path, "rb") as mf:
        model = pickle.load(mf)

    with pysam.VariantFile(raw_vcf, "r") as invcf, pysam.VariantFile(filtered_vcf, "w", header=invcf.header) as outvcf:
        for rec in invcf:
            qual = rec.qual if rec.qual is not None else 0
            dp = rec.info.get("DP", 0)

            features = np.array([[qual, dp]], dtype=float)
            probs = model.predict_proba(features)
            true_prob = probs[0, 1]

            if true_prob > 0.9 and qual >= min_qual:
                outvcf.write(rec)

    print("[ML Filter] Variants filtered using ML model and QUAL threshold.")
