import argparse
import requests
from jproperties import Properties


def file_content(url):
    resp = requests.get(url, timeout=10)
    return resp.ok, resp.text


def main(arguments):
    changed_files = arguments.add.split(',') + arguments.mod.split(',')
    cores = []
    plugins = []
    for file in changed_files:
        if file.startswith('core') or file.startswith('cli'):
            core = {
                'url': 'https://raw.githubusercontent.com/jenkinsci/jenkins/master/',
                "origin": file.replace('_zh_CN', ''),
                "current": file
            }
            cores.append(core)
        elif file.startswith('plugins'):
            plugin = {
                "url": 'https://raw.githubusercontent.com/jenkinsci/' + file.split('/')[1] + '/master/',
                "plugin": file.split('/')[1],
                "origin": file.replace('_zh_CN', '').replace('plugins/' + file.split('/')[1], ''),
                "current": file
            }
            plugins.append(plugin)

    results = []
    for core in cores:
        exists, con = file_content(core['url'] + core['origin'])
        if not exists:
            result = {
                'file_name': core['current'],
                'original_content': '',
                'translate_content': '',
                'exist': False
            }
        else:
            p = Properties()
            p.load(con, encoding='utf-8')

            ps = Properties()
            with open(core['current'], "rb") as f:
                ps.load(f, "utf-8")

            result = {
                'file_name': core['current'],
                'original_content': p,
                'translate_content': ps,
                'exist': True
            }
        results.append(result)

    for plugin in plugins:
        exists, con = file_content(plugin['url'] + plugin['origin'])
        if not exists:
            result = {
                'file_name': core['current'],
                'original_content': '',
                'translate_content': '',
                'exist': False
            }
        else:
            p = Properties()
            p.load(con, encoding='utf-8')
            ps = Properties()
            with open(plugin['current'], "rb") as f:
                ps.load(f, "utf-8")
            result = {
                'file_name': core['current'],
                'original_content': p,
                'translate_content': ps,
                'exist': True
            }
        results.append(result)

    string = []
    for result in results:
        if result['exist']:
            string.append('#### ' + result['file_name'])
            string.append("Original")
            string.append("'''")
            for k1, v1 in result['original_content'].items():
                string.append(k1 + '=' + v1.data)
            string.append("'''")
            string.append("Current")
            string.append("'''")
            for k2, v2 in result['translate_content'].items():
                string.append(k2 + '=' + v2.data)
            string.append("'''\n")

    markdown = "\n".join(str)
    print(markdown)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='xxxx')
    parser.add_argument('--add', help='an integer for the accumulator')
    parser.add_argument('--mod', help='sum the integers (default: find the max)')
    args = parser.parse_args()
    main(args)
