"""
    A module specifically designed to be between the description.py module from CIE Functions,
    and the API within cieapi_test.py.
"""

import sys

import cieapi
import styles.description
from computemodularization import compute_MacLeod_Modular, compute_Maxwellian_Modular, compute_XYZ_Modular, \
    compute_XY_modular, compute_XYZ_purples_modular, compute_xyz_standard_modular

# ------------------------------------------------------------------------------------------

"""
    A version of _head() that doesn't use package_path with pathlib library.
    Using this function directly doesn't link up right with the API, so it changes
    the usage of them by instead using a statically hosted file for the CSS, and an official
    and secure link for the mathjax.
"""
def _head():
    html_string = """
    <head>
    <link type="text/css" rel="stylesheet" href="../../../styles/description.css" />
    <script type="text/javascript"
    src="http://cdn.mathjax.org/mathjax/latest/MathJax.js?config=TeX-AMS-MML_HTMLorMML">
    </script>
    <script type="text/x-mathjax-config">
        MathJax.Hub.Config({
            displayAlign: "left",
            showProcessingMessages: false,
            messageStyle: "none",
            inlineMath:[["\\(","\\)"]],
            displayMath:[["$$","$$"]],
            tex2jax: { preview: "none" },
            "HTML-CSS": {
    """
    if sys.platform.startswith('win'):
        html_string += """
                scale: 95
        """
    elif sys.platform.startswith('linux'):
        html_string += """
                scale: 95
        """
    else:
        html_string += """
                scale: 100
        """
    html_string += """
            }
        });
    </script>
    </head> 
    """
    return html_string

"""
    The following functions are identical to their counterparts in description.py,
    just without the "_sidemenu" suffix. These have been adjusted to use the 'parameters' dictionary system
    that the entire program is revolved around, but remain mostly - if not almost near identical to their
    original counterparts.
"""

def LMS_sidemenu(parameters):
    html_string = ""
    html_string += _head()

    # copy of parameters to allow for changes without modifying original
    params = parameters.copy()
    # changing their names to be equal to 'data' and 'options' keys, so that it
    # can use as much of the original material as possible
    params['λ_min'] = params['min']
    params['λ_max'] = params['max']
    params['λ_step'] = params['step_size']
    params['log10'] = params['log']

    if parameters['base']:
        html_string += styles.description._heading('CIE LMS cone fundamentals (9 sign. figs.)')
    else:
        html_string += styles.description._heading('CIE LMS cone fundamentals')
    html_string += (
        styles.description._parameters(params) +
        styles.description._functions('\\(\\bar l_{%s,\,%d}\\)' %
                   (params['field_size'], params['age']),
                   '\\(\\bar m_{\,%s,\,%d}\\)' %
                   (params['field_size'], params['age']),
                   '\\(\\bar s_{%s,\,%d}\\)' %
                   (params['field_size'], params['age']),
                   '\\(\\lambda\\) &nbsp;(wavelength)') +
       styles.description._wavelenghts(params) +
       styles.description._normalization_LMS(params) +
       styles.description._precision_LMS(params, params['base'])
    )
    return html_string

def LMS_MB_sidemenu(parameters):
    html_string = ""
    html_string += _head()

    # copy of parameters to allow for changes without modifying original
    data = parameters.copy()
    # changing their names to be equal to 'data' and 'options' keys, so that it
    # can use as much of the original material as possible
    data['λ_min'] = data['min']
    data['λ_max'] = data['max']
    data['λ_step'] = data['step_size']

    # needs info from macleod, does computation
    data['info'] = True
    info = compute_MacLeod_Modular(data)
    data['norm_coeffs_lms_mb'] = info['norm']
    data['lms_mb_white'] = info['white']
    data['lms_mb_tg_purple'] = info['tg_purple']


    html_string += styles.description._heading(u'MacLeod\u2013Boynton ls chromaticity diagram')
    html_string += (
        styles.description._parameters(data) +
        styles.description._coordinates('\\(l_{\,\mathrm{MB},\,%s,\,%d}\\)' %
                                 (data['field_size'], data['age']),
                                 '\\(m_{\,\mathrm{MB},\,%s,\,%d}\\)' %
                                 (data['field_size'], data['age']),
                                 '\\(s_{\,\mathrm{MB},\,%s,\,%d}\\)' %
                                 (data['field_size'], data['age'])) +
        styles.description._wavelenghts(data) +
        styles.description._normalization_lms_mb(data) +
        styles.description._LMS_to_lms_mb(data, data) +
        styles.description._precision_lms_mb() +
        styles.description._illuminant_E_lms_mb(data) +
        styles.description._purpleline_tangentpoints_lms_mb(data) )

    return html_string

