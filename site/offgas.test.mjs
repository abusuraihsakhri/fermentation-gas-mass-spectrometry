import test from 'node:test';
import assert from 'node:assert/strict';
import {calculateOffgas} from './offgas.mjs';

test('inert balance and respiration', () => {
  const r = calculateOffgas({flow:100,inletO2:.21,inletCO2:0,outletO2:.16,outletCO2:.04});
  assert.ok(Math.abs(r.outletFlow-98.75)<1e-10);
  assert.ok(Math.abs(r.our-5.2)<1e-10);
  assert.ok(Math.abs(r.cer-3.95)<1e-10);
  assert.ok(Math.abs(r.rq-(3.95/5.2))<1e-10);
});
test('no oxygen uptake yields no RQ', () => {
  const r=calculateOffgas({flow:100,inletO2:.21,inletCO2:.0004,outletO2:.21,outletCO2:.0004});
  assert.equal(r.rq,null);
});
test('invalid values are rejected',()=>{
  const a={flow:100,inletO2:.21,inletCO2:0,outletO2:.16,outletCO2:.04};
  for (const changes of [{flow:0},{flow:NaN},{inletO2:-1},{outletCO2:1},{inletO2:.8,inletCO2:.4}]) {
    assert.throws(()=>calculateOffgas({...a,...changes}));
  }
});
