import warnings

from compute import my_round, sign_figs, chrom_coords_µ, LMS_energy, chop, Vλ_energy_and_LM_weights, \
    tangent_points_purple_line, chrom_coords_E, VisualData, xyz_interpolated_reference_system, linear_transformation_λ, \
    square_sum, XYZ_purples, compute_CIE_standard_XYZ, LMS_quantal, compute_tabulated
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

    def inner_LMS(variation):
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

        if parameters['log']:
            LMS[:, 1:][LMS[:, 1:] == 0] = -np.inf
            LMS[:, 1:][LMS[:, 1:] > 0] = my_round(
                np.log10(LMS[:, 1:][LMS[:, 1:] > 0]), logLMS_dp)
            LMS[:, 0] = my_round(LMS[:, 0], 1)
            return chop(LMS)
        else:
            LMS[:, 0] = my_round(LMS[:, 0], 1)
            # compute.py line 779
            return chop(LMS)
        return LMS

    dict = {
        "result": inner_LMS(np.arange(parameters['λ_min'], parameters['λ_max'] + .01, parameters['λ_step'])),
        "plot": inner_LMS(my_round(np.arange(parameters['λ_min'], parameters['λ_max'] + .01, .1), 1))
    }

    return dict


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

    # parameter adjustment for LMS-base
    parameters['base'] = True
    parameters['log'] = False
    # specific results are dependent on other plot/result values
    LMS_results = compute_LMS_Modular(parameters)
    (λ_spec, L_spec, M_spec, S_spec) = LMS_results['result'].T
    (λ_plot, L_plot, M_plot, S_plot) = LMS_results['plot'].T

    (Vλ_all, LM_weights) = Vλ_energy_and_LM_weights(parameters['field_size'], parameters['age'])
    LMS_all = LMS_energy(parameters['field_size'], parameters['age'], base=True)[0]

    (λ_all, V_std_all) = Vλ_all.T
    V_std_spline = scipy.interpolate.InterpolatedUnivariateSpline(λ_all, V_std_all)

    Vλ_spec = np.array([λ_spec, V_std_spline(λ_spec)]).T

    S_all = (LMS_all.T)[3]
    V_all = (Vλ_all.T)[1]
    V_spec = (Vλ_spec.T)[1]


    (κL, κM) = LM_weights           # k: kappa (greek letter)
    κS = 1 / np.max(S_all / V_all)
    V_plot = sign_figs(κL * L_plot + κM * M_plot, 7)
    lms_mb_plot = np.array([λ_plot,
                            κL * L_plot / V_plot,
                            κM * M_plot / V_plot,
                            κS * S_plot / V_plot]).T

    if parameters['info']:
        [L_mb_E, M_mb_E, S_mb_E] = [κL * np.sum(L_spec),
                                    κM * np.sum(M_spec),
                                    κS * np.sum(S_spec)]
        V_E = sign_figs(np.array(L_mb_E + M_mb_E), 7)
        lms_mb_E_plot = np.array([L_mb_E / V_E,
                                  M_mb_E / V_E,
                                  S_mb_E / V_E])
        lms_mb_tg_purple_plot = tangent_points_purple_line(
            lms_mb_plot, MacLeod_Boynton=True)
        lms_mb_tg_purple = lms_mb_tg_purple_plot.copy()
        lms_mb_tg_purple[:, 0] = my_round(lms_mb_tg_purple[:, 0], 1)
        lms_mb_tg_purple[:, 1:] = my_round(lms_mb_tg_purple[:, 1:], 6)

        output = {
            "norm": np.array([κL, κM, κS]),
            "white": my_round(lms_mb_E_plot, 6),
            "tg_purple": lms_mb_tg_purple
        }
        return output
    else:
        # Compute spectral chromomaticity coordinates (for table)
        lms_mb_spec = np.array([λ_spec, κL * L_spec / V_spec, κM * M_spec / V_spec, κS * S_spec / V_spec]).T
        lms_mb_spec[:, 1:] = my_round(lms_mb_spec[:, 1:], 6)
        # Compute plot points for spectrum locus
        return {
            "result": lms_mb_spec,
            "plot": lms_mb_plot
        }


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

    LMS_results = compute_LMS_Modular(parameters)
    (λ_spec, L_spec, M_spec, S_spec) = LMS_results['result'].T
    (λ_plot, L_plot, M_plot, S_plot) = LMS_results['plot'].T

    (kL, kM, kS) = (1./np.sum(L_spec), 1./np.sum(M_spec), 1./np.sum(S_spec))
    LMS_spec_N = np.array([λ_spec, kL * L_spec, kM * M_spec, kS * S_spec]).T
    lms_mw_spec = chrom_coords_µ(LMS_spec_N)
    lms_mw_spec[:,1:] = my_round(lms_mw_spec[:,1:], 6)
    # Compute plot points for spectrum locus
    (cL, cM, cS) = (1./np.sum(L_plot), 1./np.sum(M_plot), 1./np.sum(S_plot))
    LMS_plot_N = np.array([λ_plot, cL * L_plot, cM * M_plot, cS * S_plot]).T
    lms_mw_plot = chrom_coords_µ(LMS_plot_N)

    if not parameters['info']:
        return {
            "result": lms_mw_spec,
            "plot": lms_mw_plot
        }

    else:
        lms_mw_E_plot = chrom_coords_E(LMS_spec_N)
        lms_mw_tg_purple_plot = tangent_points_purple_line(lms_mw_plot)
        lms_mw_tg_purple = lms_mw_tg_purple_plot.copy()
        lms_mw_tg_purple[:, 0] = my_round(lms_mw_tg_purple[:, 0], 1)
        lms_mw_tg_purple[:, 1:] = my_round(lms_mw_tg_purple[:, 1:], 6)
        dict = {
            "norm": np.array([kL, kM, kS]),
            "white": my_round(lms_mw_E_plot, 6),
            # "white_plot": lms_mw_E_plot,
            "tg_purple": lms_mw_tg_purple,
            # "tg_purple_plot": lms_mw_tg_purple_plot
        }
        return dict

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
    # parameter adjustment for LMS-base
    parameters['base'] = True
    parameters['log'] = False
    # specific results are dependent on other plot/result values

    LMS_results = compute_LMS_Modular(parameters)
    LMS_spec = LMS_results['result']
    LMS_plot = LMS_results['plot']

    LMS_all = LMS_energy(parameters['field_size'], parameters['age'], base=True)[0]
    (Vλ_std_all, LM_weights) = Vλ_energy_and_LM_weights(parameters['field_size'], parameters['age'])
    (λ_all, L_base_all, M_base_all, S_base_all) = LMS_all.T
    (λ_all, V_std_all) = Vλ_std_all.T
    L_spline = scipy.interpolate.InterpolatedUnivariateSpline(λ_all, L_base_all)
    M_spline = scipy.interpolate.InterpolatedUnivariateSpline(λ_all, M_base_all)
    S_spline = scipy.interpolate.InterpolatedUnivariateSpline(λ_all, S_base_all)
    V_spline = scipy.interpolate.InterpolatedUnivariateSpline(λ_all, V_std_all)

    xyz_reference = xyz_interpolated_reference_system(
            parameters['field_size'], VisualData.XYZ31.copy(), VisualData.XYZ64.copy())

    # parameters above
    xyz_ref = xyz_reference
    (a21, a22) = LM_weights
    LMS_main = LMS_all[::10]
    (λ_main, L_main, M_main, S_main) = LMS_main.T
    V_main = sign_figs(a21 * L_main + a22 * M_main, 7)
    a33 = my_round(V_main.sum() / S_main.sum(), 8)
    # Compute optimised non-renormalised transformation matrix
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
                xtol=10**(-(10)), disp=False)  # exp: -(mat_dp + 2) = -10
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
     Z_exact_spec) = linear_transformation_λ(trans_mat, LMS_spec).T
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
    if not parameters['norm']:
        if parameters['info']:
            return {
                "trans_mat": trans_mat
            }
        else:
            XYZ_spec = linear_transformation_λ(trans_mat, LMS_spec)
            XYZ_spec[:, 1:] = sign_figs(XYZ_spec[:, 1:], 7)
            XYZ_plot = linear_transformation_λ(trans_mat, LMS_plot)
            XYZ_plot[:, 1:] = sign_figs(XYZ_plot[:, 1:], 7)
            return {
                "result": XYZ_spec,
                "plot": XYZ_plot
            }

    if parameters['info']:
        return {
            "trans_mat": trans_mat_N
        }
    XYZ_spec_N = linear_transformation_λ(trans_mat_N, LMS_spec)
    XYZ_spec_N[:, 1:] = sign_figs(XYZ_spec_N[:, 1:], 7)
    XYZ_plot_N = linear_transformation_λ(trans_mat_N, LMS_plot)
    XYZ_plot_N[:, 1:] = sign_figs(XYZ_plot_N[:, 1:], 7)
    return {
        "result": XYZ_spec_N,
        "plot": XYZ_plot_N
    }

