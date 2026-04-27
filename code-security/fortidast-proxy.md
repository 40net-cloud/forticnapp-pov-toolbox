## FortiCNAPP FortiDAST Proxy Server
<br>


### 📘 Reference Links

| Topic | Documentation Link |
|--------|---------------------|
| FortiDAST Proxy Serve .yml file from UI | [https://docs.fortinet.com/document/fortidast/26.1.0/user-guide/487181/fortidast-proxy) |
| FortiDAST Proxy Server                  | [https://docs.fortinet.com/document/fortidast/26.1.0/user-guide/688454/fortidast-proxy-server) |
                  


## 🚀 FortiDAST Proxy Setup (Docker)

This guide shows how to install Docker, pull the FortiDAST proxy image, and run the proxy container.

---

## 📋 Steps


FortiDAST enables scanning of internal assets in your network (non-public IP addresses) using a proxy server. For more information, see FortiDAST Proxy Server.


### 1️⃣ Install Docker or Docker Compose 

```bash
sudo apt update
```
```bash
sudo apt install docker.io -y
```
```bash
sudo apt install docker-compose -y
```

2️⃣ (Optional) Remove Existing Proxy Image

```bash
docker rmi registry.fortidast.com/fptproxyserver
```

3️⃣ Pull Latest FortiDAST Proxy Image

```bash
docker pull registry.fortidast.forticloud.com/dastproxy
```
## 📋 Now
Enable the FortiDAST Proxy server feature from UI and click Copy to copy the Docker compose file into the Proxy Server (docker-compose.yml).
Start FortiDAST Proxy Container


<img width="1181" height="597" alt="Screenshot 2026-04-28 at 12 31 57 AM" src="https://github.com/user-attachments/assets/ce2b50bb-fca2-4f51-be92-a6bcba4d422f" />



```bash
sudo docker-compose -f docker-compose.yml up -d
```


4️⃣ Verify Docker Setup

Check images:

```bash
docker image ls
```

Check containers:

```bash
docker container ls
```

```bash
docker exec -it <containerid> /bin/sh
```

5️⃣ Test Connectivity to FortiDAST Registry

```bash
curl -v registry.fortidast.forticloud.com
```

Expected:

HTTP redirect to HTTPS (port 443)
Successful connection


6️⃣ Monitor Proxy Logs

```bash
docker-compose logs -f
```

### Final Step: Scan from UI.


## 🔍 OWASP LLM FortiDAST Scan Result Demonstrated

<img width="796" height="68" alt="Screenshot 2026-04-28 at 12 29 54 AM" src="https://github.com/user-attachments/assets/a3b53b40-35d4-4a81-87d3-7afeede809d5" />




<img width="1152" height="637" alt="Screenshot 2026-04-28 at 12 29 21 AM" src="https://github.com/user-attachments/assets/ffd4b994-fce0-4540-92d9-9af85d9cafcd" />



















