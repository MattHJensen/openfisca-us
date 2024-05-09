from policyengine_us.model_api import *


class nc_use_tax(Variable):
    value_type = float
    entity = TaxUnit
    label = "North Carolina use tax"
    unit = USD
    definition_period = YEAR
    defined_for = StateCode.NC

    def formula(tax_unit, period, parameters):
        agi = tax_unit("adjusted_gross_income", period)
        p = parameters(period).gov.states.nc.tax.use_tax
        use_tax_constant_rate = p.cap.calc(
            agi
        )  # when agi less than certain threshold, use tax is a dollar value based on amount
        use_tax_fraction_rate = (
            p.rate.calc(agi) * agi
        )  # when agi is more than the threshold, use tax is a fractional amount of agi
        return use_tax_constant_rate + use_tax_fraction_rate