def compute_XY_modular(parameters):
    """
    A modularized version of 'compute_xy_diagram(...)' from compute.py.

    Parameters
    ----------
    parameters: A dictionary of the processed information from URL parameters.

    Returns
    -------
    Either:
        A ndarray of CIE cone-fundamental-based xyz chromaticity coordinates given the parameters, if and only
        if the 'purples' parameter is set to False.
        Otherwise, it'll output three ndarrays representing xyz, xyz_E and xyz_tg_purple.

    """

    temp = parameters.copy()
    temp['info'] = False
    # requires XYZ for calculations, uses function above alongside the same parameters

    XYZ = compute_XYZ_Modular(temp)
    XYZ_spec = XYZ['result']
    XYZ_plot = XYZ['plot']

    def resplot():
        xyz_spec = chrom_coords_µ(XYZ_spec)
        xyz_spec[:, 1:] = my_round(xyz_spec[:, 1:], 5)
        # returns xyz_spec, xyz_plot, xyz_spec_N, xyz_plot_N
        return {
            "result": xyz_spec,
            "plot": chrom_coords_µ(XYZ_plot)
        }

    def info():
        xyz_E_plot = chrom_coords_E(XYZ_spec)
        xyz_E = my_round(xyz_E_plot, 5)

        (xyz_tg_purple_plot,
         XYZ_tg_purple_plot) = tangent_points_purple_line(
            chrom_coords_µ(XYZ_plot), False, XYZ_plot)
        xyz_tg_purple = xyz_tg_purple_plot.copy()
        xyz_tg_purple[:, 0] = my_round(xyz_tg_purple[:, 0], 1)
        xyz_tg_purple[:, 1:] = my_round(xyz_tg_purple[:, 1:], 5)
        XYZ_tg_purple = XYZ_tg_purple_plot.copy()  # tg XYZ-space
        XYZ_tg_purple[:, 0] = my_round(XYZ_tg_purple[:, 0], 1)  # tg XYZ-space
        XYZ_tg_purple[:, 1:] = my_round(XYZ_tg_purple[:, 1:], 7)  # tg XYZ-space

        output = {
            "xyz_white": xyz_E,
            "xyz_tg_purple": xyz_tg_purple,
            "XYZ_tg_purple": XYZ_tg_purple,
        }
        if parameters['purple']:
            output.update({
                "xyz_white_plot": xyz_E_plot,
                "xyz_tg_purple_plot": xyz_tg_purple_plot,
                "XYZ_tg_purple_plot": XYZ_tg_purple_plot
            })
        return output

    if parameters['purple']:
        asd = {**info(), **resplot()}
        return asd

    if parameters['info']:
        return info()
    return resplot()


