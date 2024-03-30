import warnings

from compute import my_round, sign_figs, chrom_coords_µ, LMS_energy, chop, Vλ_energy_and_LM_weights, \
    tangent_points_purple_line, chrom_coords_E, VisualData, xyz_interpolated_reference_system, linear_transformation_λ, \
    square_sum, compute_XYZ, compute_LMS, compute_MacLeod_Boynton_diagram, compute_Maxwellian_diagram
import numpy as np
import scipy.optimize
import scipy.interpolate


"""
    This module contains the modularized versions of the CIE functions found in compute.py. These are modularized
    in the sense that they give off a specific ndarray dependant on the parameters given (dictionary of URL params),
    unlike the original ones which give several ndarrays for all at once.
    Endpoint testing shows that there is a noticable speedup in request handling time when using these functions
    contrast of using their corresponding originals from compute.py, cutting time for some from 215~ ms to 42~ ms
    as an example.
"""

def compute_LMS_Modular(parameters):

    """
    A modularized version of 'compute_LMS(...)' from compute.py, based directly on it, just
    modularized to output either plot or result to enhance performance and lessen memory usage.

    Parameters
    ----------
    parameters: Dictionary of URL parameters.

    Returns
    -------
    A ndarray of LMS function given the parameters.

    """

    # compute.py line 1568
    variation = my_round(np.arange(parameters['λ_min'], parameters['λ_max'] + .01, .1), 1)
    if parameters['mode'] == "result":
        # compute.py line 1566
        variation = np.arange(parameters['λ_min'], parameters['λ_max'] + .01, parameters['λ_step'])
    # compute.py line 1565
    λ_all = my_round(np.arange(390., 830. + .01, .1), 1)
    # compute.py line 1575
    LMS_base_all = LMS_energy(parameters['field_size'], parameters['age'])[0]
    if parameters['base']:
        # compute.py line 1572
        LMS_base_all = LMS_energy(parameters['field_size'], parameters['age'], base=True)[0]
    # compute.py line 1585
    (λ_all, L, M, S) = LMS_base_all.T

    # compute.py lines 1586-1588
    L_spline = scipy.interpolate.InterpolatedUnivariateSpline(λ_all, L)
    M_spline = scipy.interpolate.InterpolatedUnivariateSpline(λ_all, M)
    S_spline = scipy.interpolate.InterpolatedUnivariateSpline(λ_all, S)

    # compute.py lines 763-768
    LMS_sf = 6
    logLMS_dp = 5
    if parameters['base']:
        LMS_sf = 9
        logLMS_dp = 8

    # compute.py lines 770-772
    (La, Ma, Sa) = np.array([sign_figs(L_spline(variation), LMS_sf),
                          sign_figs(M_spline(variation), LMS_sf),
                          sign_figs(S_spline(variation), LMS_sf)])

    # compute.py line 773
    LMS = chop(np.array([variation, La, Ma, Sa]).T)

    # compute.py lines 776-779
    if parameters['log']:
        LMS[:, 1:][LMS[:, 1:] == 0] = -np.inf
        LMS[:, 1:][LMS[:, 1:] > 0] = my_round(
            np.log10(LMS[:, 1:][LMS[:, 1:] > 0]), logLMS_dp)
        return chop(LMS)
    else:
        # compute.py line 779
        return chop(LMS)


