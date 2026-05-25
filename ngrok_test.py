from pyngrok import ngrok

public_url = ngrok.connect(8001)

print("Public URL:")
print(public_url)