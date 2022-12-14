from cvss import CVSS2, CVSS3

def get_riskcolor(severity):
    _map = {
            'critical':'#c00000',
            'high':'#ff0000',
            'medium':'#ffc000',
            'low':'#92d050',
            'info':'#00b0f0'
    }
    return _map[severity.casefold()]

def get_severity(score):
    if score >= 9.0:
        return 'Critical'
    elif score >= 7.0:
        return 'High'
    elif score >= 4.0:
        return 'Medium'
    elif score >= 0.1:
        return 'Low'
    else:
        return 'Info'

def get_ssvc(cvss):

    if cvss is None:
        # info
        severity = 'Info'
        score = 0.0
        vector = '-'
    else:
        if not cvss.startswith('CVSS:3.1/'):
            cvss = 'CVSS:3.1/'+cvss
        _cvss_o = CVSS3(cvss)

        #severity = _cvss_o.severities()[0]
        score = min(_cvss_o.scores())
        severity = get_severity(score)
        vector = _cvss_o.clean_vector()

    if score < 0.1:
        score_print = '-'
    else:
        score_print = str(score)

    color = get_riskcolor(severity)

    return severity, score, score_print, vector, color