def compute_XYZ_purples_modular(parameters):
    """
    compute_XYZ_purples_modular is a modularized version of the compute_XYZ_purples(...) function from compute.py,
    made to fit the parameters dictionary system. There isn't much modularization here though, as XYZ_purples(...)
    requires three versions of compute_XY_modular(...) to work properly.

    Parameters
    ----------
    parameters: A dictionary containing the treated URL parameters.

    Returns
    -------
    A ndarray of the XYZ cone-fundamental-based tristimulus function of purple-line stimuli, given parameters.
    """

    if parameters['info']:
        return compute_XYZ_Modular(parameters)
    else:
        temp = parameters.copy()
        temp['purple'] = True
        xy_dict = compute_XY_modular(temp)
        # compute.py, line 1284
        return {
            "result": XYZ_purples(xy_dict["result"], xy_dict["xyz_white"], xy_dict["XYZ_tg_purple"]),
            "plot": XYZ_purples(xy_dict["plot"], xy_dict["xyz_white_plot"], xy_dict["XYZ_tg_purple_plot"]),
        }

def compute_xyz_purples_modular(parameters):
    """
    compute_xyz_purples_modular(...) is a modularized version of compute_xyz_purples(...) from compute.py, made to
    fit the parameters dictionary system.

    Parameters
    ----------
    parameters: A dictionary containing the treated URL parameters.

    Returns
    -------
    A ndarray of xyz cone-fundamental-based tristimulus values of purple-line stimuli, given parameters.
    """
    XYZ = compute_XYZ_purples_modular(parameters)
    if parameters['info']:
        return XYZ
    else:
        result = chrom_coords_µ(XYZ['result'])
        result[:, 1:] = my_round(result[:, 1:], 5)
        return {
            "result": result,
            "plot": chrom_coords_µ(XYZ['plot'])
        }

    temp = parameters.copy()
    temp['xyz-purple'] = True
    # compute.py, line 1354
    xyz = chrom_coords_µ(compute_XYZ_purples_modular(temp))
    if parameters['mode'] == "result":
        # trying to combat floating point errors
        xyz[:, 0] = my_round(xyz[:, 0], 1)
        # compute.py, line 1355
        xyz[:, 1:] = my_round(xyz[:, 1:], 5)
    return chop(xyz)

