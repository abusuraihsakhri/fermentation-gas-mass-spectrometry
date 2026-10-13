// Dry-gas inert-balance model. All fractions are 0–1; gas flow is mmol/min.
export function calculateOffgas({flow, inletO2, inletCO2, outletO2, outletCO2}) {
  const values = {flow, inletO2, inletCO2, outletO2, outletCO2};
  for (const [name, value] of Object.entries(values)) {
    if (typeof value !== 'number' || !Number.isFinite(value)) {
      throw new Error(`${name} must be a finite number`);
    }
  }
  if (flow <= 0) throw new Error('Inlet flow must be greater than zero');
  for (const name of ['inletO2','inletCO2','outletO2','outletCO2']) {
    if (values[name] < 0 || values[name] > 1) {
      throw new Error(`${name} must be a fraction between 0 and 1`);
    }
  }
  const inertIn = 1 - inletO2 - inletCO2;
  const inertOut = 1 - outletO2 - outletCO2;
  if (inertIn <= 0 || inertOut <= 0) {
    throw new Error('O2 + CO2 must be less than 100% for both gas streams');
  }
  const outletFlow = flow * inertIn / inertOut;
  const our = flow * inletO2 - outletFlow * outletO2;
  const cer = outletFlow * outletCO2 - flow * inletCO2;
  const warnings = [];
  if (our <= 0) warnings.push('Oxygen uptake is zero or negative; RQ is undefined.');
  if (cer < 0) warnings.push('Net CO2 evolution is negative; check measurements.');
  return {outletFlow, our, cer, rq: our > 0 ? cer / our : null, warnings};
}