def compute_MacLeod_Modular(parameters):

    """
    A modularized version of 'compute_MacLeod_Boynton_diagram(...)' from compute.py, modularized
    to give plots and results separately.

    Parameters
    ----------
    parameters: Dictionary of URL parameters.

    Returns
    -------
    A ndarray of MacLeod-Boynton function given the parameters.

    """

    # MacLeod uses LMS-base for calculations, needs that
    parameters['base'] = True
    parameters['log'] = False
    # the "result" for lms_mb_tg_purple is dependent on "plot" for lms_mb_tg_purple,
    # uses this trick to lessen code
    temp = parameters.copy()
    if parameters['purple']:
        temp['mode'] = "plot"
    LMS_base = compute_LMS_Modular(temp)
    # compute.py, line 1580
    (Vλ_std_all, LM_weights) = Vλ_energy_and_LM_weights(parameters['field_size'], parameters['age'])
    # compute.py, line 1566
    λ_spec = np.arange(parameters['λ_min'], parameters['λ_max'] + .01, parameters['λ_step'])
    # compute.py line 1591
    (λ_all, V_std_all) = Vλ_std_all.T
    # compute.py line 1595
    V_std_spline = scipy.interpolate.InterpolatedUnivariateSpline(λ_all, V_std_all)
    # compute.py line 1602
    Vλ_std_spec = np.array([λ_spec, V_std_spline(λ_spec)]).T

    # compute.py line 850
    V_spec = (Vλ_std_spec.T)[1]
    # compute.py line 848
    S_all = ((LMS_energy(parameters['field_size'],
                            parameters['age'], base=True)[0]).T)[3]
    # compute.py 849
    V_all = (Vλ_std_all.T)[1]
    # compute.py 851
    (κL, κM) = LM_weights
    (λ_factor, L, M, S) = LMS_base.T

    # compute.py, line 852
    κS = 1 / np.max(S_all / V_all)

    # parameter treatment:

    def illuminantE():

        """
        Small internal function for calculation of Illuminant E for MacLeod-Boynton;
        the plots and result versions share the same code mostly, so an internal function
        like this may be ideal to reduce code.
        Doesn't need parameters as it is an internal function declared after the declaration
        of variables necessary.

        Returns
        -------
        The plot for MacLeod-Boynton's (given parameters) Illuminant E.

        """

        # compute.py, line 866
        [L_mb_E, M_mb_E, S_mb_E] = [κL * np.sum(L), κM * np.sum(M), κS * np.sum(S)]
        # compute.py line 869
        V_E = sign_figs(np.array(L_mb_E + M_mb_E), 7)
        # compute.py, line 870
        lms_mb_E_plot = np.array([L_mb_E / V_E, M_mb_E / V_E, S_mb_E / V_E])
        return lms_mb_E_plot

    if parameters['norm']:
        # compute.py, line 880
        return chop(np.array([κL, κM, κS]))

    if parameters['mode'] == "result": # result
        if parameters['white']:
            lms_mb_E_plot = illuminantE()
            # compute.py, line 873
            lms_mb_E = my_round(lms_mb_E_plot, 6)
            return lms_mb_E
        else:
            # compute.py, line 854/861
            lms_mb_spec = np.array([λ_factor,
                                    κL * L / V_spec,
                                    κM * M / V_spec,
                                    κS * S / V_spec]).T

            if parameters['purple']:
                # compute.py, lines 875-879
                lms_mb_tg_purple_plot = tangent_points_purple_line(
                    lms_mb_spec, MacLeod_Boynton=True)
                lms_mb_tg_purple = lms_mb_tg_purple_plot.copy()
                lms_mb_tg_purple[:, 0] = my_round(lms_mb_tg_purple[:, 0], 1)
                lms_mb_tg_purple[:, 1:] = my_round(lms_mb_tg_purple[:, 1:], 6)
                return chop(lms_mb_tg_purple)
            # compute.py, lines 858
            lms_mb_spec[:, 1:] = my_round(lms_mb_spec[:, 1:], 6)
            return chop(lms_mb_spec)
    else:
        if parameters['white']:
            # compute.py, line 866
            lms_mb_E_plot = illuminantE()
            return chop(lms_mb_E_plot)
        else:
            # compute.py, line 860
            V_plot = sign_figs(κL * L + κM * M, 7)
            # compute.py, line 861/854
            lms_mb_plot = np.array([λ_factor,
                                    κL * L / V_plot,
                                    κM * M / V_plot,
                                    κS * S / V_plot]).T
            if parameters['purple']:
                # compute.py, lines 875-876
                lms_mb_tg_purple_plot = tangent_points_purple_line(
                    lms_mb_plot, MacLeod_Boynton=True)
                return chop(lms_mb_tg_purple_plot)
            return chop(lms_mb_plot)

