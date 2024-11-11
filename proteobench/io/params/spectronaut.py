import re
import pandas as pd
from proteobench.io.params import ProteoBenchParameters
from pathlib import Path

def extract_value(lines, search_term):
    return next(
        (line.split(search_term)[1].strip() for line in lines if search_term in line),
        None
    )


def read_spectronaut_settings(file_path: str)-> ProteoBenchParameters:
    #check if file exists
    if not Path(file_path).exists():
        raise FileNotFoundError(f"File {file_path} not found")

    with open(file_path, 'r') as file:
        lines = file.readlines()

    # Remove any trailing newline characters from each line
    lines = [line.strip() for line in lines]

    params = ProteoBenchParameters()
    params.software_name = "Spectronaut"
    params.software_version = lines[0].split()[1]
    params.search_engine= "Spectronaut"
    params.search_engine_version = params.software_version

    lines = [re.sub(r'^[\s│├─└]*', '', line).strip() for line in lines]

    params.ident_fdr_psm = extract_value(lines,"Precursor Qvalue Cutoff:")
    params.ident_fdr_peptide = None
    params.ident_fdr_protein = extract_value(lines, "Protein Qvalue Cutoff (Experiment):")
    params.enable_match_between_runs = None
    params.precursor_mass_tolerance = extract_value(lines, "MS1 Mass Tolerance Strategy:")
    params.fragment_mass_tolerance = extract_value(lines, "MS2 Mass Tolerance Strategy:")
    params.enzyme = extract_value(lines, "Enzymes / Cleavage Rules:")
    params.allowed_miscleavages = extract_value(lines, "Missed Cleavages:")
    params.max_peptide_length = extract_value(lines, "Max Peptide Length:")
    params.min_peptide_length = extract_value(lines, "Min Peptide Length:")
    params.fixed_mods = extract_value(lines, "Fixed Modifications:")
    params.variable_mods = extract_value(lines, "^Variable Modifications:")
    params.max_mods = extract_value(lines, "Max Variable Modifications:")
    params.min_precursor_charge = extract_value(lines, "Peptide Charge:")
    params.max_precursor_charge = extract_value(lines, "Peptide Charge:")
    params.scan_window  = extract_value(lines,"XIC IM Extraction Window:")
    params.quantification_method  = extract_value(lines, "Quantity MS Level:") # "Quantity MS Level:" or "Protein LFQ Method:" or "Quantity Type:"
    params.second_pass  = extract_value(lines, "directDIA Workflow:")
    params.protein_inference  =  extract_value(lines, "Inference Algorithm:") # or Protein Inference Workflow:
    params.predictors_library   = extract_value(lines, "Hybrid (DDA + DIA) Library")


    return params


if __name__ == "__main__":
    fnames =  [
        "../../../test/params/spectronaut_Experiment1_ExperimentSetupOverview_BGS_Factory_Settings.txt"
    ]

    for file in fnames:
        parameters =  read_spectronaut_settings(file)
        actual = pd.Series(parameters.__dict__)
        actual.to_csv(Path(file).with_suffix(".csv"))
        print(parameters)

