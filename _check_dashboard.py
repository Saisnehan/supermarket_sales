from html.parser import HTMLParser

class V(HTMLParser):
    def __init__(self):
        super().__init__()
        self.errors = []
        self.stack  = []
        self.void   = {
            'area','base','br','col','embed','hr','img',
            'input','link','meta','param','source','track','wbr'
        }
    def handle_starttag(self, t, a):
        if t not in self.void:
            self.stack.append(t)
    def handle_endtag(self, t):
        if t in self.void: return
        if self.stack and self.stack[-1] == t:
            self.stack.pop()
        else:
            self.errors.append(f'Mismatched </{t}>')

with open('dashboard.html', encoding='utf-8') as f:
    src = f.read()

v = V()
v.feed(src)

checks = {
    'Chart.js CDN':          'chart.js' in src,
    'data-theme attr':       'data-theme' in src,
    'Monthly chart':         'cMonthly' in src,
    'Category chart':        'cCategory' in src,
    'Scatter chart':         'cScatter' in src,
    'Viz studio':            'cViz' in src,
    'CSV export fn':         'exportCSV' in src,
    'Image export fn':       'exportImg' in src,
    'Theme toggle fn':       'toggleTheme' in src,
    'Sidebar toggle fn':     'toggleSidebar' in src,
    'IBM Plex font':         'IBM Plex' in src,
    'IBM colour tokens':     '--ibm-blue-60' in src,
    'Heatmap section':       'heatmap' in src.lower(),
    'KPI cards':             'kpi' in src.lower(),
    'Dark mode support':     'isDark' in src,
    'Filter bar':            'fbar' in src,
    'Responsive viewport':   'viewport' in src,
}

failed = [k for k,v2 in checks.items() if not v2]
if failed:
    print('FAILED checks:', failed)
else:
    print(f'File size : {len(src):,} bytes')
    print(f'Lines     : {src.count(chr(10)):,}')
    print(f'Parse errs: {len(v.errors)} -- {v.errors[:3] if v.errors else "none"}')
    print(f'Unclosed  : {v.stack[:5] if v.stack else "none"}')
    print('All checks PASSED')
