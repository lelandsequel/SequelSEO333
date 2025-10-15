# 📊 Google Sheets & Drive Setup Guide

This guide walks you through setting up automatic uploads to Google Sheets and Google Drive for your SEO lead finder.

---

## 🎯 What You'll Get

After setup, your automation will:
- ✅ **Upload CSV data** → Google Sheets (structured, filterable data)
- ✅ **Upload sales reports** → Google Drive (full intelligence reports)
- ✅ **Access from anywhere** → View leads on any device
- ✅ **Share with team** → Easy collaboration

---

## 🤖 What is a Service Account?

A **Service Account** is like a "robot user" for Google services:

- **Regular Account**: You (human) log in with username/password
- **Service Account**: Robot logs in with a JSON key file

**Why we need it:**
- Your automation runs on GitHub Actions (no human to click "login")
- The service account can upload files automatically
- It's secure - the JSON key is stored as a GitHub Secret

---

## 🛠️ Setup Steps

### **STEP 1: Create Google Cloud Project**

1. Go to: https://console.cloud.google.com/
2. Sign in with your Google account
3. Click the **project dropdown** at the top (says "Select a project")
4. Click **"NEW PROJECT"**
5. Name it: `SEO Lead Finder` or `C&L Page Services`
6. Click **"CREATE"**
7. Wait ~30 seconds for it to be created

---

### **STEP 2: Enable Required APIs**

1. Make sure your new project is selected (check top bar)
2. Go to: https://console.cloud.google.com/apis/library
3. Search for: `Google Sheets API`
4. Click it → Click **"ENABLE"**
5. Go back to API Library
6. Search for: `Google Drive API`
7. Click it → Click **"ENABLE"**

---

### **STEP 3: Create Service Account**

1. Go to: https://console.cloud.google.com/iam-admin/serviceaccounts
2. Click **"+ CREATE SERVICE ACCOUNT"** (top of page)
3. **Service account name:** `seo-lead-finder`
4. **Service account ID:** (auto-fills, leave it)
5. **Description:** `Automated lead finder uploads`
6. Click **"CREATE AND CONTINUE"**
7. **Role:** Skip this step - click **"CONTINUE"**
8. Click **"DONE"**

---

### **STEP 4: Create & Download JSON Key**

1. You should see your service account in the list: `seo-lead-finder@...`
2. **Click on it** (the email address)
3. Go to the **"KEYS"** tab (top of page)
4. Click **"ADD KEY"** → **"Create new key"**
5. Select **"JSON"**
6. Click **"CREATE"**
7. **A file downloads** - this is your credentials file!

**⚠️ IMPORTANT:** Save this file securely - it's like a password!

The file will be named something like: `seo-lead-finder-abc123.json`

---

### **STEP 5: Note the Service Account Email**

1. **Open the JSON file** you just downloaded (in a text editor)
2. **Find the line** that says `"client_email"`
3. **Copy that email** - it looks like:
   ```
   seo-lead-finder@your-project-123.iam.gserviceaccount.com
   ```
4. **Keep this handy** - you'll need it in the next steps!

---

### **STEP 6: Create Google Sheet**

