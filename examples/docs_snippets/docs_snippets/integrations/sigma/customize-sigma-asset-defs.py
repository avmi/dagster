from dagster_sigma import (
    DagsterSigmaTranslator,
    SigmaBaseUrl,
    SigmaOrganization,
    SigmaWorkbook,
    load_sigma_asset_specs,
)

import dagster as dg

sigma_organization = SigmaOrganization(
    base_url=SigmaBaseUrl.AWS_US,
    client_id=dg.EnvVar("SIGMA_CLIENT_ID"),
    client_secret=dg.EnvVar("SIGMA_CLIENT_SECRET"),
)


# A translator class lets us customize properties of the built Sigma assets, such as the owners or asset key
class MyCustomSigmaTranslator(DagsterSigmaTranslator):
    def get_workbook_spec(self, data: SigmaWorkbook) -> dg.AssetSpec:
        # Adds a custom team owner tag to all reports
        return super().get_asset_spec(data)._replace(owners=["my_team"])


sigma_specs = load_sigma_asset_specs(
    sigma_organization, dagster_sigma_translator=MyCustomSigmaTranslator
)
defs = dg.Definitions(assets=[*sigma_specs], resources={"sigma": sigma_organization})
