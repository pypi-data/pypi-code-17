from client import AuroraTCPClient, AuroraError

for x in range(1, 31):
    client = AuroraTCPClient(ip='127.0.0.1', port=3000, address=x)
    client.connect()
    try:
        print x
        print client.state(2)
    except AuroraError as e:
        print e.message
    finally:
        client.close()
