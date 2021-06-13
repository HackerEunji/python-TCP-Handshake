import socket, ssl

'''
if ssl.HAS_TLSv1_3:
    print("{0} with support for TLS 1.3"
      .format(ssl.OPENSSL_VERSION))

if hasattr(ssl, 'PROTOCOL_TLSv1_3'):
    ciphers.insert(0, ['GREASE_3A', 'GREASE_6A', 'AES128-GCM-SHA256', 'AES256-GCM-SHA256', 'AES256-GCM-SHA384', 'CHACHA20-POLY1305-SHA256'])
'''

context = ssl.SSLContext(ssl.PROTOCOL_TLSv1) #original
#context = ssl.SSLContext(ssl.SSLv23_METHOD)

if getattr(context, "post_handshake_auth", None)is not None:
  context.post_handshake_auth = True
  
#print(ssl.HAS_TLSv1)
#print(ssl.HAS_TLSv1_1)
#print(ssl.HAS_TLSv1_2)
#print(ssl.HAS_TLSv1_3)

context.load_cert_chain(certfile="mycert.pem") 

def handle(conn):
    conn.write(b'GET / HTTP/1.1\n')
    print(conn.recv().decode())

while True:
  sock = socket.socket()
  sock.bind(('192.168.68.1', 12348))
  sock.listen(5)
  context = ssl.create_default_context(ssl.Purpose.CLIENT_AUTH)
  context.load_cert_chain(certfile="mycert.pem") 
  context.options |= ssl.OP_NO_TLSv1 | ssl.OP_NO_TLSv1_1 | ssl.OP_NO_TLSv1_2 # optional
  #context.options |= ssl.OP_NO_TLSv1
  #context.options |= ssl.OP_NO_TLSv1_1
  #context.options |= ssl.OP_NO_TLSv1_2


  context.set_ciphers('AES256+ECDH:AES256+EDH') #original
  #context.set_ciphers('TLS_AES_128_CCM_SHA256')
  #context.set_ciphers('TLS_AES_128_GCM_SHA256')

  while True:
    conn = None
    ssock, addr = sock.accept()
    try:
      conn = context.wrap_socket(ssock, server_side=True)
      handle(conn)
    except ssl.SSLError as e:
      print(e)
    finally:
      if conn:
        conn.close()