# cpcalc V2: apparent c_p and c_v of fluids, mixtures and multiphase samples

V2 of the CL 202 Topic 5 tool. It keeps the spec's theory (Eqs. 1–23), simplifies the code and adds:
- a web interface with drop-down tables;
- a temperature-dependent database of 192 compounds, plus "add your own";
- a calculation sheet typeset in LaTeX, and theory pages.

## Install and run

```
pip install numpy scipy openpyxl streamlit pandas     # engine + interface
pip install thermo                                     # optional: "Find in thermo" for compounds not built in
pip install pytest sympy CoolProp                      # optional: tests and validation
```

From this folder (the one that contains `cpcalc/`):

| What | Command |
|---|---|
| **Web interface** | `python -m cpcalc ui` (opens in the browser) |
| List the examples | `python -m cpcalc examples` |
| Run one example in the terminal | `python -m cpcalc example D3 --explain` |
| Run every example | `python -m cpcalc example all` |
| Run your workbook | `python -m cpcalc run my_case.xlsx --explain --html sheet.html` |
| Excel template | `python -m cpcalc template --out my_case.xlsx` |
| All tests | `python -m cpcalc test` |

In the browser, `http://localhost:8501/?example=D6` opens that example directly. Screenshots are in `docs/`.

## The interface

- **1 System**: temperature, pressure, c_p / c_v / both, and phase amounts as volume or mass fractions.
  - **Phases table**: name, state, substance (searchable drop-down of every compound and mixture), amount, method.
  - **Mixtures**: any number of components, given as mole, mass or volume fractions, with an ideal / NRTL / Margules / Peng-Robinson model.
  - **Optional sweep**: over temperature, over the amount of one phase, or over a mixture composition.
- **2 Data**: every property the calculation needs at your T, with:
  - its status (database / yours / missing / outside the data range);
  - a *your value* column that always wins;
  - your own (T, value) curves.
- **3 Results**:
  - c_p,app, c_v,app, the phase table, warnings and assumptions;
  - one plain message per phase listing what is missing and where to find it;
  - a sweep chart;
  - downloads (HTML calculation sheet, text, JSON).
- **4 Calculation sheet**: the route taken for each phase (methods tried, what each lacked, which one ran), then every step. Each step shows the equation, the numbers substituted and the result, typeset in LaTeX with its spec equation number.
- **5 Theory**: eight short pages, each with its equations, the conditions under which they hold, and the code that uses them.
- **Sidebar**: examples, open or save an Excel workbook, add a compound, and browse the database.
  - *Find in thermo* looks up almost any compound by name, formula or CAS number and adds its data with sources.
  - *Add as my own* lets you type the data yourself.

## Database (192 compounds, temperature-dependent)

Built by `tools/build_database.py`. Every record names its source and kind:

- **About 130 fluids from CoolProp reference equations of state.** For each: liquid c_p, ρ, α_V and κ_T at 1 atm from the triple point to the normal boiling point; ideal-gas C_p; T_c, P_c, ω and M.
- **About 37 extra liquids from thermo/chemicals data methods.** These are alcohols, glycols, glycerol, acids and solvents. The data methods are Zábranský, DIPPR/Perry, VDI and CRC. κ_T for these comes from the COSTALD estimate and is labelled *estimated*.
- **24 particle solids**: oxides, metals, SiC and others.
  - c_p curves from NIST-JANAF, the NIST WebBook, Perry or CRC.
  - Density from CRC.
  - α_V and κ_T at room temperature (250–350 K) for Al2O3, Cu, Ag, Au, Al, Fe, Ni and Si. These come from NIST SRD 30, the CRC-based expansion table and the KnowledgeDoor isothermal bulk moduli.
- **Spec values**: the NIST-JANAF α-Al2O3 curve, and θ_D(Cu) = 343 K (marked unverified).

Data are never extrapolated. Outside a range the run stops and says which range exists, e.g. "water boils at 373.12 K at 1 atm".

## What changed from V1 (simpler)

- **Smaller engine**: 15 engine modules (2,624 lines) became 10 (1,863 lines), and the routing logic is one short table per phase state. The whole package, including the new web interface, is 3,350 lines (V1: 4,520).
- **Workbook**: nine sheets became six (Setup, Phases, Mixtures, Data, Curves, Pairs).
- **Data**: values are either a single number (optional T range) or a curve. Polynomial/Shomate input is gone: the database stores curves, and you can type points.
- **Phase states**: phases are liquid / solid / gas. Any of them can be a pure compound or a mixture, so the "solution" phase type is gone.
- **Assumptions**: no `allow_assumptions` switches. The model makes the obvious assumption and always lists it, and each one lowers the status. Examples: C_p^E = 0 for an ideal mixture, V^E = 0, k_ij = 0 when blank, and a value without a T range used at any T.
- **Error messages**: one message per phase, not one per property.
- **Removed features**: the overrides sheet, extrapolation on request, the pressure correction, absolute-mass amounts, pressure sweeps and the terminal menu (replaced by the web interface).

## Judgment calls

- **Evidence kinds for database data**: evaluated data (CoolProp reference equations, JANAF, Zábranský, DIPPR, CRC) count as *experimental*, so a run on database data can be "calculated". Estimation methods count as *estimated*, and placeholders as *illustrative*.
- **Liquids at another pressure**: they use the 1 atm database data. A note is shown above 6 bar.
- **Method order when set to auto**:
  - liquid: data only (Peng–Robinson only if you choose it, because liquid caloric errors reach about 26 %);
  - solid: data, then Debye;
  - gas: Peng–Robinson, then ideal gas.
- **D6 and D9 now behave differently from the spec**, because the database has solid α_V and κ_T:
  - D6 now computes c_v too.
  - D9 at 298 K uses the c_p − c_v identity, giving C_p − C_v of copper = 0.75 J/mol/K (v1 had estimated 0.71).

## Tests (121, all passing)

| Suite | Tests | Covers |
|---|---|---|
| Engine | 25 | units, lookup order, ranges, fractions, mixture bases, errors, warnings, status |
| Consistency | 18 | the spec identities and limits (TC suite) |
| Examples | 25 | every example; spec [R] targets for D1–D9 |
| Interface and I/O | 21 | workbook round trips (xlsx and CSV), reports, CLI, database integrity, engine independence, the web app (Streamlit AppTest) |
| Validation | 32 | VAL-01, VAL-02, VAL-05, VAL-07 and TC-17 against CoolProp; the database curves reproduce CoolProp within 0.1 %; deviations in `validate/error_table.txt`. SKIPPED without CoolProp. |

The engine (`cpcalc/engine.py` and the modules it imports) needs only NumPy and SciPy.
