# 📊 Google Sheets & Drive Integration

## Overview

The SEO Lead Finder now automatically uploads results to Google Sheets and Google Drive:

- **CSV Data** → Google Sheets (structured, filterable data)
- **Sales Reports** → Google Drive (full intelligence reports)
- **CSV Files** → Google Drive (backup copies)

---

## What Gets Uploaded

### Google Sheets
- **What**: Lead data in structured table format
- **File**: All leads with scores, contact info, SEO metrics
- **Benefits**: 
  - Filter and sort leads
  - Share with team
  - Analyze trends over time
  - Export to other tools

### Google Drive
- **What**: Full files (CSV + TXT reports)
- **Files**:
  - `leads_YYYYMMDD_HHMMSS.csv` - All lead data
  - `sales_report_Location_YYYY-MM-DD.txt` - Full intelligence reports
- **Benefits**:
  - Download complete files
  - Share specific reports
  - Archive historical data
  - Access from anywhere

---

## Setup Required

See **[GOOGLE_SETUP_GUIDE.md](GOOGLE_SETUP_GUIDE.md)** for complete step-by-step instructions.

**Quick summary:**
1. Create Google Cloud project
2. Enable Google Sheets API and Google Drive API
3. Create service account and download JSON key
4. Create Google Sheet and share with service account
5. Create Google Drive folder and share with service account
6. Update `.env` file with IDs
7. Add secrets to GitHub for automation

---

## Configuration

Add these to your `.env` file:

```bash
# Google Sheets & Drive (OPTIONAL - CSV output always works)
GOOGLE_SHEETS_SERVICE_ACCOUNT_JSON_PATH=./secrets/google-service-account.json
GOOGLE_SHEETS_SPREADSHEET_ID=your-spreadsheet-id-here
GOOGLE_SHEETS_WORKSHEET_NAME=Leads
GOOGLE_DRIVE_FOLDER_ID=your-folder-id-here
```

---

## How It Works

### Local Runs
When you run `python main.py --once --geo "Houston, TX"`:

1. ✅ Saves CSV locally: `./out/leads_*.csv`
2. ✅ Uploads CSV to Google Drive
3. ✅ Appends data to Google Sheets
4. ✅ Saves sales report locally: `./out/sales_report_*.txt`
5. ✅ Uploads sales report to Google Drive

### Automated Runs (GitHub Actions)
When weekly automation runs:

1. ✅ Runs the pipeline on GitHub servers
2. ✅ Uploads results to Google Sheets & Drive
3. ✅ Sends Slack notification (if configured)
4. ✅ Results accessible immediately in Google

---

## Error Handling

The integration is **optional** and **fail-safe**:

- ❌ If credentials not found → Saves locally only
- ❌ If upload fails → Saves locally only
- ❌ If API error → Saves locally only
- ✅ Local CSV files **always** work

You'll see warnings like:
```
⚠️  Google credentials not found: ...
   File saved locally only: ./out/leads_20251014_123456.csv
```

This is normal if you haven't set up Google integration yet!

---

## Testing

Test the integration locally:

```bash
python3 main.py --once --geo "Houston, TX"
```

**Expected output:**
```
✅ CSV saved: ./out/leads_20251014_123456.csv
✅ Uploaded to Google Drive: leads_20251014_123456.csv
   URL: https://drive.google.com/file/d/...
✅ Google Sheets updated: 100 rows appended
✅ Sales report saved: ./out/sales_report_Houston_TX_2025-10-14.txt
✅ Uploaded to Google Drive: sales_report_Houston_TX_2025-10-14.txt
   URL: https://drive.google.com/file/d/...
```

**Then check:**
1. Google Sheet - should have new rows
2. Google Drive folder - should have CSV + TXT files

---

## Files Modified

### New Files
- `modules/drive_io.py` - Google Drive upload functionality
- `GOOGLE_SETUP_GUIDE.md` - Complete setup instructions
- `GOOGLE_DRIVE_INTEGRATION.md` - This file

### Updated Files
- `modules/report_generator.py` - Now uploads reports to Drive
- `modules/sheets_io.py` - Now uploads CSVs to Drive
- `.env` - Added `GOOGLE_DRIVE_FOLDER_ID`
- `.github/workflows/weekly.yml` - Added Drive secrets
- `README.md` - Added Google integration docs

---

## Troubleshooting

### "Google credentials not found"
- Check that `secrets/google-service-account.json` exists
- Verify path in `.env` file

### "Permission denied" or "403 Forbidden"
- Make sure you shared Sheet/Folder with service account email
- Check that you gave "Editor" access

### "Spreadsheet not found"
- Double-check Spreadsheet ID in `.env`
- Verify service account has access

### "Folder not found"
- Double-check Folder ID in `.env`
- Verify service account has access

### Files upload but don't appear
- Check the correct folder in Google Drive
- Refresh the page
- Check service account has "Editor" not "Viewer" access

---

## Security Notes

**⚠️ Important:**
- The JSON key file is like a password - keep it secure!
- Never commit `secrets/google-service-account.json` to git
- It's already in `.gitignore` - don't remove it
- For GitHub Actions, use GitHub Secrets (encrypted)

**What's safe to commit:**
- `.env` with placeholder values (no actual IDs)
- Documentation files
- Code that uses the credentials

**What's NOT safe to commit:**
- `secrets/google-service-account.json`
- `.env` with real IDs (already in `.gitignore`)
- Any file containing the service account email/key

---

## Next Steps

1. **Set up Google integration** - Follow [GOOGLE_SETUP_GUIDE.md](GOOGLE_SETUP_GUIDE.md)
2. **Test locally** - Run a search and verify uploads work
3. **Add GitHub Secrets** - For weekly automation
4. **Enable automation** - Use the Streamlit UI to configure weekly runs

---

## Benefits

### Before (Local Only)
- ❌ Results only on your computer
- ❌ Hard to share with team
- ❌ Manual file management
- ❌ No remote access

### After (Google Integration)
- ✅ Access from anywhere
- ✅ Easy team collaboration
- ✅ Automatic organization
- ✅ Cloud backup
- ✅ Filter/sort in Sheets
- ✅ Download full reports from Drive