def compute_Maxwellian_Modular(parameters):

    """
    A modularized version of 'compute_Maxwellian_diagram(...)' from compute.py, modularized
    to give plots and results separately.

    Parameters
    ----------
    parameters: Dictionary of URL parameters.

    Returns
    -------
    A ndarray of Maxwellian chromaticity function given the parameters.

    """
    # parameter adjustment for LMS-base
    parameters['base'] = True
    parameters['log'] = False
    # specific results are dependent on other plot/result values
    temp = parameters.copy()
    if parameters['purple']:
        temp['mode'] = "plot"
    elif parameters['norm']:
        temp['mode'] = "result"

    LMS_base = compute_LMS_Modular(temp)

    # compute.py, line 932
    (λ_factor, L, M, S) = LMS_base.T
    # compute.py, lines 935-937
    (kL, kM, kS) = (1. / np.sum(L), 1. / np.sum(M), 1. / np.sum(S))
    LMS_spec_N = np.array([λ_factor, kL * L, kM * M, kS * S]).T
    lms_mw_spec = chrom_coords_µ(LMS_spec_N)

    # parameter treatment:

    if parameters['norm']:
        # compute.py, line 951
        return chop(np.array([kL, kM, kS]))
    if parameters['mode'] == "result":
        if parameters['purple']:
            # compute.py, lines 947-950
            lms_mw_tg_purple_plot = tangent_points_purple_line(lms_mw_spec)
            lms_mw_tg_purple = lms_mw_tg_purple_plot.copy()
            lms_mw_tg_purple[:, 0] = my_round(lms_mw_tg_purple[:, 0], 1)
            lms_mw_tg_purple[:, 1:] = my_round(lms_mw_tg_purple[:, 1:], 6)
            return chop(lms_mw_tg_purple)
        elif parameters['white']:
            # compute.py, lines 944-945
            lms_mw_E_plot = chrom_coords_E(LMS_spec_N)
            return chop(my_round(lms_mw_E_plot, 6))
        else:
            # compute.py, lines 937-938
            lms_mw_spec = chrom_coords_µ(LMS_spec_N)
            lms_mw_spec[:, 1:] = my_round(lms_mw_spec[:, 1:], 6)
            return chop(lms_mw_spec)
    else:
        if parameters['purple']:
            # compute.py, line 942
            LMS_purple_plot = chrom_coords_µ(LMS_spec_N)
            # compute.py, line 947
            return chop(tangent_points_purple_line(LMS_purple_plot))
        elif parameters['white']:
            # compute.py, line 944
            return chop(chrom_coords_E(LMS_spec_N))
        else:
            # compute.py, line 942
            return chop(chrom_coords_µ(LMS_spec_N))

def compute_XYZ_Modular(parameters):
    """
    A modularized version of the original 'compute_XYZ(...)' from compute.py.

    Parameters
    ----------
    parameters: A dictionary containing the processed information from URL parameters.

    Returns
    -------
    A ndarray of CIE cone-fundamental-based XYZ tristimulus functions given the parameters.

    """
    # XYZ uses LMS-base for calculations, needs that
    parameters['base'] = True
    parameters['log'] = False

    temp = parameters.copy()
    temp['mode'] = "result"
    LMS_base_result = compute_LMS_Modular(temp)

    # compute.py, line 1697
    xyz_reference = xyz_interpolated_reference_system(
        parameters['field_size'], VisualData.XYZ31.copy(), VisualData.XYZ64.copy())

    # compute.py, line 1580
    (Vλ_std_all, LM_weights) = Vλ_energy_and_LM_weights(parameters['field_size'], parameters['age'])

    # compute.py line 1575
    LMS_base_all = LMS_energy(parameters['field_size'], parameters['age'], base=True)[0]
    # compute.py line 1585
    (λ_all, L, M, S) = LMS_base_all.T

    (λ_all, V_std_all) = Vλ_std_all.T
    # compute.py lines 1586-1588
    L_spline = scipy.interpolate.InterpolatedUnivariateSpline(λ_all, L)
    M_spline = scipy.interpolate.InterpolatedUnivariateSpline(λ_all, M)
    S_spline = scipy.interpolate.InterpolatedUnivariateSpline(λ_all, S)
    V_spline = scipy.interpolate.InterpolatedUnivariateSpline(λ_all, V_std_all)

    # compute.py, lines 1019-1060
    xyz_ref = xyz_reference
    (a21, a22) = LM_weights
    LMS_main = LMS_base_all[::10]
    (λ_main, L_main, M_main, S_main) = LMS_main.T
    V_main = sign_figs(a21 * L_main + a22 * M_main, 7)
    a33 = my_round(V_main.sum() / S_main.sum(), 8)
    λ_x_min_ref = 502
    ok = False
    while not ok:
        with warnings.catch_warnings():
            warnings.simplefilter('ignore')
            a13 = scipy.optimize.fmin(
                square_sum, 0.39, (a21, a22, a33,
                                   L_spline, M_spline, S_spline,
                                   V_spline,
                                   λ_main, λ_x_min_ref,
                                   xyz_ref, False),
                xtol=10 ** (-(10)), disp=False)  # exp: -(mat_dp + 2) = -10
        trans_mat, λ_x_min_ref, ok = (
            square_sum(a13, a21, a22, a33,
                       L_spline, M_spline, S_spline,
                       V_spline,
                       λ_main, λ_x_min_ref,
                       xyz_ref, True)[1:])
        # Compute renormalized transformation matrix
    (λ_spec,
     X_exact_spec,
     Y_exact_spec,
     Z_exact_spec) = linear_transformation_λ(trans_mat, LMS_base_result).T
    if ((λ_spec[0] == 390. and λ_spec[-1] == 830.) and
            (my_round(λ_spec[1] - λ_spec[0], 1) ==
             1.0)):
        trans_mat_N = trans_mat
    else:
        (X_exact_sum, Y_exact_sum, Z_exact_sum) = (np.sum(X_exact_spec),
                                                   np.sum(Y_exact_spec),
                                                   np.sum(Z_exact_spec))
        trans_mat_N = my_round(trans_mat * ([Y_exact_sum / X_exact_sum],
                                            [1],
                                            [Y_exact_sum / Z_exact_sum]), 8)
    # parameter treatment
    if parameters['trans']:
        if parameters['norm']:
            return chop(trans_mat_N)
        else:
            return chop(trans_mat)

    # calculations for plot and result in XYZ are mostly the same, just
    # a difference in what LMS result they use for linear_transformation_λ(...) below
    # changing this should work fine
    if parameters['mode'] == "plot":
        LMS_base_result = compute_LMS_Modular(parameters)

    # compute.py, lines 1060-1075
    if parameters['norm']:
        XYZ_normalized = linear_transformation_λ(trans_mat_N, LMS_base_result)
        XYZ_normalized[:, 1:] = sign_figs(XYZ_normalized[:, 1:], 7)
        return chop(XYZ_normalized)
    else:
        XYZ = linear_transformation_λ(trans_mat, LMS_base_result)
        XYZ[:, 1:] = sign_figs(XYZ[:, 1:], 7)
        return chop(XYZ)

