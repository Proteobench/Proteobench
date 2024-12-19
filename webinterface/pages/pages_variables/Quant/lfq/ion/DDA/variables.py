from dataclasses import dataclass, field
from typing import List, Type

from pages.texts.generic_texts import WebpageTexts


@dataclass
class VariablesDDAQuant:
    all_datapoints: str = "all_datapoints"
    all_datapoints_submission: str = "all_datapoints_submission"
    input_df_submission: str = "input_df_submission"
    result_performance_submission: str = "result_performance_submission"
    submit: str = "submit"
    fig_logfc: str = "fig_logfc"
    fig_metric: str = "fig_metric"
    fig_cv: str = "fig_CV_violinplot"
    result_perf: str = "result_perf"
    meta_data: str = "meta_data"
    input_df: str = "input_df"
    meta_file_uploader_uuid: str = "meta_file_uploader_uuid"
    comments_submission_uuid: str = "comments_submission_uuid"
    check_submission_uuid: str = "check_submission_uuid"
    meta_data_text: str = "comments_for_submission"
    check_submission: str = "heck_submission"
    button_submission_uuid: str = "button_submission_uuid"
    df_head: str = "df_head"
    placeholder_fig_compare: str = "placeholder_fig_compare"

    all_datapoints_submitted: str = "all_datapoints_submitted"
    placeholder_table_submitted: str = "placeholder_table_submitted"
    placeholder_slider_submitted: str = "placeholder_slider_submitted"
    highlight_list_submitted: List[str] = field(default_factory=list)
    selectbox_id_submitted_uuid: str = "selectbox_id_submitted"
    selectbox_id_uuid: str = "selectbox_id"
    slider_id_submitted_uuid: str = "slider_id_submitted"
    slider_id_uuid: str = "slider_id"
    download_selector_id_uuid: str = "download_selector_id"
    table_id_uuid: str = "table_id"

    placeholder_table: str = "placeholder_table"
    placeholder_slider: str = "placeholder_slider"

    placeholder_downloads_container: str = "placeholder_downloads_container"
    highlight_list: List[str] = field(default_factory=list)
    first_new_plot: bool = True
    default_val_slider: int = 3
    beta_warning: bool = True
    github_link_pr: str = "github.com/Proteobot/Results_quant_ion_DDA.git"

    additional_params_json: str = "../webinterface/configuration/dda_quant.json"

    description_module_md: str = "pages/markdown_files/Quant/lfq/ion/DDA/introduction_DDA_quan_ions.md"
    description_files_md: str = "pages/markdown_files/Quant/lfq/ion/DDA/file_description.md"
    description_input_file_md: str = "pages/markdown_files/Quant/lfq/ion/DDA/input_file_description.md"
    description_slider_md: str = "pages/markdown_files/Quant/lfq/ion/DDA/slider_description.md"
    description_table_md: str = "pages/markdown_files/Quant/lfq/ion/DDA/table_description.md"
    description_results_md: str = "pages/markdown_files/Quant/lfq/ion/DDA/result_description.md"
    description_submission_md: str = "pages/markdown_files/Quant/lfq/ion/DDA/submit_description.md"

    parse_settings_dir: str = "../proteobench/io/parsing/io_parse_settings/Quant/DDA"

    texts: Type[WebpageTexts] = WebpageTexts
    doc_url: str = "https://proteobench.readthedocs.io/en/latest/available-modules/2-quant-lfq-ion-dda/"

    title: str = "DDA Ion quantification"
