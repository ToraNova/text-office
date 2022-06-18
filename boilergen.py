#!/usr/bin/env python

import argparse
from cvss import CVSS2, CVSS3

parser = argparse.ArgumentParser()
# single
parser.add_argument('name', help='name of finding', type=str)
parser.add_argument('-c', '--cvss', help="cvss vector of finding", type=str)
args = parser.parse_args()

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

_cvss_v = args.cvss
if _cvss_v is None:
    # info
    severity = 'Info'
    score = 0.0
    vector = '-'
else:
    if not _cvss_v.startswith('CVSS:3.1/'):
        _cvss_v = 'CVSS:3.1/'+_cvss_v
    _cvss_o = CVSS3(_cvss_v)

    #severity = _cvss_o.severities()[0]
    score = min(_cvss_o.scores())
    severity = get_severity(score)
    vector = _cvss_o.clean_vector()

if score < 0.1:
    score_print = '-'
else:
    score_print = str(score)

color = get_riskcolor(severity)

finding_name = args.name
clean_name = args.name.casefold().translate(dict.fromkeys(map(ord, u' \n#/\\()[]{}<>-')))
strscore = str(score).replace('.','')
mdfile_name = f'{strscore}_{clean_name}.md'

print('creating boilerplate markdown with:',severity, score, vector, color)
with open(mdfile_name, 'a+') as out:
    out.write(f'''### {finding_name}

<table style=Table Grid, colwidths=1.11in;1.11in;4in>
<para before=6pt, spacing=1.15, after=6pt, align=center>
|<cell color=#000000>Risk Rating</cell>|<cell color=#000000>Overall Score</cell>|<cell color=#000000>CVSS Vector</cell>|
|---|---|---|
|<cell color={color}>{severity}</cell>|{score_print}|{vector}|
</para>
</table>

**Affected Module**

-

**Observations**

**Screenshots**

<align center>
<img width=12cm>![](screencaps/test-1.png "TODO: caption 1")</img>

<img width=12cm>![](screencaps/test-2.png "TODO: caption 2")</img>
</align>

**Implications**

**Recommendations**

**Reference**

**Management Comments**

**Status**

Open

<pgbr>
''')