def compute_XYZ_standard_modular(parameters):
    """
    compute_XYZ_standard_modular(...) is a modularized version of compute_CIE_standard_XYZ(...) from compute.py,
    made to fit the parameters dictionary system. Possible to modularize and optimize further, but it is
    minimal to change.

    Parameters
    ----------
    parameters: A dictionary containing treated URL parameters.

    Returns
    -------
    A ndarray of CIE XYZ colour-matching functions given field-size.
    """
    # compute.py, line 1826
    (XYZ31_std_main,
     XYZ31_plot,
     XYZ64_std_main,
     XYZ64_plot) = compute_CIE_standard_XYZ(
        VisualData.XYZ31.copy(), VisualData.XYZ64.copy())
    # parameter treatment
    if parameters['field_size'] == 2:
        return {
            "result": XYZ31_std_main,
            "plot": XYZ31_plot
        }
    else:
        return {
            "result": XYZ64_std_main,
            "plot": XYZ64_plot
        }

def compute_xyz_standard_modular(parameters):
    """
    compute_xyz_standard_modular(...) is the modularized version of compute_CIE_std_xy_diagram(...) from compute.py,
    fit to take in the parameter system we have in place.

    Parameters
    ----------
    parameters: A dictionary of URL parameters.

    Returns
    -------
    A ndarray of computated CIE chromaticity coordinates for spectral stimuli, etc.
    """

    relevant = compute_XYZ_standard_modular(parameters)

    if parameters['info']:
        white = np.array([0.33330, 0.33333, 0.33337])
        purple_plot = tangent_points_purple_line(chrom_coords_µ(relevant['plot']))
        purple = purple_plot.copy()
        purple[:, 1:] = my_round(purple_plot[:, 1:], 5)
        if parameters['field_size'] == 2:
            white = np.array([0.33331, 0.33329, 0.33340])
        return {
            "white": white,
            "tg_purple": purple
        }
    result = chrom_coords_µ(relevant['result'])
    result[:, 1:] = my_round(result[:, 1:], 5)
    return {
        "result": result,
        "plot": chrom_coords_µ(relevant['plot'])
    }