## FortiCNAPP FortiDAST Proxy Server
<br>


### 📘 Reference Links

| Topic | Documentation Link |
|--------|---------------------|
| ** FortiDAST Proxy Server** | [https://docs.fortinet.com/document/fortidast/26.1.0/user-guide/688454/fortidast-proxy-server) |
                  
<br>

## 🚀 FortiDAST Proxy Setup (Docker)

This guide shows how to install Docker, pull the FortiDAST proxy image, and run the proxy container.

---

## 📋 Steps

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

4️⃣ Verify Docker Setup

Check images:

```bash
docker image ls
```

Check containers:

```bash
docker container ls
```

5️⃣ Test Connectivity to FortiDAST Registry

```bash
curl -v registry.fortidast.forticloud.com
```

Expected:

HTTP redirect to HTTPS (port 443)
Successful connection


6️⃣ Start FortiDAST Proxy Container

```bash
sudo docker-compose -f docker-compose.yml up -d
```

7️⃣ Monitor Proxy Logs

```bash
docker-compose logs -f
```

### Final Step: Scan from UI.










