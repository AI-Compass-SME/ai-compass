
# Deployment Plan & Strategy

## 1. Project Overview & Requirements
**Active Components:**
*   **Backend:** `Application_Prototype/mvp_v1/backend` (FastAPI)
*   **Frontend:** `Application_Prototype/mvp_v1/frontend` (Vite + React)
*   **Core Logic:** `benchmarking_ai` (Root Level - *Critical Dependency*)

---

## 2. Repository Strategy: Staying "Clean"
Since you want to avoid changing your current repository, here are the two best options for managing your deployment code:

### Option A: Forking (The "History" Path)
**Recommended if:** You want to keep the full history of the project and might pull experimental updates from the original repo later.
- **Action:** Fork the repo on GitHub.
- **Management:** Perform all restructuring (moving folders for Plan B) in the fork. Use the fork for your live deployments.

### Option B: New "Production" Repository (The "Clean" Path) - **RECOMMENDED**
**Recommended if:** You want a clean, professional repo that only contains the app logic without the research/EDA clutter. 
- **Action:** Create a brand new repository (e.g., `ai-compass-prod`).
- **Management:** Copy only `Application_Prototype/mvp_v1` and `benchmarking_ai` into the root of this new repo. 
- **Benefit:** It's lighter, faster to clone on your VPS, and much easier to secure (no unnecessary scripts or data).

---

## 3. Plan A: VPS Deployment (Recommended for Control)
**Platform:** Hostinger (VPS)
**Strategy:** "Lift and Shift"
**Valid for:** Current folder structure (Monorepo). No restructuring required.

### Deployment Checklist

#### 1. Server Preparation
- [ ] **Provision VPS:** Ubuntu 22.04 LTS recommended.
- [ ] **SSH Access:** `ssh root@<your-ip>`
- [ ] **Security (Uncomplicated Firewall - UFW):**
    ```bash
    ufw allow OpenSSH
    ufw allow 'Nginx Full'
    ufw enable
    ```
- [ ] **Update OS:** `apt update && apt upgrade -y`
- [ ] **Install Core Dependencies:**
    ```bash
    apt install -y python3-pip python3-venv nodejs npm nginx git
    npm install -g pm2
    ```

#### 2. Docker Setup (Future-Proofing)
Even if you don't use it immediately, installing Docker now makes future updates and CI/CD much easier.
- [ ] **Install Docker Engine:**
    ```bash
    # Add Docker's official GPG key:
    sudo apt-get update
    sudo apt-get install ca-certificates curl
    sudo install -m 0755 -d /etc/apt/keyrings
    sudo curl -fsSL https://download.docker.com/linux/ubuntu/gpg -o /etc/apt/keyrings/docker.asc
    sudo chmod a+r /etc/apt/keyrings/docker.asc

    # Add the repository to Apt sources:
    echo \
      "deb [arch=$(dpkg --print-architecture) signed-by=/etc/apt/keyrings/docker.asc] https://download.docker.com/linux/ubuntu \
      $(. /etc/os-release && echo "$VERSION_CODENAME") stable" | \
      sudo tee /etc/apt/sources.list.d/docker.list > /dev/null
    sudo apt-get update
    
    # Install Check:
    sudo apt-get install docker-ce docker-ce-cli containerd.io docker-buildx-plugin docker-compose-plugin -y
    ```
- [ ] **Post-Installation Steps:**
    ```bash
    # Run Docker without sudo (for your deployer user):
    sudo usermod -aG docker deployer
    newgrp docker
    # Verify installation
    docker run hello-world
    ```

#### 3. Application Setup
- [ ] **Clone Repository:**
    ```bash
    cd /var/www
    git clone https://github.com/your-username/ai-compass.git
    cd ai-compass
    ```
- [ ] **Backend Setup:**
    ```bash
    cd Application_Prototype/mvp_v1/backend
    python3 -m venv venv
    source venv/bin/activate
    pip install -r requirements.txt
    # Setup .env file
    cp .env.example .env
    nano .env # Add Prod DB URL
    ```
- [ ] **Frontend Setup:**
    ```bash
    cd ../frontend
    npm install
    # Create production build
    npm run build
    # Verify 'dist' folder exists
    ```

#### 4. Process Management (PM2 & Systemd)
- [ ] **Backend Service (Systemd or PM2):**
    *   Command: `uvicorn main:app --host 127.0.0.1 --port 8000`
    *   *Note: Ensure `benchmarking_ai` is accessible via PYTHONPATH or relative imports.*
