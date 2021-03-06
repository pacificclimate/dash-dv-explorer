"""
This module simplifies and abstracts out accessing values from the
configuration. Not all config access uses these functions, but the gnarly
cases are centralized here.
"""

import os.path
from pkg_resources import resource_filename


def validate_filepath(filepath):
    filepath = resource_filename("dve", filepath)
    if not os.path.isfile(filepath):
        raise ValueError(f"'{filepath}' does not exist or is not a file")


def validate(config):
    """
    Validate a configuration. Specifically:
    - Check that all filepaths in use exist

    Raise a descriptive exception if validation fails.
    """
    for filepath in config["paths"].values():
        validate_filepath(filepath)

    for design_value_id in config["ui"]["dvs"]:
        dv_defn = config["dvs"][design_value_id]

        if dv_has_climate_regime(config, design_value_id, "historical"):
            for key in (
                "station_path",
                "input_model_path",
                "reconstruction_path",
                "table",
            ):
                validate_filepath(dv_defn[key])

        for fcf_id in config["ui"]["future_change_factors"]:
            validate_filepath(dv_defn["future_change_factor_paths"][fcf_id])


def dv_has_climate_regime(config, design_value_id, climate_regime):
    """
    Return a boolean indicating whether a DV has definitions for specific
    climate regime (historical or future) datasets.
    """
    return (
        "abs_units" if climate_regime == "historical" else "cf_units"
    ) in config["dvs"][design_value_id]


def dv_name(config, design_value_id):
    """
    Return the name of a design variable. Currently this is the internal
    id of the DV, so `config` is not used. That could conceivably change.
    """
    return design_value_id


def nice_units(config, units):
    try:
        definition = config["units"][units]
        return (
            definition["nice"],
            (" " if definition.get("separator", True) else ""),
        )
    except KeyError:
        return units, " "


def dv_units(config, design_value_id, climate_regime, nice=True):
    """
    Return the units of a given design variable, for historical or future
    projections.
    """
    units = config["dvs"][design_value_id][
        "abs_units" if climate_regime == "historical" else "cf_units"
    ]
    if not nice:
        return units
    return nice_units(config, units)[0]


def dv_label(
    config,
    design_value_id,
    climate_regime="historical",
    with_units=True,
    with_description=False,
):
    """
    Return the name, with optional description, and units of a DV.

    :param config:
    :param design_value_id:
    :param climate_regime:
    :param with_description:
    :return:
    """
    description = (
        f" [{config['dvs'][design_value_id]['description']}]"
        if with_description
        else ""
    )
    units = (
        f" ({dv_units(config, design_value_id, climate_regime)})"
        if with_units
        else ""
    )
    return f"{dv_name(config, design_value_id)}{description}{units}"


def dv_roundto(config, design_value_id, climate_regime):
    if dv_units(config, design_value_id, climate_regime) == "ratio":
        return config["dvs"][design_value_id]["ratio_roundto"]
    return config["dvs"][design_value_id]["roundto"]


def climate_regime_label(config, climate_regime, which="long"):
    return config["ui"]["labels"]["climate_regime"][climate_regime][which]


def historical_dataset_label(config, dataset_id):
    return config["ui"]["labels"]["historical_dataset"][dataset_id]


def future_change_factor_label(config, dataset_id, which="short", nice=True):
    units, separator = nice_units(config, "degC") if nice else ("degC", " ")
    return config["ui"]["labels"]["future_change_factors"][which].format(
        value=dataset_id, separator=separator, units=units
    )


def dataset_label(
    config,
    climate_regime,
    historical_dataset_id,
    future_dataset_id,
    which="short",
    nice=True,
):
    if climate_regime == "historical":
        return historical_dataset_label(config, historical_dataset_id)
    return future_change_factor_label(
        config, future_dataset_id, which=which, nice=nice
    )