def compute_XY_modular(parameters):
    """
    A modularized version of 'compute_xy_diagram(...)' from compute.py.

    Parameters
    ----------
    parameters: A dictionary of the processed information from URL parameters.

    Returns
    -------
    A ndarray of CIE cone-fundamental-based xyz chromaticity coordinates given the parameters.

    """

    temp = parameters.copy()
    # requires XYZ for calculations, uses function above alongside the same parameters
    xyz = compute_XYZ_Modular(temp)

    # no checking for normalization; calculations for renormalized and non-renormalized
    # remain the same
    if not parameters['purple']:
        # compute.py, lines 1173-1189
        if not parameters['white']:
            xyz_spec_N = chrom_coords_µ(xyz)
            if parameters['mode'] == "plot":
                return xyz_spec_N
            else:
                xyz_spec_N[:, 1:] = my_round(xyz_spec_N[:, 1:], 5)
                return xyz_spec_N
        else:
            xyz_E_plot_N = chrom_coords_E(xyz)
            if parameters['mode'] == "plot":
                return xyz_E_plot_N
            else:
                xyz_E_N = my_round(xyz_E_plot_N, 5)
                return xyz_E_N
    else:
        if parameters['mode'] is not "plot":
            temp['mode'] = "plot"
            xyz = compute_XYZ_Modular(temp)
        # compute.py, line 1180
        XYZ = chrom_coords_µ(xyz)
        # compute.py, lines 1193
        (xyz_purple_plot, XYZ_purple_plot) = tangent_points_purple_line(XYZ, False, xyz)
        if parameters['mode'] == "plot":
            if parameters['XYZ']:
                return XYZ_purple_plot
            else:
                return xyz_purple_plot
        else:
            if parameters['XYZ']:
                # compute.py, lines 1198-1200
                XYZ_purple_plot[:, 0] = my_round(XYZ_purple_plot[:, 0], 1)
                XYZ_purple_plot[:, 1:] = my_round(XYZ_purple_plot[:, 1:], 7)
                return XYZ_purple_plot
            else:
                # compute.py, lines 1195-1197
                xyz_purple_plot[:, 0] = my_round(xyz_purple_plot[:, 0], 1)
                xyz_purple_plot[:, 1:] = my_round(xyz_purple_plot[:, 1:], 5)
                return xyz_purple_plot