1. Go to: https://sheets.google.com
2. Create a **new blank spreadsheet**
3. Name it: `SEO Leads - C&L Page Services`
4. Click the **"Share"** button (top right)
5. **Paste the service account email** from Step 5
6. Give it **"Editor"** access
7. **Uncheck "Notify people"** (it's a robot, not a person!)
8. Click **"Share"**
9. **Copy the Spreadsheet ID** from the URL:
   - URL: `https://docs.google.com/spreadsheets/d/1ABC123xyz.../edit`
   - ID: `1ABC123xyz...` (the part between `/d/` and `/edit`)

**Save this ID** - you'll need it for your `.env` file!

---

### **STEP 7: Create Google Drive Folder**

1. Go to: https://drive.google.com
2. Click **"New"** → **"Folder"**
3. Name it: `SEO Lead Reports`
4. **Right-click the folder** → **"Share"**
5. **Paste the service account email** again
6. Give it **"Editor"** access
7. Click **"Share"**
8. **Open the folder** and **copy the Folder ID** from the URL:
   - URL: `https://drive.google.com/drive/folders/1XYZ789abc...`
   - ID: `1XYZ789abc...` (the part after `/folders/`)

**Save this ID** - you'll need it for your `.env` file!

---

### **STEP 8: Install the JSON Key File**

1. **Create a `secrets` folder** in your project:
   ```bash
   mkdir -p secrets
   ```

2. **Move the JSON file** you downloaded to this location:
   ```bash
   mv ~/Downloads/seo-lead-finder-*.json secrets/google-service-account.json
   ```

3. **Verify it's there:**
   ```bash
   ls -l secrets/google-service-account.json
   ```

---

### **STEP 9: Update Your `.env` File**

Open `seo_lead_finder/.env` and update these lines:

```bash
# Google Sheets & Drive (OPTIONAL - CSV output always works)
GOOGLE_SHEETS_SERVICE_ACCOUNT_JSON_PATH=./secrets/google-service-account.json
GOOGLE_SHEETS_SPREADSHEET_ID=1ABC123xyz...  # ← Paste your Sheet ID here
GOOGLE_SHEETS_WORKSHEET_NAME=Leads
GOOGLE_DRIVE_FOLDER_ID=1XYZ789abc...  # ← Paste your Drive Folder ID here
```

**Replace:**
- `1ABC123xyz...` with your actual Spreadsheet ID from Step 6
- `1XYZ789abc...` with your actual Folder ID from Step 7

---

### **STEP 10: Test It Locally**

Run a test search to verify uploads work:

```bash
python3 main.py --once --geo "Houston, TX"
```

**You should see:**
```
✅ CSV saved: ./out/leads_20251014_123456.csv
✅ Uploaded to Google Drive: leads_20251014_123456.csv
   URL: https://drive.google.com/file/d/...
✅ Google Sheets updated: 100 rows appended
✅ Sales report saved: ./out/sales_report_Houston_TX_2025-10-14.txt
✅ Uploaded to Google Drive: sales_report_Houston_TX_2025-10-14.txt
   URL: https://drive.google.com/file/d/...
```

**Check:**
1. Go to your Google Sheet - you should see lead data
2. Go to your Google Drive folder - you should see CSV + TXT files

---

### **STEP 11: Add to GitHub Secrets (for Automation)**

For weekly automation to work, add the credentials to GitHub:

1. Go to: https://github.com/lelandsequel/SequelSEO333/settings/secrets/actions
2. Click **"New repository secret"**
3. Add these secrets:

**Secret 1: GOOGLE_SERVICE_ACCOUNT_JSON**
- Name: `GOOGLE_SERVICE_ACCOUNT_JSON`
- Value: Copy/paste the **entire contents** of `secrets/google-service-account.json`

**Secret 2: GOOGLE_SHEETS_SPREADSHEET_ID**
- Name: `GOOGLE_SHEETS_SPREADSHEET_ID`
- Value: Your Spreadsheet ID from Step 6

**Secret 3: GOOGLE_DRIVE_FOLDER_ID**
- Name: `GOOGLE_DRIVE_FOLDER_ID`
- Value: Your Folder ID from Step 7

---

## ✅ You're Done!

Now your automation will:
- ✅ Save CSV files locally
- ✅ Upload CSV data to Google Sheets
- ✅ Upload CSV files to Google Drive
- ✅ Upload sales reports to Google Drive
- ✅ Work both locally and on GitHub Actions

---

## 🔍 Troubleshooting

### "Google credentials not found"
- Make sure `secrets/google-service-account.json` exists
- Check the path in your `.env` file

### "Permission denied" or "403 Forbidden"
- Make sure you shared the Sheet/Folder with the service account email
- Check that you gave "Editor" access, not just "Viewer"

### "Spreadsheet not found"
- Double-check the Spreadsheet ID in your `.env` file
- Make sure the service account has access to the sheet

### "Folder not found"
- Double-check the Folder ID in your `.env` file
- Make sure the service account has access to the folder

---

## 📚 What Gets Uploaded Where

| File Type | Local | Google Sheets | Google Drive |
|-----------|-------|---------------|--------------|
| CSV data | ✅ `./out/leads_*.csv` | ✅ Appended to sheet | ✅ Full CSV file |
| Sales reports | ✅ `./out/sales_report_*.txt` | ❌ | ✅ Full TXT file |

**Google Sheets** = Structured data you can filter/sort/analyze
**Google Drive** = Full files you can download/share

---

## 🎯 Next Steps

Once setup is complete:
1. Test locally (Step 10)
2. Add GitHub Secrets (Step 11)
3. Enable weekly automation in the UI
4. Let it run automatically every Monday!

