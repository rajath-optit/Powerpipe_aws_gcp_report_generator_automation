# **PowerPipe Installation and Usage Guide**  
### *Comprehensive Guide for AWS Security & Compliance Audits*  

---

## **📌 Table of Contents**  
1️⃣ [Installation Guide for PowerPipe](#installation-guide-for-powerpipe)  
2️⃣ [Setup PowerPipe](#setup-powerpipe)  
3️⃣ [Initialize for a Cloud Account](#initialize-for-a-cloud-account)  
4️⃣ [Generate Final Report](#generate-final-report)  
5️⃣ [Review the Report](#review-the-report)  
6️⃣ [Remediate Issues](#remediate-issues)  

---

## **1️⃣ Installation Guide for PowerPipe**  

### **Prerequisites**  
Ensure the following dependencies are installed before proceeding:  

✅ **Docker** – Required for running PowerPipe and Steampipe in containers.  
✅ **AWS CLI** – Needed for authentication with AWS services.  
✅ **tmux (optional)** – Helps manage long-running processes.  

### **Create Setup Directory**  
Run the following commands to set up a working directory:  

```sh
mkdir setup_powerpipe  
cd setup_powerpipe  
```

### **Create Necessary Directories**  
PowerPipe stores logs and reports in a dedicated directory:  

```sh
sudo mkdir -p /opt/powerpipedata/logs  
sudo chmod 777 /opt/powerpipedata/logs  
```

✅ **All logs and snapshots will be stored here.**  

---

## **2️⃣ Setup PowerPipe**  

### **Create a Docker Network**  
Set up a dedicated Docker network:  

```sh
sudo docker network create powerpipe-network  
```

### **Build the PowerPipe Docker Image**  

#### **Create a Dockerfile**  
Create a `Dockerfile` with the following content:  

```dockerfile
FROM ubuntu:latest  

# Install dependencies  
RUN apt-get update && \  
    apt-get install -y curl tar && \  
    groupadd -g 1001 powerpipe && \  
    useradd -u 1001 --create-home --shell /bin/bash --gid powerpipe powerpipe  

# Install PowerPipe  
RUN curl -LO https://github.com/turbot/powerpipe/releases/download/v0.3.1/powerpipe.linux.amd64.tar.gz && \  
    tar xvzf powerpipe.linux.amd64.tar.gz && \  
    mv powerpipe /usr/local/bin/powerpipe && \  
    rm -rf powerpipe.linux.amd64.tar.gz  

# Install Steampipe  
RUN curl -LO https://steampipe.io/install/steampipe.sh && \  
    sudo sh steampipe.sh && \  
    rm -f steampipe.sh  

# Install AWS plugin  
RUN steampipe plugin install aws  

ENTRYPOINT ["/bin/bash", "-c", "powerpipe server"]  
```

#### **Build the Docker Image**  

```sh
sudo docker build -t powerpipe-image .  
```

---

## **3️⃣ Initialize for a Cloud Account**  

### **Run the PowerPipe Container**  

```sh
sudo docker run -d --name powerpipe-container \  
  --network powerpipe-network \  
  -p 9024:9024 \  
  -p 9125:9125 \  
  -e AWS_ACCESS_KEY_ID=AKIAEXAMPLE123 \  
  -e AWS_SECRET_ACCESS_KEY=EXAMPLEKEY123 \  
  -e AWS_REGION=ap-south-1 \  
  -v /opt/powerpipedata/logs:/home/powerpipe/mod \  
  powerpipe-image  
```

✅ **This starts PowerPipe and binds ports 9024 and 9125.**  

### **Verify Running Containers**  

```sh
docker ps  
```

### **Access the Container**  

```sh
sudo docker exec -it powerpipe-container /bin/bash  
```

### **Initialize PowerPipe Mods**  

```sh
mkdir -p /home/powerpipe/mod  
cd /home/powerpipe/mod  
powerpipe mod init  
```

### **Install Compliance Mods**  

```sh
powerpipe mod install github.com/turbot/steampipe-mod-aws-compliance  
powerpipe mod install github.com/turbot/steampipe-mod-aws-insights  
powerpipe mod install github.com/turbot/steampipe-mod-aws-thrifty  
powerpipe mod install github.com/turbot/steampipe-mod-aws-well-architected  
powerpipe mod install github.com/turbot/steampipe-mod-aws-top-10  
```

✅ **These modules provide AWS security and compliance checks.**  

---

## **4️⃣ Generate Final Report**  

### **Start Steampipe Service**  

```sh
nohup steampipe service start --port 9025 > steampipe.log 2>&1 &  
```

✅ **Use a unique port for each client.**  

### **Start PowerPipe Server**  

```sh
nohup powerpipe server --port 9125 > powerpipe.log 2>&1 &  
```

✅ **PowerPipe is now accessible at:** `http://10.10.30.93:9125/`  

---

## **5️⃣ Review the Report**  

### **Important Reports**  

#### **All Controls**  

```sh
aws_compliance.benchmark.all_controls  
```

#### **Security & Compliance**  

```sh
aws_compliance.benchmark.foundational_security  
aws_well_architected.benchmark.well_architected_framework  
aws_top_10.benchmark.account_security  
```

#### **Cost Optimization**  

```sh
aws_thrifty.benchmark.ec2  
aws_thrifty.benchmark.s3  
aws_thrifty.benchmark.rds  
aws_thrifty.benchmark.cloudwatch  
```

📌 **For quick access to all necessary reports, use:**  

```sh
python important_mod_link_open.py  
```

✅ **Automation scripts add priority/severity findings and remediation actions.**  

---

## **6️⃣ Remediate Issues**  

### **Run PowerPipe with Root Access**  

```sh
sudo docker run -d --name powerpipe-container-root \  
  --network powerpipe-network \  
  -p 9024:9024 \  
  -p 9125:9125 \  
  -e AWS_ACCESS_KEY_ID=AKIAEXAMPLE123 \  
  -e AWS_SECRET_ACCESS_KEY=EXAMPLEKEY123 \  
  -e AWS_REGION=ap-south-1 \  
  --user root \  
  powerpipe-image  
```

### **Using Steampipe for Multi-Account Support**  

```sh
docker pull steampipe  
docker run -e AWS_ACCESS_KEY_ID=your_access_key -e AWS_SECRET_ACCESS_KEY=your_secret_key steampipe  
```

✅ **This setup allows managing multiple AWS accounts in isolated environments.**  

---

## **🚀 Alternative to PowerPipe: Using Steampipe for Custom Reporting**  

If the PowerPipe dashboard is unavailable, Steampipe provides a flexible CLI-based solution.  

### **Installation**  

```sh
steampipe plugin install aws  
```

### **Example Query**  

```sql
select 
  title, 
  create_date, 
  mfa_enabled 
from 
  aws_iam_user;  
```

### **Output Example:**  

```plaintext
+-----------------+---------------------+-------------+
| title           | create_date         | mfa_enabled |
+-----------------+---------------------+-------------+
| pam_beesly      | 2005-03-24 21:30:00 | false       |
| creed_bratton   | 2005-03-24 21:30:00 | true        |
| stanley_hudson  | 2005-03-24 21:30:00 | false       |
+-----------------+---------------------+-------------+
```

---

## **📌 Final Notes & Next Steps**  

✅ **AWS & GCP Support:** Use corresponding configurations for GCP security scans.  
✅ **Cost Reports:** Use the cost optimization script to generate financial insights.  
✅ **Follow Execution Order:** Scripts are numbered for sequential execution.  
✅ **Client Report Delivery:** Ensure reports include graphs and tables for documentation.  

📌 **For more details, visit the GitHub repository & README.** 🚀

---------------------------------------------------set username and password----------------------------------
# **2. Comprehensive Guide: Setting Up Username-Password Authentication in Nginx**  

## **📌 Overview**  
In web security, protecting resources from unauthorized access is crucial. One simple yet effective method is **Basic Authentication** using a username and password. This document provides a **step-by-step guide** to implementing Basic Authentication in Nginx, including why it's needed, how to configure it, and how to troubleshoot issues.

---

## **🔍 What is Basic Authentication?**  
Basic Authentication is a simple HTTP authentication method that requires users to enter a **username and password** before accessing a webpage or API. The credentials are verified against a stored file containing hashed passwords.

### **Why Use Basic Authentication?**  
✅ **Quick and easy to implement**  
✅ **Prevents unauthorized access to sensitive resources**  
✅ **Works without requiring additional software or database**  
✅ **Compatible with almost all web browsers and API clients**  

🔴 **Limitations**:  
⚠️ Credentials are sent in **every request** (even though they are base64-encoded, they are not encrypted).  
⚠️ Not as secure as OAuth or JWT authentication.  
⚠️ Best suited for **internal applications** or **low-risk** web resources.

---

# **📖 Step 1: Install Required Tools**  
Before setting up authentication, you need the `apache2-utils` package, which includes the `htpasswd` tool to manage password files.

### **🔹 For Ubuntu/Debian**  
```bash
sudo apt update
sudo apt install apache2-utils -y
```

### **🔹 For CentOS/RHEL**  
```bash
sudo yum install httpd-tools -y
```

To verify the installation:
```bash
htpasswd -h
```
If installed correctly, you should see usage instructions.

---

# **📖 Step 2: Create a `.htpasswd` File**  
The `.htpasswd` file stores usernames and their **hashed passwords**.

### **🔹 Create a New `.htpasswd` File** (For First User)  
```bash
htpasswd -c /etc/nginx/.htpasswd myuser
```
- `-c`: Creates a new file (only use this the first time).  
- `myuser`: The username (replace with your own).  
- You will be prompted to enter a password (it will be **hashed** and stored securely).  

### **🔹 Add Another User** (Without Overwriting Existing Users)  
```bash
htpasswd /etc/nginx/.htpasswd anotheruser
```

### **🔹 Alternative: Create `.htpasswd` Using OpenSSL**  
```bash
echo "myuser:$(openssl passwd -apr1 'mypassword')" >> /etc/nginx/.htpasswd
```
- This avoids using `htpasswd` if `apache2-utils` is unavailable.  
- Uses **MD5-based APR1 hashing** for security.

### **🔹 Verify the `.htpasswd` File**  
```bash
cat /etc/nginx/.htpasswd
```
Example output:
```
myuser:$apr1$xyz123$abcdefg123456
anotheruser:$apr1$hijklmn$9876543abcd
```

---

# **📖 Step 3: Configure Nginx for Authentication**  
After creating the `.htpasswd` file, modify the **Nginx site configuration** to enforce authentication.

### **🔹 Open Your Nginx Configuration File**  
```bash
sudo nano /etc/nginx/sites-available/default
```
OR  
```bash
sudo nano /etc/nginx/sites-available/powerpipe
```

### **🔹 Add the Authentication Block**  
Inside the `server` block, add the following:

```nginx
location /secure/ {
    auth_basic "Restricted Area";  # Message displayed on login prompt
    auth_basic_user_file /etc/nginx/.htpasswd;
}
```

### **🔹 Example: Full Nginx Configuration File**  
```nginx
server {
    listen 443 ssl;
    server_name mydomain.com;

    # SSL Configuration (Modify for your SSL certs)
    ssl_certificate /etc/nginx/ssl/selfsigned.crt;
    ssl_certificate_key /etc/nginx/ssl/selfsigned.key;

    # Authentication for a specific directory
    location /secure/ {
        auth_basic "Restricted Area";
        auth_basic_user_file /etc/nginx/.htpasswd;
    }

    # Allow access to the manifest file without authentication
    location /manifest.json {
        auth_basic off;
        proxy_pass http://mybackendserver:9102/manifest.json;
    }

    # Reverse proxy to backend application
    location / {
        proxy_pass http://mybackendserver:9102;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
    }
}
```

---

# **📖 Step 4: Restart and Test Nginx**  
After modifying the configuration, restart Nginx to apply the changes.

### **🔹 Restart Nginx**  
```bash
sudo systemctl restart nginx
```

### **🔹 Verify Nginx Status**  
```bash
sudo systemctl status nginx
```

### **🔹 Open Your Browser and Test**  
Go to:  
```
https://mydomain.com/secure/
```
You should see a **login prompt** requesting your username and password.

---

# **📖 Step 5: Troubleshooting Common Issues**  

### **🔹 403 Forbidden or 500 Internal Server Error**  
✅ Check if the `.htpasswd` file exists and is readable:  
```bash
ls -l /etc/nginx/.htpasswd
```
✅ Ensure Nginx has the correct permissions:  
```bash
sudo chmod 640 /etc/nginx/.htpasswd
```

### **🔹 No Login Prompt Appears?**  
✅ Ensure Nginx is configured correctly:  
```bash
sudo nginx -t
```
If there’s a syntax error, fix it before restarting Nginx.

✅ Check Nginx logs:  
```bash
sudo journalctl -xe  # View system logs  
sudo tail -f /var/log/nginx/error.log  # View Nginx error log  
```

### **🔹 Browser Caches Old Credentials**  
If you entered incorrect credentials and your browser remembers them, clear saved logins or use **incognito mode** to test again.

---

# **📖 Step 6: Enhancing Security**  

### **🔹 1. Restrict Access to the `.htpasswd` File**  
Ensure that `.htpasswd` is only accessible to Nginx and administrators:  
```bash
sudo chown root:nginx /etc/nginx/.htpasswd
sudo chmod 640 /etc/nginx/.htpasswd
```

### **🔹 2. Use Fail2Ban to Protect Against Brute Force Attacks**  
Fail2Ban can block repeated failed login attempts:  
```bash
sudo apt install fail2ban -y
```

### **🔹 3. Use HTTPS to Encrypt Authentication Data**  
Always **use SSL/TLS** to prevent passwords from being sent in plain text. Ensure your Nginx configuration has valid SSL certificates.

---

# **🚀 Summary: What This Guide Covers**
✅ **Installed** required tools (`apache2-utils`)  
✅ **Created** a secure `.htpasswd` file  
✅ **Configured** Nginx to enforce authentication  
✅ **Restarted and tested** the setup  
✅ **Troubleshot** common issues  
✅ **Enhanced security** with permissions and best practices  

---

# **📌 Why This Is Useful?**
🔹 **Provides a simple authentication method** for securing internal applications.  
🔹 **No need for a database** or additional authentication services.  
🔹 **Quick and effective** way to restrict access to specific URLs.  

Would you like additional enhancements, such as **auto-blocking failed login attempts** or **advanced logging**? Let me know! 🚀


----------------------------------------------
# [3. reference: when setting up username-password authentication for a URL in Nginx.] 
---

# **Setting Up Username-Password Authentication in Nginx**

## **1️⃣ Navigate to the Nginx Configuration Directory**
First, move into the `sites-available` directory, where Nginx configuration files are stored:
```bash
cd /etc/nginx/sites-available/
ls -ltr  # List files in detail
```

## **2️⃣ Checking Existing Configurations**
To inspect the existing Nginx site configuration files, use:
```bash
less default
less powerpipe
```

## **3️⃣ Creating a New `.htpasswd` File**
To enable basic authentication, create a password file using `htpasswd`:

### **Creating a New User File**
Use this command to create a new `.htpasswd` file with a username:
```bash
htpasswd -c /etc/nginx/.htpasswd username
```
- The `-c` flag creates a new file (use it only the first time).
- You will be prompted to enter a password for the user.

### **Adding a New User to an Existing File**
If `.htpasswd` already exists, add another user without the `-c` flag:
```bash
htpasswd /etc/nginx/.htpasswd anotheruser
```

### **Alternative Using OpenSSL**
Another way to generate user credentials using OpenSSL:
```bash
echo "username:$(openssl passwd -apr1 'yourpassword')" >> /etc/nginx/.htpasswd
```

## **4️⃣ Configuring Nginx to Use the Password File**
After creating the `.htpasswd` file, edit your Nginx site configuration file (`/etc/nginx/sites-available/default` or `powerpipe`) and add the authentication settings:

```nginx
location /secure/ {
    auth_basic "Restricted Area";
    auth_basic_user_file /etc/nginx/.htpasswd;
}
```

Save the file and restart Nginx:
```bash
sudo systemctl restart nginx
```

## **5️⃣ Verifying Authentication**
Open a browser and go to:
```
http://yourdomain.com/secure/
```
It should prompt for a username and password.

### **Troubleshooting**
If authentication fails, check logs:
```bash
sudo journalctl -xe
sudo tail -f /var/log/nginx/error.log
```

---

# **Adding a New Client Configuration in Nginx (`powerpipe` Example)**

To configure authentication and proxy settings for a new client inside the `powerpipe` Nginx configuration file, add the following block:

```nginx
# HTTPS Configuration for Foradian Container 1 (Port 9102)
server {
    listen 443 ssl;
    server_name 10.10.30.93;
 
    # SSL Configuration
    ssl_certificate /etc/nginx/ssl/selfsigned.crt;
    ssl_certificate_key /etc/nginx/ssl/selfsigned.key;
 
    # SSL Protocols & Ciphers for better security
    ssl_protocols TLSv1.2 TLSv1.3;
    ssl_ciphers 'HIGH:!aNULL:!MD5';
 
    # Basic Authentication for Foradian Container 1
    auth_basic "Restricted Area";
    auth_basic_user_file /etc/nginx/.htpasswd-foradian1;
 
    # WebSocket for Foradian Container 1
    location /ws {
        proxy_pass http://localhost:9102;  
        proxy_http_version 1.1;
        proxy_set_header Upgrade $http_upgrade;
        proxy_set_header Connection "upgrade";
        proxy_set_header Host $host;
        proxy_cache_bypass $http_upgrade;
    }
 
    # Manifest without authentication
    location /manifest.json {
        proxy_pass http://10.10.30.93:9102/manifest.json;
        auth_basic off;
    }
 
    # Proxy for Powerpipe app
    location / {
        proxy_pass http://10.10.30.93:9102;  
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
    }
}
```

### **Modifications for a New Client**
- **Change the `server_name`** to the new client’s IP or domain.
- **Modify the `listen` port** (e.g., change `443` to `444` or an unused port).
- **Update authentication file reference** (`.htpasswd-foradian1` → `.htpasswd-newclient`).
- **Adjust the backend service port** (`9102` → desired application port).

### **Restart Nginx**
```bash
sudo systemctl restart nginx
```

---

# **Final Notes**
- Ensure **SSL certificates** are correctly configured if using HTTPS.
- Keep the `.htpasswd` file secure and restrict access using file permissions:
  ```bash
  sudo chmod 640 /etc/nginx/.htpasswd
  ```
- Always test changes before deploying to production.

This document serves as a **quick reference guide** for setting up authentication and proxy configurations in Nginx. 🚀
