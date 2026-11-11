"""Theory pages shown in the UI (LaTeX) and in the terminal (plain text).
Data only: each topic has a short text, numbered equations, the conditions under
which they hold, and where the code uses them."""

TOPICS = [
    {
        "title": "1. What is an apparent heat capacity?",
        "text": "A sample made of several phases (a liquid with particles, an emulsion, a slurry) is heated slowly. "
                "Its apparent heat capacity is the heat taken up per kelvin and per kilogram of sample. "
                "At constant pressure it is the temperature derivative of the total enthalpy; at constant volume, "
                "of the total internal energy.",
        "equations": [
            (r"c_{p,\mathrm{app}} \equiv \frac{1}{m}\left(\frac{\partial H_{\mathrm{tot}}}{\partial T}\right)_P,\qquad "
             r"c_{v,\mathrm{app}} \equiv \frac{1}{m}\left(\frac{\partial U_{\mathrm{tot}}}{\partial T}\right)_V", "(1) definitions"),
            (r"H_{\mathrm{tot}} = \sum_k m_k\,h_k(T,P,\mathbf{x}_k) + H^{\sigma}", "(1) enthalpy is additive over phases (interface separated)"),
            (r"c_{p,\mathrm{app}} = \sum_k w_k\,c_{p,k},\qquad w_k = \frac{m_k}{m}", "(2) with the interface term neglected"),
        ],
        "holds": "slow heating; one T and one P; no melting, boiling, dissolution or reaction; interface neglected.",
        "code": "engine.assemble, sample.cp_apparent",
    },
    {
        "title": "2. From c_p to c_v: the calculus of thermodynamics",
        "text": "c_p and c_v differ by the work of expansion. The triple-product rule and a Maxwell relation give the "
                "difference from the expansivity and the compressibility, which are measurable for any phase.",
        "equations": [
            (r"C_p - C_v = T\left(\frac{\partial P}{\partial T}\right)_V\left(\frac{\partial V}{\partial T}\right)_P "
             r"= -T\frac{(\partial P/\partial T)_V^2}{(\partial P/\partial V)_T} = \frac{T\,v\,\alpha_V^2}{\kappa_T}", "(3)"),
            (r"c_p - c_v = \frac{T\,\alpha_V^2}{\rho\,\kappa_T},\qquad \alpha_V = \frac{1}{V}\left(\frac{\partial V}{\partial T}\right)_P,"
             r"\quad \kappa_T = -\frac{1}{V}\left(\frac{\partial V}{\partial P}\right)_T", "(3), (12) specific form"),
            (r"\left(\frac{\partial C_v}{\partial V}\right)_T = T\left(\frac{\partial^2 P}{\partial T^2}\right)_V,\qquad "
             r"\left(\frac{\partial C_p}{\partial P}\right)_T = -T\left(\frac{\partial^2 V}{\partial T^2}\right)_P", "(4)"),
        ],
        "holds": "any phase of fixed composition. For water near 4 C alpha_V = 0, so c_p = c_v there.",
        "code": "pure.cp_minus_cv, engine.cv_identity",
    },
    {
        "title": "3. Gases and fluids: Peng-Robinson departure functions",
        "text": "A real fluid is an ideal gas plus a departure. The ideal-gas part C_p^ig(T) comes from data; the "
                "departure comes from the Peng-Robinson equation of state. The cubic in Z can have three roots: the "
                "middle one is never used, and of the outer two the one with the lower fugacity coefficient is stable.",
        "equations": [
            (r"P = \frac{RT}{v-b} - \frac{a(T)}{v^2+2bv-b^2},\quad a = 0.45724\frac{R^2T_c^2}{P_c}\left[1+m\left(1-\sqrt{T/T_c}\right)\right]^2,"
             r"\quad b = 0.07780\frac{RT_c}{P_c}", "(6)-(7)"),
            (r"C_v = C_p^{ig} - R + C_v^R,\qquad C_v^R = \frac{T\,a''}{2\sqrt2\,b}\ln\frac{v+(1+\sqrt2)b}{v+(1-\sqrt2)b}", "(5), (9)"),
            (r"Z^3-(1-B)Z^2+(A-3B^2-2B)Z-(AB-B^2-B^3)=0,\quad A=\frac{aP}{(RT)^2},\ B=\frac{bP}{RT}", "(10)"),
            (r"\ln\varphi = Z-1-\ln(Z-B)-\frac{A}{2\sqrt2 B}\ln\frac{Z+(1+\sqrt2)B}{Z+(1-\sqrt2)B}", "(11) choosing the stable root"),
        ],
        "holds": "within ~1 % for vapours; only fair for liquids (C_p errors 4-26 %), poor for water and alcohols and near "
                 "the critical point. For liquids the data method is used first.",
        "code": "pure.pr_parameters, pure.pr_state, pure.select_root",
    },
    {
        "title": "4. Liquids and solids from data; the Debye model",
        "text": "For a condensed phase c_p is taken from data (a value or a curve against T) and c_v follows from the "
                "identity of topic 2. When no c_p data exist for a solid, the Debye model gives C_v from one parameter, "
                "the Debye temperature.",
        "equations": [
            (r"\alpha_V = -\frac{1}{\rho}\frac{d\rho}{dT},\qquad c_v = c_p - \frac{T\,\alpha_V^2}{\rho\,\kappa_T}", "(12)"),
            (r"C_v = 9nR\left(\frac{T}{\theta_D}\right)^3\int_0^{\theta_D/T}\frac{x^4e^x}{(e^x-1)^2}\,dx + \gamma_eT,\qquad "
             r"C_p = C_v + \frac{T\,v\,\alpha_V^2}{\kappa_T}", "(13)"),
            (r"T \ll \theta_D:\ C_v \to \frac{12\pi^4}{5}nR\left(\frac{T}{\theta_D}\right)^3,\qquad T \gg \theta_D:\ C_v \to 3nR", "limits"),
        ],
        "holds": "data only inside their temperature range (never extrapolated). Debye: one theta_D, best for monatomic crystals.",
        "code": "engine.m_data, engine.m_debye, pure.debye_cv",
    },
    {
        "title": "5. Mixtures (solutions)",
        "text": "An ideal mixture adds its components by mass. A real mixture adds an excess heat capacity, the second "
                "temperature derivative of the excess Gibbs energy. Constant-parameter models give C_p^E = 0, so a "
                "temperature-dependent parameter is needed. c_v of a mixture is not the average of the c_v of its parts.",
        "equations": [
            (r"c_p = \sum_i w_i\,c_{p,i} + \frac{C_p^E}{M},\qquad C_p^E = -T\left(\frac{\partial^2G^E}{\partial T^2}\right)_{P,x},"
             r"\quad H^E = -T^2\frac{\partial(G^E/T)}{\partial T}", "(14)"),
            (r"\frac{G^E}{RT} = x_1x_2\left(A+\frac{B}{T}+D\ln T\right)\ \Rightarrow\ H^E = Rx_1x_2(B-DT),\ C_p^E = -RDx_1x_2", "(15) Margules"),
            (r"\frac{G^E}{RT} = x_1x_2\left[\frac{\tau_{21}G_{21}}{x_1+x_2G_{21}}+\frac{\tau_{12}G_{12}}{x_2+x_1G_{12}}\right],"
             r"\ G_{ij}=e^{-\alpha\tau_{ij}},\ \tau_{ij}=a_{ij}+\frac{b_{ij}}{T}+e_{ij}\ln T", "(16) NRTL"),
            (r"c_p - c_v = \frac{T\left(\sum_i w_i\alpha_i/\rho_i\right)^2}{\sum_i w_i\kappa_i/\rho_i}\quad(V^E = 0)", "(19)"),
            (r"a_m = \sum_i\sum_j x_ix_j(1-k_{ij})\sqrt{a_ia_j},\qquad b_m = \sum_i x_ib_i", "(17) mixing rule for Peng-Robinson"),
        ],
        "holds": "NRTL and Margules: two components; parameters should be fitted to C_p^E or H^E data. Mixture "
                 "fractions can be given as mole, mass or volume (of the pure components) fractions.",
        "code": "engine.mix_condensed, engine.mix_peng_robinson, mixtures.py",
    },
    {
        "title": "6. The whole sample: c_p and c_v",
        "text": "Phase volume fractions become mass fractions through the densities. c_p of the sample is the mass "
                "average (thermal-equilibrium model). c_v is NOT the mass average of the phase c_v: at constant total "
                "volume the phases push on each other. The whole-sample identity gives it exactly, and the mass "
                "average is only a lower bound.",
        "equations": [
            (r"w_k = \frac{\phi_k\rho_k}{\sum_j\phi_j\rho_j},\qquad c_{p,\mathrm{app}} = \sum_k w_k\,c_{p,k} "
             r"= \frac{\sum_k\phi_k(\rho c_p)_k}{\rho_s}", "(20)"),
            (r"c_{p,\mathrm{app}} - c_{v,\mathrm{app}} = \frac{T\left(\sum_k\phi_k\alpha_k\right)^2}{\rho_s\sum_k\phi_k\kappa_k}", "(21)"),
            (r"c_{v,\mathrm{app}} - \sum_k w_kc_{v,k} = \frac{T}{\rho_s\sum_j\phi_j\kappa_j}\sum_{k<l}\phi_k\phi_l\kappa_k\kappa_l"
             r"\left(\frac{\alpha_k}{\kappa_k}-\frac{\alpha_l}{\kappa_l}\right)^2 \geq 0", "(22)-(23)"),
            (r"c_p^{\mathrm{Pak\text{-}Cho}} = \sum_k\phi_k\,c_{p,k}\quad\text{(diagnostic only: weights a per-mass quantity by volume)}", "Pak-Cho form"),
        ],
        "holds": "needs rho of every phase (for volume fractions) and alpha_V, kappa_T of every phase (for c_v).",
        "code": "engine.assemble, sample.py",
    },
    {
        "title": "7. Where the numbers come from",
        "text": "For every property the program takes, in this order: your value (if valid at T), your curve, the "
                "database value, the database curve, then a derivation (alpha_V from a density curve). Your data always "
                "win. Nothing is extrapolated: outside a range the run stops and says which range exists. If a method "
                "lacks inputs the next method is tried; if none works, one message lists what each method needs.",
        "equations": [],
        "holds": "the database: CoolProp reference equations (about 130 fluids), thermo/chemicals evaluated data "
                 "(Zabransky, DIPPR, VDI, NIST-JANAF, NIST WebBook, Perry, CRC) and the spec values. Liquid data are at 1 atm.",
        "code": "properties.find",
    },
    {
        "title": "8. Evidence and status",
        "text": "Each number carries its kind: experimental (measured or evaluated data), derived (computed from such "
                "data), unspecified, estimated (an estimation method), illustrative (a placeholder). A result is only "
                "as strong as its weakest input. Status: calculated; calculated under assumptions (an assumption, a "
                "warning or weaker data were used: all are listed); not calculable (nothing is printed).",
        "equations": [],
        "holds": "assumptions the program may make (always listed): C_p^E = 0 for an ideal mixture, V^E = 0 for mixture "
                 "volumes, k_ij = 0 when blank, gamma_e = 0 when blank, a value without a T range used at any T.",
        "code": "engine.build_result",
    },
]
