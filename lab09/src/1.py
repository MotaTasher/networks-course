import subprocess

res = subprocess.check_output('ifconfig').decode()

def FindTarget(string, pos_start, target):
    diff = string[pos_start:].find(target)
    pos_start += diff
    if diff == -1:
        return pos_start
    pos_start += len(target)
    pos_end = (string[pos_start:]).find(' ') + pos_start
    print(f"{target[:-1]}: {string[pos_start:pos_end]}")
    return pos_start

pos_start = 0
while True:
    diff = FindTarget(res, pos_start, 'inet ') - pos_start
    if diff == -1:
        break
    pos_start += diff
    diff = FindTarget(res, pos_start, 'netmask ') - pos_start
    if diff == -1:
        break
    pos_start += diff