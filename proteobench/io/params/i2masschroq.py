import pathlib
from typing import Optional

import pandas as pd

from proteobench.io.params import ProteoBenchParameters


def extract_params(fname: pathlib.Path) -> ProteoBenchParameters:
    """
    Extract parameters from an i2MassChroQ parameter file and return a `ProteoBenchParameters` object.

    Args:
        fname (pathlib.Path): The file path to the i2MassChroQ parameter file.

    Returns:
        ProteoBenchParameters: The extracted parameters encapsulated in a `ProteoBenchParameters` object.
    """
    # Read parameters from the file
    params = pd.read_csv(fname, sep="\t", header=None, index_col=0).squeeze()

    # Construct tolerance strings for fragment and parent mass errors
    _tol_frag = "{} {}".format(
        params.loc["spectrum, fragment monoisotopic mass error"], # this would be "sage_fragment_tol	-0.02 0.02 da" with sage
        params.loc["spectrum, fragment monoisotopic mass error units"].replace("Daltons", "Da"),
    )

    # Construct tolerance strings for parent mass error
    _tol_prec_lower = "{} {}".format(
        params.loc["spectrum, parent monoisotopic mass error minus"], # "sage_precursor_tol	-10 10 ppm"
        params.loc["spectrum, parent monoisotopic mass error units"].replace("Daltons", "Da"),
    )

    _tol_prec_upper = "{} {}".format(
        params.loc["spectrum, parent monoisotopic mass error plus"],
        params.loc["spectrum, parent monoisotopic mass error units"].replace("Daltons", "Da"),
    )

    # Max missed cleavage sites, either from scoring or refinement
    max_cleavage = params.loc["scoring, maximum missed cleavage sites"] # "sage_database_enzyme_missed_cleavages	2"
    if params.loc["refine"] == "yes":
        max_cleavage = int(params.loc["refine, maximum missed cleavage sites"])

    _enzyme = str(params.loc["protein, cleavage site"]) # "sage_database_enzyme_cleave_at	KR" and "sage_database_enzyme_restrict	P" and "sage_database_enzyme_c_terminal	true"
    # Replace the enzyme pattern with the enzyme name used in ProteoBench
    if _enzyme == "[RK]|{P}":
        _enzyme = "Trypsin"
    elif _enzyme == "[RK]":
        _enzyme = "Trypsin/P"

    fixed_mods_list = list(params.loc[params.index.str.contains("residue, modification mass")].dropna()) # "sage_database_static_mods	C:57.021465"
    var_mods_list = list(params.loc[params.index.str.contains("residue, potential modification mass")].dropna()) # "sage_database_variable_mods	M:15.994915 ^E:-18.010565 ^Q:-17.026548"

    # Add "hidden" modifications when using X!Tandem:
    if params.loc["AnalysisSoftware_name"] == "X!Tandem" or params.loc["AnalysisSoftware_name"] == "X! Tandem":
        if params.loc["protein, quick acetyl"] == "yes":
            var_mods_list.append("Acetyl(N-term)")
        if params.loc["protein, quick pyrolidone"] == "yes":
            var_mods_list.append("Pyrolidone(N-term)")

    # Create and return a ProteoBenchParameters object with the extracted values
    params = ProteoBenchParameters(
        software_name="i2MassChroQ",
        software_version=params.loc["i2MassChroQ_VERSION"],
        search_engine=params.loc["AnalysisSoftware_name"],
        search_engine_version=str(params.loc["AnalysisSoftware_version"] or ""),
        ident_fdr_psm=float(params.loc["psm_fdr"]),
        ident_fdr_peptide=float(params.loc["peptide_fdr"]),
        ident_fdr_protein=float(params.loc["protein_fdr"]),
        # set match between runs to True if it is enabled
        enable_match_between_runs=True if params.loc["mcq_mbr"] == "T" else False,
        precursor_mass_tolerance="[-" + _tol_prec_lower + ", " + _tol_prec_upper + "]",
        fragment_mass_tolerance="[-" + _tol_frag + ", " + _tol_frag + "]",
        enzyme=_enzyme,
        allowed_miscleavages=max_cleavage,
        min_peptide_length=None,  # xtandem: "spectrum, minimum fragment mz" / for sage: "sage_database_enzyme_min_len	5"
        max_peptide_length=None,  # xtandem: Not mentioned, up to 38 AA in peptides / for sage: "sage_database_enzyme_max_len	50"
        fixed_mods=";".join(fixed_mods_list),
        variable_mods=";".join(var_mods_list),
        max_mods=None, # "sage_database_max_variable_mods	2"
        min_precursor_charge=1,  # xtandem: Fixed in software / for sage maybe: "sage_database_min_ion_index	2" (I have to check the documentation)
        max_precursor_charge=int(params.loc["spectrum, maximum parent charge"]),
    )

    return params


if __name__ == "__main__":
    """
    Reads i2MassChroQ parameter files, extracts parameters, and writes them to CSV files.
    """
    # List of parameter file paths
    for fname in [
        "../../../test/params/i2mproteobench_2pep_fdr01psm_fdr01prot_xtandem.tsv",
    ]:
        file = pathlib.Path(fname)

        # Read the parameter file to extract parameters
        params = pd.read_csv(file, sep="\t", header=None, index_col=0).squeeze()
        params = extract_params(file.with_suffix(".tsv"))

        # Convert the parameters to a dictionary and then to a pandas Series
        data_dict = params.__dict__
        series = pd.Series(data_dict)
        print(series)

        # Write the Series to a CSV file
        series.to_csv(file.parent / (file.stem + "_sel.csv"))
