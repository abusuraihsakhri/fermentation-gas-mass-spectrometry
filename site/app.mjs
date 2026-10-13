import {calculateOffgas} from './offgas.mjs';

const ids = ['flow', 'inletO2', 'inletCO2', 'outletO2', 'outletCO2'];
const form = document.querySelector('#calculator');
const error = document.querySelector('#error');
const warningBox = document.querySelector('#warnings');
const exportButton = document.querySelector('#export');
const message = document.querySelector('#result-message');
let latest = null;

const fmt = (value) => value == null ? 'Undefined' : Number(value.toPrecision(7)).toLocaleString('en-US', {maximumFractionDigits: 6});

function clearResult() {
  latest = null;
  for (const id of ['our', 'cer', 'rq', 'outletFlow']) {
    document.getElementById(id).textContent = '—';
  }
  warningBox.textContent = '';
  exportButton.disabled = true;
}
form.addEventListener('submit', (event) => {
  event.preventDefault();
  error.textContent = '';
  clearResult();
  try {
    const values = {};
    for (const id of ids) {
      const input = document.getElementById(id);
      if (input.value.trim() === '') throw new Error('All five measurements are required.');
      values[id] = Number(input.value);
    }
    latest = {inputs: values, result: calculateOffgas({
      flow: values.flow,
      inletO2: values.inletO2 / 100,
      inletCO2: values.inletCO2 / 100,
      outletO2: values.outletO2 / 100,
      outletCO2: values.outletCO2 / 100,
    })};
    for (const id of ['our', 'cer', 'rq', 'outletFlow']) {
      document.getElementById(id).textContent = fmt(latest.result[id]);
    }
    warningBox.textContent = latest.result.warnings.join(' ');
    message.textContent = 'Values calculated locally from your measurements.';
    exportButton.disabled = false;
  } catch (err) {
    error.textContent = err instanceof Error ? err.message : 'Invalid measurements.';
    message.textContent = 'No valid result available.';
  }
});
form.addEventListener('reset', () => {
  clearResult();
  error.textContent = '';
  message.textContent = 'Enter measured gas concentrations and choose Calculate.';
});
exportButton.addEventListener('click', () => {
  if (!latest) return;
  const names = [...ids, 'outlet_flow_mmol_min', 'our_mmol_min', 'cer_mmol_min', 'rq'];
  const data = [...ids.map(id => latest.inputs[id]),latest.result.outletFlow,latest.result.our,
    latest.result.cer,latest.result.rq == null ? '' : latest.result.rq];
  const csv = names.join(',') + '\r\n' + data.join(',') + '\r\n';
  const url = URL.createObjectURL(new Blob([csv], {type:'text/csv;charset=utf-8'}));
  const anchor = document.createElement('a');
  anchor.href = url;
  anchor.download = 'offgas-results.csv';
  document.body.append(anchor);
  anchor.click();
  anchor.remove();
  setTimeout(() => URL.revokeObjectURL(url), 1000);
});
