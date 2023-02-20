'''
Copyright (C) 2023 ToraNova

    This program is free software: you can redistribute it and/or modify
    it under the terms of the GNU Affero General Public License as published
    by the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU Affero General Public License for more details.

    You should have received a copy of the GNU Affero General Public License
    along with this program.  If not, see <https://www.gnu.org/licenses/>.
'''

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