def LMS_MW_sidemenu(parameters):
    html_string = ""
    html_string += _head()

    # copy of parameters to allow for changes without modifying original
    data = parameters.copy()
    # changing their names to be equal to 'data' and 'options' keys, so that it
    # can use as much of the original material as possible
    data['λ_min'] = data['min']
    data['λ_max'] = data['max']
    data['λ_step'] = data['step_size']

    # needs info from maxwell, does computation
    data['info'] = True
    info = compute_Maxwellian_Modular(data)
    data['norm_coeffs_lms_mw'] = info['norm']
    data['lms_mw_white'] = info['white']
    data['lms_mw_tg_purple'] = info['tg_purple']

    html_string += (styles.description._heading('Maxwellian lm chromaticity diagram') +
                    styles.description._parameters(data) +
                    styles.description._coordinates('\\(l_{\,%s,\,%d}\\)' %
                                 (data['field_size'], data['age']),
                                 '\\(m_{\,%s,\,%d}\\)' %
                                 (data['field_size'], data['age']),
                                 '\\(s_{\,%s,\,%d}\\)' %
                                 (data['field_size'], data['age'])) +
                    styles.description._wavelenghts(data) +
                    styles.description._normalization_lms_mw(data) +
                    styles.description._LMS_to_lms_mw(data) +
                    styles.description._precision_lms_mw() +
                    styles.description._illuminant_E_lms_mw(data) +
                    styles.description._purpleline_tangentpoints_lms_mw(data))

    return html_string


def XYZ_sidemenu(parameters):
    html_string = ""
    html_string += _head()

    # copy of parameters to allow for changes without modifying original
    data = parameters.copy()
    # changing their names to be equal to 'data' and 'options' keys, so that it
    # can use as much of the original material as possible
    data['λ_min'] = data['min']
    data['λ_max'] = data['max']
    data['λ_step'] = data['step_size']

    data['info'] = True
    info = compute_XYZ_Modular(data)
    # compute_XYZ_Modular makes the trans_mat itself either normal or not normalized, depending on
    # the value of parameters['norm']; if it is activated, 'trans_mat' is normalized, so it makes sure
    # that either way, it gets the right one
    data['trans_mat'] = info['trans_mat']
    data['trans_mat_N'] = info['trans_mat']


    html_string += (styles.description._heading('CIE XYZ cone-fundamental-based tristimulus functions') +
                    styles.description._parameters(data) +
                    styles.description._functions('\\(\\bar x_{\,\mathrm{F},\,%s,\,%d}\\)' %
                               (data['field_size'], data['age']),
                               '\\(\\bar y_{\,\mathrm{F},\,%s,\,%d}\\)' %
                               (data['field_size'], data['age']),
                               '\\(\\bar z_{\,\mathrm{F},\,%s,\,%d}\\)' %
                               (data['field_size'], data['age']),
                               '\\(\\lambda\\) &nbsp;(wavelength)') +
                    styles.description._wavelenghts(data) +
                    styles.description._normalization_XYZ(data, data) +
                    styles.description._LMS_to_XYZ(data, data) +
                    styles.description._precision_XYZ()
                    )
    return html_string

