import subprocess

def proxy_parts(line):
    parts = {}
    main_part = line[line.index('<'):line.index('>')]
    country_ping = main_part[:main_part.index('[')].split()[1:]
    parts['country'] = country_ping[0]
    parts['ping'] = country_ping[1]
    parts['attrs'] = main_part[main_part.index('[') + 1:main_part.index(']')].split(',')
    parts['address'] = main_part[main_part.index(']') + 2:]
    return parts

def external_proxies():
    exec = 'python get_proxy.py'
    p = subprocess.Popen(exec, stdout=subprocess.PIPE, shell=True)
    out, err = p.communicate()
    result = (out.decode('utf-8')).split('\n')
    result_table = []
    for line in result:
        if line and not line.startswith('#'):
            print(line)
            proxy = proxy_parts(line)
            print(proxy)
            result_table.append(proxy)
    return result_table

if __name__ == '__main__':
    raw = external_proxies()
    print(raw)
