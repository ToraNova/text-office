#!bin/python

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

_cvss_v = args.cvss
if _cvss_v is None:
    # info
    severity = 'Info'
    score = '-'
    vector = '-'
else:
    if not _cvss_v.startswith('CVSS:3.1/'):
        _cvss_v = 'CVSS:3.1/'+_cvss_v
    _cvss_o = CVSS3(_cvss_v)

    severity = _cvss_o.severities()[0]
    score = _cvss_o.scores()[0]
    vector = _cvss_o.clean_vector()

color = get_riskcolor(severity)

finding_name = args.name
clean_name = args.name.casefold().translate(dict.fromkeys(map(ord, u' #/()[]{}')))
mdfile_name = f'{clean_name}.md'

print('creating boilerplate markdown with:',severity, score, vector, color)
with open(mdfile_name, 'a+') as out:
    out.write(f'''### {finding_name}

<table style=Table Grid, colwidths=1.11in;1.11in;4in>
<para before=6pt, spacing=1.15, after=6pt, align=center>
|<cell color=#000000>Risk Rating</cell>|<cell color=#000000>Overall Score</cell>|<cell color=#000000>CVSS Vector</cell>|
|---|---|---|
|<cell color={color}>{severity}</cell>|{score}|{vector}|
</para>
</table>

**Affected Module**

-

**Observations**

**Screenshots**

**Implications**

**Recommendations**

**Reference**

**Status**
''')
