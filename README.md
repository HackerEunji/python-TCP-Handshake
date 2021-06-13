# python-TCP-Handshake
Generate Certificate
-------------------
<pre><code>openssl req -new -x509 -days 365 -nodes -out mycert.pem -keyout mycert.pem
</code></pre>

![1](https://user-images.githubusercontent.com/37477693/121798088-3b131d80-cc5f-11eb-9c09-1852ac424108.png)

Server.py
-------------------
![2](https://user-images.githubusercontent.com/37477693/121798125-76155100-cc5f-11eb-8135-28c8e4701ac5.png)
<img src="https://user-images.githubusercontent.com/37477693/121798127-7a416e80-cc5f-11eb-970b-80a8598edad0.png" width="700" height="500">

소켓을 생성하고,  bind를 하고, 연결을 하고, 서비스를 처리하는 전형적인 과정들을 담았다.

It contains typical processes for creating sockets, binding, connecting, and processing services.

Client.py
-------------------
<img src="https://user-images.githubusercontent.com/37477693/121798153-ab21a380-cc5f-11eb-9d57-a67f71271bf6.png" width="600" height="400">
반대로, 클라이언트 입장에서는 서버쪽에 연결을 요청하고 송신한 데이터를 수신받는 과정을 담당한다.

Conversely, the client is responsible for requesting connections to the server side and receiving data sent.

두가지 모두  Openssl 1.1.1k 버전과 파이썬 3.9.1 version을 이용해주었다.

Both clients and servers used Openssl 1.1.1k version and Python 3.9.1 version.

![5](https://user-images.githubusercontent.com/37477693/121798156-ae1c9400-cc5f-11eb-9d2b-f53fc100f494.png)

자꾸 TLSv1.2로 통신한다...

Still communicating with TLSv1.2...

---------------------------------------
Wireshark reports TLS 1.3 in the protocol column due to Server Hello containing a Supported Versions extension with TLS 1.3.
Recall that TLS sessions begin with a handshake to negotiate parameters such as the protocol version and ciphers. The client sends a Client Hello handshake message in a TLS record containing:

* TLS Record - Version: minimum supported TLS version (in TLS 1.2 and before). In TLS 1.3, this field is not really used and MUST be 0x0303 ("TLS 1.2") or 0x301 ("TLS 1.0") for compatibility purposes. Reference: RFC 8446 (page 79)

* Client Hello - Version: maximum supported TLS version (in TLS 1.2 and before). In TLS 1.3, this field is not used but MUST be set to 0x0303 ("TLS 1.2"). Reference: RFC 8446 (4.1.2. Client Hello)

* Client Hello - Supported Versions Extension: list of supported versions. This is the only value used by TLS 1.3 implementations (which may agree TLS 1.3, 1.2 or other versions). Reference: RFC 8446 (4.2.1. Supported Versions)

The server sends a Server Hello handshake message with:

* Server Hello - Version: negotiated version (for TLS 1.2 and before). If TLS 1.3 is negotiated, it MUST be set to 0x0303 ("TLS 1.2").

* Server Hello - Supported Versions: a single negotiated version (for TLS 1.3). Cannot be used to negotiate earlier versions.

So in TLS 1.2, the client sends a range of supported versions while a TLS 1.3 client sends a list of supported versions. The server will then pick a single version, but for compatibility purposes it will use a new field for selecting TLS 1.3 or newer.

[참조](https://networkengineering.stackexchange.com/questions/55752/why-does-wireshark-show-version-tls-1-2-here-instead-of-tls-1-3)와 같은 이유들 때문이다.

For the above reasons.


---------------------------------------
그래서 내가 구현한 것들에 대해, 어느정도 확신을 갖게 되었다.

So I've come to have some confidence in what I've embodied.

<img src="https://user-images.githubusercontent.com/37477693/121798622-5d5a6a80-cc62-11eb-94b8-dadc29e2b0ce.png" width="1200" height="300">
정상적으로 Client Hello, Server Hello등을 주고 받는 것을 볼 수 있다.

Normally, you can see Client Hello, Server Hello, etc. being exchanged.

## Client Hello
<img src="https://user-images.githubusercontent.com/37477693/121798625-63504b80-cc62-11eb-806b-7d51012abbad.png" width="500" height="50">
<img src="https://user-images.githubusercontent.com/37477693/121798627-65b2a580-cc62-11eb-88f6-f18dc6d653a8.png" width="700" height="500">

실제로 앞서 말한 TLS1.2의 0x0303으로 강제되는 것 또한 확인하였다.

In fact, we also confirmed that TLS1.2 was forced to 0x0303.

<img src="https://user-images.githubusercontent.com/37477693/121798629-6814ff80-cc62-11eb-8be0-2dbb9a2cc83c.png" width="700" height="500">

자신이 사용할 수 있는 프로토콜과 cipher suite들을 나열하게 된다.

It lists the protocols and cipher suites that it can use.

## Server Hello
<img src="https://user-images.githubusercontent.com/37477693/121798631-6a775980-cc62-11eb-88ac-7b39836b4993.png" width="500" height="50">
<img src="https://user-images.githubusercontent.com/37477693/121798633-6c411d00-cc62-11eb-9252-2ab2ade8beb3.png" width="700" height="500">

Server Hello에서는 앞선 client hello 메시지로부터 protocol을 선택하고 ciphersuite도 선택한다.

Server Hello selects protocols and ciphersuite from the previous client hello message.

여기에선 TLS_ECDHE_WITH_AES_128_GCM_SHA256을 cipher suite로 고른것을 알 수 있다.

Here, TLS_ECDHE_With_AES_128_GCM_SHA256 is selected as the ciphersuit.

<img src="https://user-images.githubusercontent.com/37477693/121798636-6ea37700-cc62-11eb-8bed-40b66c8889a1.png" width="700" height="220">

[사진 출처](https://rsec.kr/?p=455)

이를 통해, TLS 프로토콜과 키교환 방식은 ECDHE를 사용했으며, AES_128이라는 대칭키 이용 블록 암호화 방식, 블록 암호 운용방식, HMAC을 포함하는 것을 알 수 있다.

Through this, we can see that the TLS protocol and key exchange method used ECDHE and included a symmetric key-using block encryption method called AES_128, block cipher operation method, and HMAC.


여기에서 서버에서 생성된 임의의 난수, 서버의 SSL 버전, 클라이언트에게서 받은 Cipher Suit 리스트 중선택한 Cipher Suite, 세션 식별자 등을 보내게 되는 것을 확인할 수 있다.

Here you can see that random numbers generated by the server, SSL versions of the server, Cipher Suite selected from the list of Cipher Suit received from the client, and session identifiers are sent.

## Change Cipher Suite Spec
<img src="https://user-images.githubusercontent.com/37477693/121798637-7105d100-cc62-11eb-951e-052c95520f22.png" width="500" height="50">
handshake에서 데이터 암호화용 대칭키 생성이 완료되고, 데이터를 암호화하라는 내용을 보내게 된다.

Handshake completes the creation of a symmetric key for data encryption and sends a message to encrypt the data.

Change Cipher Spec 메시지로 지금까지 협의된 내용 (서명 방식, 압축 방식, 암호화 방식, 키 교환 방식)을 적용할 것을 알리고, 그 다음부터 암호화된 데이터인 Application Data 를 전송하는 것을 알 수 있다.

The Change Cipher Spec message informs the application of the negotiated content (signature method, compression method, encryption method, key exchange method) and then sends the encrypted data, "Application Data".

<img src="https://user-images.githubusercontent.com/37477693/121798639-72cf9480-cc62-11eb-94e5-c9c4c71f9cdf.png" width="700" height="500">
<img src="https://user-images.githubusercontent.com/37477693/121798640-7531ee80-cc62-11eb-9c49-f7aa70f642d1.png" width="700" height="500">

실제로 바로 다음의 Application Data에서 Encrypted된 Application Data가 포함되는 것을 알 수 있다.

In fact, the very following Application Data contains Encrypted Application Data.

이 과정이후부터 서버도 알고리즘 목록 전달이 끝나고 핸드쉐이크 과정이 종료되는 것을 알 수 있다. 이 뒤로는 암호화 통신이 이루어진다.

After this process, the server can also see that the list of algorithms is delivered and the handshake process is terminated. This is followed by cryptographic communication.

<img src="https://user-images.githubusercontent.com/37477693/121798642-77944880-cc62-11eb-8cf3-8637ebbecb4d.png" width="700" height="400">
<img src="https://user-images.githubusercontent.com/37477693/121798643-79f6a280-cc62-11eb-8375-7751b5883b5c.png" width="700" height="300">

상당히 많은 Application Data들이 왔다갔다 한다.

Quite a lot of Application Data comes and goes.

## 출력 내용
<img src="https://user-images.githubusercontent.com/37477693/121798645-7bc06600-cc62-11eb-94f5-680f32ddccb0.png" width="400" height="200">

내가 코드에 작성해준 내용대로 HTTP/1.1을 포함한다.

It includes HTTP/1.1 as I wrote in the code.

<img src="https://user-images.githubusercontent.com/37477693/121798649-7ebb5680-cc62-11eb-86e1-8b921a033174.png" width="700" height="80">

## FINISH
<img src="https://user-images.githubusercontent.com/37477693/121798655-82e77400-cc62-11eb-8dc5-ad909adeb8a8.png" width="500" height="50">
<img src="https://user-images.githubusercontent.com/37477693/121798657-85e26480-cc62-11eb-9ccc-a30909121b8a.png" width="700" height="500">

결과적으로 FIN되는 것을 알 수 있다.

As a result, it can be seen that FIN.

<img src="https://user-images.githubusercontent.com/37477693/121798661-88dd5500-cc62-11eb-843f-6516a397ac5b.png" width="700" height="350">

너무 정확하게 그 과정들이 보여 너무 신기했다.

(글씨가 겹쳐보이는 것은 내가 글씨 크기 조절을 했기 때문)

It was so amazing to see the processes so accurately.

(The reason why the letters overlap is because I resized them.)

