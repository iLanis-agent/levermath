// Lever Math engine: mass times distance on each side of a pivot, the distance that balances a mass, and where the pivot goes on a beam. Exact integers (tenths of a kg, hundredths of a m), results rounded half up.
function _p(t, err, intDigits, places, lo, hi) { // decimal text -> integer scaled by 10^places
  t = typeof t === "string" ? t.trim() : "";
  var m = new RegExp("^([0-9]{1," + intDigits + "})(?:\\.([0-9]{1," + places + "}))?$").exec(t);
  if (!m) throw new Error(err);
  var v = parseInt(m[1], 10) * Math.pow(10, places) + (m[2] ? parseInt(m[2].padEnd(places, "0"), 10) : 0);
  if (v < lo || v > hi) throw new Error(err);
  return v;
}
var _MASS = "each mass must be from 0.1 to 1000 kg with at most one decimal place";
var _DIST = "each distance must be from 0.01 to 20 m with at most two decimal places";
var _BEAM = "the beam must be from 0.1 to 20 m with at most one decimal place";
function _hu(n, d) { return Math.floor((2 * n + d) / (2 * d)); }
function _dec(v, places) {
  var base = Math.pow(10, places);
  var s = String(Math.floor(v / base)), f = String(v % base).padStart(places, "0").replace(/0+$/, "");
  return f ? s + "." + f : s;
}
function _kg(m) { return _dec(m, 1) + " kg"; }
function _m(d) { return _dec(d, 2) + " m"; }
function _tq(m, d) { return _dec(_hu(m * d, 10), 2) + " kg·m"; } // thousandths -> hundredths
function _in(m1, d1, m2, d2) {
  return { a: _p(m1, _MASS, 4, 1, 1, 10000), x: _p(d1, _DIST, 2, 2, 1, 2000), b: _p(m2, _MASS, 4, 1, 1, 10000), y: _p(d2, _DIST, 2, 2, 1, 2000) };
}

function balanceTruth(m1, d1, m2, d2) {
  var p = _in(m1, d1, m2, d2), t1 = p.a * p.x, t2 = p.b * p.y;   // thousandths of a kg·m
  var s = "Side one is " + _kg(p.a) + " at " + _m(p.x) + ", making " + _tq(p.a, p.x) + ". Side two is " + _kg(p.b) + " at " + _m(p.y) + ", making " + _tq(p.b, p.y) + ". ";
  if (t1 === t2) return s + "They balance.";
  var big = t1 > t2 ? "Side one" : "Side two";
  return s + big + " is heavier by " + _dec(_hu((t1 > t2 ? t1 - t2 : t2 - t1), 10), 2) + " kg·m.";
}
function matchTruth(m1, d1, m2) {
  var a = _p(m1, _MASS, 4, 1, 1, 10000), x = _p(d1, _DIST, 2, 2, 1, 2000), b = _p(m2, _MASS, 4, 1, 1, 10000);
  return "To balance " + _kg(a) + " at " + _m(x) + " with " + _kg(b) + " on the other side, put the " + _kg(b) + " at " + _m(_hu(a * x, b)) + " from the pivot.";
}
function fulcrumTruth(m1, m2, beam) {
  var a = _p(m1, _MASS, 4, 1, 1, 10000), b = _p(m2, _MASS, 4, 1, 1, 10000), L = _p(beam, _BEAM, 3, 1, 1, 200);
  var x1 = _hu(10 * b * L, a + b), x2 = _hu(10 * a * L, a + b);  // hundredths of a m from each end
  return "With " + _kg(a) + " at one end of a " + _dec(L, 1) + " m beam and " + _kg(b) + " at the other, the pivot goes " + _m(x1) + " from the " + _kg(a) + " end and " + _m(x2) + " from the " + _kg(b) + " end.";
}
