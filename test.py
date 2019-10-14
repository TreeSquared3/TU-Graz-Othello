import pexpect

child = pexpect.spawn("python3.7 orthello_tugraz_ws2019_11914789.py")

child.expect("*y against a [human] or an [ai*")
child.sendline("human")

child.expect("player1> ")
child.sendline("e2")