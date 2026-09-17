# ?? Shah Digital Store ? Certified Home Theaters & Audio

A complete, responsive, colorful, mobile-first web application and inventory system designed specifically for **Shah Digital Store** (Used and Refurbished Home Theater Systems & Professional Sound Engineering).

Built with **Python**, **Streamlit**, **SQLite**, and **HTML/CSS**.

---

## ?? Store Highlights & Features

- ?? **Store Name**: **Shah Digital Store**
- ?? **Contact / WhatsApp Number**: **`+91 96001 73174`**
- ?? **Vibrant Colorful UI**: High-impact modern gradients (deep indigo, electric cyan, vibrant emerald, amber accents), glowing badges, and smooth responsive cards.
- ?? **Home Page**: Interactive hero banner, audio category highlights, featured inventory spotlight, and quick consultation actions.
- ?? **Public Products Catalog**:
  - Live search across brands (Denon, Yamaha, Polk, Klipsch, Onkyo) and features (Dolby Atmos, 4K, 5.1).
  - Clean price tags in Indian Rupees (**?**).
  - Specifications accordion.
  - One-click **"?? WhatsApp Enquiry"** button linking directly to `+91 96001 73174` with pre-filled product details.
- ??? **Installation Support Section**:
  - Highlights professional on-site speaker mounting, concealed wiring, AVR Audyssey/YPAO acoustic room calibration, and projector alignment.
  - Interactive "Book Installation" form that registers customer requests in the SQLite database and sends an instant WhatsApp confirmation.
- ?? **About Page**: Store background, 10-point technical bench check, 7-Day Testing Warranty, and location details.
- ?? **Dedicated Customer Login Portal**:
  - Completely separate from admin controls so regular customers have their own dedicated space.
  - Allows customers to register with their phone number, log in, and track inquiries.
- ?? **Separate Admin Portal**:
  - Password-protected area for store managers (Default Password: **`admin123`**).
  - Real-time business metrics (Available Stock, Sold Items, Registered Customers, Pending Installations, Gross Inventory Value).
  - Full CRUD operations (Add, Edit, Mark as Sold, Delete, Image Upload).
  - **Automatic 2-Day Sold Product Retention Rule**: Sold items disappear immediately from public customers, are kept for 48 hours for bookkeeping, and then automatically purged from the database.

---

## ?? Project Structure

```text
home-theater-store/
??? app.py                     # Main Streamlit application
??? requirements.txt           # Python dependencies (streamlit, pillow)
??? README.md                  # Complete documentation and setup guide
??? database/
?   ??? __init__.py
?   ??? database.py            # SQLite schema, queries, CRUD, customer auth & 2-day cleanup
?   ??? home_theater.db        # SQLite database file
??? utils/
?   ??? __init__.py
?   ??? helpers.py             # WhatsApp URLs (+91 96001 73174), INR formatting, security hashing
??? images/
    ??? .gitkeep
    ??? default_theater.jpg    # Safe fallback image
    ??? denon_avr.jpg          # Starter demo image
    ??? yamaha_rx.jpg          # Starter demo image
    ??? polk_audio_5_1.jpg     # Starter demo image
    ??? klipsch_sub.jpg        # Starter demo image
    ??? onkyo_soundbar.jpg     # Starter demo image
```

---

## ?? How to Run Locally

1. Open your terminal in the `home-theater-store` directory:
   ```bash
   cd home-theater-store
   ```
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
3. Run the website:
   ```bash
   streamlit run app.py
   ```
   *(On Windows, you can also run: `python -m streamlit run app.py`)*

4. Open your browser at:
   `http://localhost:8501`

---

## ?? Logins

- **Customer Login**: Under the **?? Customer Login** tab, customers can create an account using their mobile number.
- **Admin Portal**: Under the **?? Admin Portal** tab. Default password is **`admin123`**.
