# Deployment Steps for EC2

Follow these steps to deploy the Django application on an AWS EC2 instance.

## 1. Prepare EC2 Instance
- Launch an EC2 instance (Ubuntu 22.04 LTS recommended).
- Ensure Security Group allows inbound traffic on port 80 (HTTP) and port 22 (SSH).
- Connect to your instance via SSH.

## 2. Install Dependencies (Docker Compose V2)
Before installing Docker, uninstall any conflicting packages:

```bash
for pkg in docker.io docker-doc docker-compose docker-compose-v2 podman-docker containerd runc; do sudo apt-get remove $pkg; done
```

Run the following commands on the server to install the latest Docker and Docker Compose V2. This avoids compatibility issues like `KeyError: 'ContainerConfig'`.

```bash
# Add Docker's official GPG key:
sudo apt-get update
sudo apt-get install ca-certificates curl gnupg
sudo install -m 0755 -d /etc/apt/keyrings
curl -fsSL https://download.docker.com/linux/ubuntu/gpg | sudo gnupg --dearmor -o /etc/apt/keyrings/docker.gpg
sudo chmod a+r /etc/apt/keyrings/docker.gpg

# Add the repository to Apt sources:
echo \
  "deb [arch="$(dpkg --print-architecture)" signed-by=/etc/apt/keyrings/docker.gpg] https://download.docker.com/linux/ubuntu \
  "$(. /etc/os-release && echo "$VERSION_CODENAME")" stable" | \
  sudo tee /etc/apt/sources.list.d/docker.list > /dev/null
sudo apt-get update

# Install Docker and the Compose plugin:
sudo apt-get install docker-ce docker-ce-cli containerd.io docker-buildx-plugin docker-compose-plugin

# Verify installation (should be Docker Compose version v2.x.x)
docker compose version
```

### Post-Installation Setup
```bash
sudo systemctl start docker
sudo systemctl enable docker
sudo usermod -aG docker $USER
```
*Note: Logout and log back in for group changes to take effect.*

## 3. Clone and Setup
Clone the repository and navigate to the deployment directory:

```bash
git clone <your-repo-url>
cd django-mvp-backend-demo/deploy
```


> [!IMPORTANT]
> Change the `SECRET_KEY`, `DB_PASSWORD`, and update `ALLOWED_HOSTS` to include your server's IP or domain.
> Ensure `DEBUG=False` is set.

## 5. Build and Start Services
Run Docker Compose using the production file and pointing to your environment file:

```bash
# We use -f to specify the production compose file
docker compose -f docker-compose.prod.yml up --build -d
```

## 6. Post-Deployment
- The application should now be accessible at `http://<your-ec2-ip>/`.
- Static files are served by Nginx from the `static_volume`.
- Port 8000 is NOT exposed to the public; it is only accessible internally by Nginx.

## Troubleshooting
- **"could not translate host name 'db'"**: This usually means the `db` container failed to start. Check `docker logs deploy-db-1` to see why. Most common cause is missing `POSTGRES_PASSWORD` in `.env.prod`.
- **Environment Variables**: Docker Compose uses `.env.prod` (via `env_file`) inside the containers. I have updated the yaml to be direct.
- **Check logs**: `docker compose -f docker-compose.prod.yml logs -f`
- **Restart services**: `docker compose -f docker-compose.prod.yml restart`
