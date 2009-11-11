import sys

input = sys.stdin.read()

input = input + 'poop'

sys.stdout.write('Message to stdout\n' + input)
sys.stderr.write('Message to stderr\n' + input)