- [ ] **Frontend Serving (Nginx):**
    *   Configure Nginx to return `index.html` for SPA routing.

#### 5. Nginx Reverse Proxy Configuration
- [ ] **Create Config:** `/etc/nginx/sites-available/ai-compass`
    ```nginx
    server {
        listen 80;
        server_name your-domain.com;

        # Frontend (Static Files)
        location / {
            root /var/www/ai-compass/Application_Prototype/mvp_v1/frontend/dist;
            try_files $uri $uri/ /index.html;
        }

        # Backend (API Proxy)
        location /api/ {
            proxy_pass http://127.0.0.1:8000;
            proxy_set_header Host $host;
            proxy_set_header X-Real-IP $remote_addr;
        }
    }
    ```
- [ ] **Enable Site:** `ln -s /etc/nginx/sites-available/ai-compass /etc/nginx/sites-enabled/`
- [ ] **Test & Reload:** `nginx -t && systemctl reload nginx`

#### 6. Finalization
- [ ] **SSL Certification:** `certbot --nginx -d your-domain.com`

### Security & Maintenance Guide (Critical for Plan A)
Since you are managing the server, you must perform these steps to keep it secure.

#### 1. Initial Security Hardening (Run once after provisioning as root)
- [ ] **Create Non-Root User:**
    ```bash
    adduser deployer
    usermod -aG sudo deployer
    su - deployer
    ```
- [ ] **Disable Root SSH Login (Optional but Recommended):**
    - Edit `/etc/ssh/sshd_config`: Ensure `PermitRootLogin no`.
    - Restart SSH: `sudo systemctl restart ssh`.
- [ ] **Install Fail2Ban:**
    - Protects against brute-force attacks on SSH.
    - `sudo apt install fail2ban -y`
    - `sudo systemctl enable fail2ban && sudo systemctl start fail2ban`
- [ ] **Enable Unattended Upgrades:**
    - Automatically installs critical security patches.
    - `sudo apt install unattended-upgrades -y`
    - `sudo dpkg-reconfigure --priority=low unattended-upgrades`

#### 2. Ongoing Maintenance Routine
- [ ] **Weekly/Monthly:** Run system updates to keep packages secure.
    - `sudo apt update && sudo apt upgrade -y`
    - Check disk space: `df -h`
- [ ] **Monitoring:** Check logs if something fails.
    - App Logs: `pm2 logs`
    - System Logs: `/var/log/syslog`
- [ ] **Backups:**
    - Regularly backup your PostgreSQL database (`pg_dump`).
    - Backup your `.env` file.

---

## Plan B: PaaS Deployment
**Platform:** Render (Backend) + Vercel (Frontend)
**Strategy:** "Cloud Native"
**Requirement:** **Code Restructuring is Highly Recommended** to make the backend self-contained.

### Deployment Checklist

#### 1. Preparation (Restructuring)
- [ ] **Move Logic:**
    *   Move `benchmarking_ai` folder -> `Application_Prototype/mvp_v1/backend/modules/benchmarking_ai`.
- [ ] **Update Code:**
    *   Refactor imports in `backend/` to use `from .modules.benchmarking_ai import ...`.
    *   Remove `sys.path.append(...)` hacks in `config.py`.
- [ ] **Update Requirements:** Ensure all ML dependencies are in `backend/requirements.txt`.

#### 2. Backend (Render)
- [ ] **Create Web Service:** Connect GitHub Repo.
- [ ] **Root Directory:** `Application_Prototype/mvp_v1/backend`
- [ ] **Build Command:** `pip install -r requirements.txt`
- [ ] **Start Command:** `uvicorn main:app --host 0.0.0.0 --port 10000`
- [ ] **Environment Variables:** `DATABASE_URL`, `PYTHON_VERSION=3.11.x`.

#### 3. Frontend (Vercel)
- [ ] **Create Project:** Connect GitHub Repo.
- [ ] **Root Directory:** `Application_Prototype/mvp_v1/frontend`
- [ ] **Framework:** Vite.
- [ ] **Build Command:** `npm run build`.
- [ ] **Output Directory:** `dist`.
- [ ] **Env Vars:** `VITE_API_URL` (Your Render URL).

---

## Comparison
| Feature | Plan A (VPS) | Plan B (PaaS) |
| :--- | :--- | :--- |
| **Complexity** | High (Manual Config) | Low (Automated) |
| **Control** | Full (Root Access) | Limited (Managed) |
| **Scalability** | Manual | Automatic |
| **Maintenance** | High (Updates/Security) | Zero |
| **Cost** | Low/Fixed | Variable |