def XY_sidemenu(parameters):
    html_string = ""
    html_string += _head()

    # copy of parameters to allow for changes without modifying original
    data = parameters.copy()
    # changing their names to be equal to 'data' and 'options' keys, so that it
    # can use as much of the original material as possible
    data['λ_min'] = data['min']
    data['λ_max'] = data['max']
    data['λ_step'] = data['step_size']

    data['info'] = True
    info = compute_XY_modular(data)
    # same as XYZ, the 'xyz_white' in info is equal to both normalized and unnormalized value of xyz_white,
    # depending on the true/false of parameters['norm'] (copied to data, so data['norm']
    data['xyz_white'] = info['xyz_white']
    data['xyz_white_N'] = info['xyz_white']
    data['xyz_tg_purple'] = info['xyz_tg_purple']
    data['xyz_tg_purple_N'] = info['xyz_tg_purple']

    html_string += (
        styles.description._heading("CIE xy cone-fundamental-based chromaticity diagram") +
        styles.description._parameters(data) +
        styles.description._coordinates('\\(x_{\,\mathrm{F},\,%s,\,%d}\\)' %
                                 (data['field_size'], data['age']),
                                 '\\(y_{\,\mathrm{F},\,%s,\,%d}\\)' %
                                 (data['field_size'], data['age']),
                                 '\\(z_{\,\mathrm{F},\,%s,\,%d}\\)' %
                                 (data['field_size'], data['age'])) +
        styles.description._wavelenghts(data) +
        styles.description._normalization_xyz(data, data) +
        styles.description._XYZ_to_xyz(data) +
        styles.description._precision_xyz() +
        styles.description._illuminant_E_xyz(data, data) +
        styles.description._purpleline_tangentpoints_xyz(data, data)
    )
    return html_string

def XYZP_sidemenu(parameters):
    html_string = ""
    html_string += _head()

    # copy of parameters to allow for changes without modifying original
    data = parameters.copy()
    # changing their names to be equal to 'data' and 'options' keys, so that it
    # can use as much of the original material as possible
    data['λ_min'] = data['min']
    data['λ_max'] = data['max']
    data['λ_step'] = data['step_size']

    data['info'] = True
    info = compute_XYZ_Modular(data)
    # compute_XYZ_Modular makes the trans_mat itself either normal or not normalized, depending on
    # the value of parameters['norm']; if it is activated, 'trans_mat' is normalized, so it makes sure
    # that either way, it gets the right one
    data['trans_mat'] = info['trans_mat']
    data['trans_mat_N'] = info['trans_mat']

    # also needs result from computation of itself to get these values
    data['info'] = False
    purples = compute_XYZ_purples_modular(data)['result']
    data['λ_purple_min'] = '%.1f' % purples[0, 0]
    data['λ_purple_max'] = '%.1f' % purples[-1, 0]
    data['λ_purple_min_N'] = data['λ_purple_min']
    data['λ_purple_max_N'] = data['λ_purple_max']

    html_string += (
        styles.description._heading("XYZ cone-fundamental-based tristimulus functions for purple-line stimuli") +
        styles.description._parameters(data) +
        styles.description._functions(
                            '\\(\\bar x_{\,\mathrm{Fp},\,%s,\,%d}\\)' %
                            (data['field_size'], data['age']),
                            '\\(\\bar y_{\,\mathrm{Fp},\,%s,\,%d}\\)' %
                            (data['field_size'], data['age']),
                            '\\(\\bar z_{\,\mathrm{Fp},\,%s,\,%d}\\)' %
                            (data['field_size'], data['age']),
                            '<nobr>\\(\\lambda_{\\mathrm{c}}\\)</nobr> \
                            &nbsp;(complementary<font size="0.0em"> </font>\
                            &nbsp;wavelength)') +
        styles.description._wavelenghts_complementary(data, data) +
        styles.description._normalization_XYZ(data, data) +
        styles.description._LMS_to_XYZ_purples(data, data) +
        styles.description._precision_XYZ()
    )
    return html_string

