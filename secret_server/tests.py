from secret_server.sdk_client import SDK_Client

client = SDK_Client()

client.configure()

print(client.token)

client.remove()
