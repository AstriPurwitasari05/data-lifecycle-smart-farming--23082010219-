# 🌱 Data Lifecycle Smart Farming

![Python](https://img.shields.io/badge/Python-3.12-blue?logo=python)
![Streamlit](https://img.shields.io/badge/Streamlit-Dashboard-red?logo=streamlit)
![Kaggle](https://img.shields.io/badge/Dataset-Kaggle-20BEFF?logo=kaggle)
![Status](https://img.shields.io/badge/Status-Active-brightgreen)

> **Dashboard interaktif monitoring kelembaban tanah** berbasis IoT sensor  
> menggunakan dataset Plant Vase dari Kaggle.

---

## 🔗 Live Dashboard

[![Open Dashboard](https://img.shields.io/badge/🌐_Buka_Dashboard-Streamlit-FF4B4B?style=for-the-badge)](https://overably-twee-shara.ngrok-free.dev)

**👉 Link:** `https://overably-twee-shara.ngrok-free.dev`

---

## 📋 Deskripsi Proyek

Proyek ini merupakan implementasi **Data Lifecycle Management** pada bidang Smart Farming.  
Data kelembaban tanah dikumpulkan dari sensor IoT pada 3 pot tanaman (plant vase),  
kemudian diproses melalui pipeline: **Ingestion → Cleaning → Analysis → Visualization**.

| Info | Detail |
|------|--------|
| 📦 Dataset | [Soil Moisture Dataset - Kaggle](https://www.kaggle.com/datasets/amirmohammdjalili/soil-moisture-dataset) |
| 🗓️ Periode Data | 06 Maret 2020 — 29 Maret 2020 |
| 📊 Total Data | 18,349 baris (setelah cleaning) |
| 🌿 Sumber Sensor | plant_vase1, plant_vase1_2, plant_vase2 |
| 🛠️ Tools | Python, Streamlit, Plotly, Pandas, Seaborn |

---

## 📁 Struktur File
```
data-lifecycle-smart-farming/
├── 📄 README.md
├── 📓 Data_Lifecycle_Smart_Farming.ipynb
├── 📊 plant_vase1.CSV
├── 📊 plant_vase1(2).CSV
├── 📊 plant_vase2.CSV
├── ✅ cleaned_data.csv
├── 🖥️ streamlit_app.py
├── 🖼️ correlation_heatmap.png
├── 📈 timeseries_plant_vase1.png
├── 📈 timeseries_plant_vase1_2.png
└── 📈 timeseries_plant_vase2.png
```

---

## 🔄 Pipeline Data Lifecycle
```
[1. Ingestion]     → Download dataset dari Kaggle API
        ↓
[2. EDA]           → df.describe(), df.isnull(), df.info()
        ↓
[3. Cleaning]      → Handle missing values, outlier IQR, format datetime
        ↓
[4. Analysis]      → Correlation heatmap, time series trend
        ↓
[5. Visualization] → Dashboard Streamlit interaktif
        ↓
[6. Governance]    → Data Quality Score, README, GitHub repo
```

---

## 📊 Fitur Dashboard

| Visualisasi | Deskripsi |
|-------------|-----------|
| 🔵 **Gauge Meter** | Rata-rata kelembaban tiap sensor secara real-time |
| 🚨 **Alert System** | Warna merah jika moisture < threshold (default: 0.30) |
| 📈 **Time Series** | Tren kelembaban dengan opsi agregasi Raw/Jam/Hari |
| 🌡️ **Heatmap** | Korelasi antar sensor moisture per sumber data |
| ⚙️ **Filter** | Filter sumber data & slider threshold interaktif |

---

## 📈 Data Quality Score

| Metrik | plant_vase1 | plant_vase1_2 | plant_vase2 |
|--------|-------------|---------------|-------------|
| ✅ Accuracy | 100% | 100% | 100% |
| ✅ Completeness | 100% | 100% | 100% |
| 📅 Timeliness | Data dalam 30 hari terakhir | | |

---

## 🛠️ Teknologi

![Python](https://img.shields.io/badge/Python-FFD43B?style=flat&logo=python&logoColor=blue)
![Pandas](https://img.shields.io/badge/Pandas-2C2D72?style=flat&logo=pandas&logoColor=white)
![Streamlit](https://img.shields.io/badge/Streamlit-FF4B4B?style=flat&logo=streamlit&logoColor=white)
![Plotly](https://img.shields.io/badge/Plotly-239120?style=flat&logo=plotly&logoColor=white)
![Google Colab](https://img.shields.io/badge/Google_Colab-F9AB00?style=flat&logo=googlecolab&logoColor=white)
![GitHub](https://img.shields.io/badge/GitHub-100000?style=flat&logo=github&logoColor=white)

---

## 👩‍💻 Author

| Info | Detail |
|------|--------|
| 👤 Nama | Astri Purwitasari |
| 🎓 NIM | 23082010219 |
| 📧 Email | astrisari51@gmail.com |
| 📚 Mata Kuliah | Big Data — Data Lifecycle Management |

---

<div align="center">
  <i>🌱 Built with ❤️ for Smart Farming | 2024</i>
</div>
