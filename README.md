# 🗺️ Google Maps Lead Gen Pro

**Developed by [AIDevLab]**

This advanced Python script uses the SerpApi Google Maps engine to identify highly qualified leads for your agency. It specifically searches for businesses that **do not have a website listed**, making them perfect candidates for web development and SEO services.

---

## 🚀 Key Features
- **Smart Filtering**: Skips businesses that already have a website.
- **Deep Search**: Automatically paginates through local results (up to 100+ leads per search).
- **Pro Data**: Gathers Business Name, Physical Address, Phone Number, Rating, and Category.
- **Excel-Ready**: Generates formatted `.xlsx` files ready to import into your CRM.

## 🛠️ Setup Instructions

### 1. Configure Your API Key
The API key is stored securely in the `.env` file. We have already pre-set it with your SerpApi key.
- Open `.env` and ensure `SERP_API_KEY=your_key_here` is correct.

### 2. Basic Setup (PowerShell / Windows)
Open your terminal in this folder and run:

```powershell
# 1. Create a virtual environment
python -m venv venv

# 2. Activate the environment
.\venv\Scripts\Activate.ps1

# 3. Install required libraries
pip install -r requirements.txt
```

> [!TIP]
> If you get an error that scripts are disabled, run: `Set-ExecutionPolicy RemoteSigned -Scope CurrentUser`

### 3. Run the Scraper
Start finding leads immediately:
```powershell
python google_maps_scraper.py
```
1.  Enter the business type (e.g., `Dentist`)
2.  Enter the city (e.g., `New York`)
3.  The results will be saved in your folder as an Excel file.

---

## 📂 Requirements
- Python 3.10+
- SerpApi account (for the Google Maps access)
- Internet connection

## 📄 Output Fields
The generated Excel file includes:
1.  **Business Name**
2.  **Location (Address)**
3.  **Phone Number**
4.  **Rating & Review Count** (Target businesses with high ratings but no website!)
5.  **Category**
6.  **Status**: Marked as "Needs Website" for your outreach tracking.

---
**Enjoy the leads! 🚀**
*Visit [AIDevLab] for more elite automation tools.*