def XYP_sidemenu(parameters):
    html_string = ""
    html_string += _head()

    # copy of parameters to allow for changes without modifying original
    data = parameters.copy()
    # changing their names to be equal to 'data' and 'options' keys, so that it
    # can use as much of the original material as possible
    data['λ_min'] = data['min']
    data['λ_max'] = data['max']
    data['λ_step'] = data['step_size']

    data['info'] = True
    info = compute_XY_modular(data)
    # same as XYZ, the 'xyz_white' in info is equal to both normalized and unnormalized value of xyz_white,
    # depending on the true/false of parameters['norm'] (copied to data, so data['norm']
    data['xyz_white'] = info['xyz_white']
    data['xyz_white_N'] = info['xyz_white']
    data['xyz_tg_purple'] = info['xyz_tg_purple']
    data['xyz_tg_purple_N'] = info['xyz_tg_purple']

    # also needs result from computation of itself to get these values
    data['info'] = False
    purples = compute_XYZ_purples_modular(data)['result']
    data['λ_purple_min'] = '%.1f' % purples[0, 0]
    data['λ_purple_max'] = '%.1f' % purples[-1, 0]
    data['λ_purple_min_N'] = data['λ_purple_min']
    data['λ_purple_max_N'] = data['λ_purple_max']

    html_string += (
        styles.description._heading("xy cone-fundamental-based chromaticity diagram (purple-line stimuli)") +
        styles.description._parameters(data) +
        styles.description._coordinates('\\(x_{\,\mathrm{F},\,%s,\,%d}\\)' %
                                 (data['field_size'], data['age']),
                                 '\\(y_{\,\mathrm{F},\,%s,\,%d}\\)' %
                                 (data['field_size'], data['age']),
                                 '\\(z_{\,\mathrm{F},\,%s,\,%d}\\)' %
                                 (data['field_size'], data['age'])) +
        styles.description._wavelenghts_complementary(data, data) +
        styles.description._normalization_xyz(data, data) +
        styles.description._XYZ_purples_to_xyz_purples(data) +
        styles.description._precision_xyz() +
        styles.description._illuminant_E_xyz(data, data) +
        styles.description._purpleline_tangentpoints_xyz_complementary(data, data)
    )
    return html_string

def XYZ_std_sidemenu(parameters):
    html_string = ""
    html_string += _head()

    # copy of parameters to allow for changes without modifying original
    data = parameters.copy()
    # changing their names to be equal to 'data' and 'options' keys, so that it
    # can use as much of the original material as possible

    html_string += styles.description._heading("CIE XYZ standard colour-matching functions")

    # field_size = 2
    if data['field_size'] == cieapi.STD_1931:
        html_string += (
            styles.description._parameters_std('2') +
            styles.description._functions('\\(\\bar x\\) ',
                       '\\(\\bar y\\) ',
                       '\\(\\bar z\\)',
                       '\\(\\lambda\\) &nbsp;(wavelength)') +
            styles.description._wavelenghts_std() +
            styles.description._normalization_XYZ31() +
            styles.description._precision_XYZ()
        )
    else:
        # field_size = 10
        html_string += (
            styles.description._parameters_std('10') +
            styles.description._functions('\\(\\bar x_{10}\\)',
                               '\\(\\bar y_{10}\\)',
                               '\\(\\bar z_{10}\\)',
                               '\\(\\lambda\\) &nbsp;(wavelength)') +
            styles.description._wavelenghts_std() +
            styles.description._normalization_XYZ64() +
            styles.description._precision_XYZ()
        )
    return html_string

def XY_std_sidemenu(parameters):
    html_string = ""
    html_string += _head()

    # copy of parameters to allow for changes without modifying original
    data = parameters.copy()
    # changing their names to be equal to 'data' and 'options' keys, so that it
    # can use as much of the original material as possible
    data['info'] = True
    info = compute_xyz_standard_modular(data)
    # the info 'tg_purple' is applied to both for same reason normalization is above;
    #
    data['xyz31_tg_purple'] = info['tg_purple']
    data['xyz64_tg_purple'] = info['tg_purple']

    html_string += styles.description._heading("CIE xy standard chromaticity diagram")
    if data['field_size'] == cieapi.STD_1931:
        html_string += (
                styles.description._parameters_std('2') +
                styles.description._coordinates('\\(x\\)', '\\(y\\)', '\\(z\\)') +
                styles.description._wavelenghts_std() +
                styles.description._normalization_xyz31() +
                styles.description._XYZ31_to_xyz31() +
                styles.description._precision_xyz() +
                styles.description._illuminant_E_xyz31() +
                styles.description._purpleline_tangentpoints_xyz31(data)
        )
    else:
        html_string += (
                styles.description._parameters_std('10') +
                styles.description._coordinates('\\(x_{10}\\)',
                             '\\(y_{\,10}\\)',
                             '\\(z_{\,10}\\)') +
                styles.description._wavelenghts_std() +
                styles.description._normalization_xyz64() +
                styles.description._XYZ64_to_xyz64() +
                styles.description._precision_xyz() +
                styles.description._illuminant_E_xyz64() +
                styles.description._purpleline_tangentpoints_xyz64(data)
        )
    return html_string
