from openfisca_us.model_api import *


class ca_renters_tax_credit(Variable):
    value_type = float
    entity = TaxUnit
    label = "Renters Tax Credit"
    unit = USD
    documentation = (
        "https://casetext.com/statute/california-codes/california-revenue-and-taxation-code/division-2-other-taxes/part-10-personal-income-tax/chapter-2-imposition-of-tax/section-170535-credit-for-qualified-renter"
    )
    definition_period = YEAR

    def formula(tax_unit, period, parameters):
        # Check eligibility based on state, rent, filing status, and income.
        p = parameters(period).gov.state.ca.tax.income.credits.renter
        agi = tax_unit("adjusted_gross_income", period)
        rent = tax_unit("rent", period)
        filing_status = tax_unit("filing_status", period)
        in_ca = tax_unit.household("state_code_str", period) == "CA"
        income_cap = p.income_cap[filing_status]
        income_eligible = agi <= income_cap
        has_rent = rent > 0
        eligible = in_ca & income_eligible & has_rent
        # Determine amount if eligible based on filing status.
        amount_if_eligible = p.amount[filing_status]
        # Return eligibility * (amount if eligible).
        return eligible * amount_if_eligible
