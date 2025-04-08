# Telegram Threat Intelligence Data Collector 📡

A Python-based system for collecting, analyzing, and storing cyber threat intelligence data from Telegram channels.

The tool searches Telegram posts using custom hashtags, filters out spam or scam messages, stores data in MongoDB, and exports raw JSON data for offline analysis.

---

## Features

- 🔍 Hashtag-based search (using external `hashtags.txt` file)
- 🧩 Discover related Telegram channels
- 🛡️ Scam/spam keyword filtering-
- 🗂️ Raw JSON export (`output.json`)
- ✅ Duplicate message filtering
- ⚙️ Easy setup and configuration

---

## Project Structure

```
telegram-threat-intel/
├── telegram_data_collector.py     # Main Python script
├── hashtags.txt                   # List of hashtags to monitor
├── output.json                    # Raw JSON export of collected messages
├── requirements.txt               # Python dependencies
└── README.md                      # Project documentation
```

---

## Requirements

- Python 3.8+
- Telegram API credentials (API ID and API Hash)
- Python libraries:
  - `telethon`
  - `pymongo`

### Install dependencies:

```bash
pip install -r requirements.txt
```

---

## Setup

1. **Clone the repository**

```bash
git clone https://github.com/your-username/telegram-threat-intel.git
cd telegram-threat-intel
```

2. **Get your Telegram API credentials**
   - Visit [my.telegram.org](https://my.telegram.org) to get API ID and API Hash.

3. **Create `hashtags.txt`**
   - Add hashtags to track (one per line, without `#`).

Example:
```
CyberThreat
MalwareAlert
APTGroup
RussiaUkraine
```
4. **Run the script**

```bash
python telegram_data_collector.py
```

---

## Output

- 🗃️ **Raw JSON Export:** `output.json` containing all collected data

---

## Roadmap

- [ ] Add NLP-based hashtag validation
- [ ] Reputation-based channel scoring
- [ ] Scheduled scraping (cronjob support)
- [ ] Docker containerization
- [ ] Integration with external threat intelligence feeds

---

## Troubleshooting

- **API errors:** Check API credentials and ensure they are correct. 
- **Empty results:** Confirm hashtags are active, and Telegram account is verified.

---

## Contributing

Contributions are welcome!  
Feel free to fork the repository and submit pull requests.

---

## License

This project is licensed under the MIT License.

---

## Author

**Dhanush S.**  
Cybersecurity Analyst | Threat Intelligence Enthusiast

[LinkedIn](https://www.linkedin.com/in/dhanush-s-396a70168/) • [GitHub](https://github.com/dhanushfdh)

---

