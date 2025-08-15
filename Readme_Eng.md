# RevoText

**Revolutionizing Real Estate Descriptions with AI**

RevoText is an AI-powered textual assistant tailored for real estate advertisers. It transforms rough text drafts into polished, clear, and engaging property descriptions—effortlessly and quickly.

## What It Does

- **Automatic Grammar & Style Correction**: Enhances text quality with linguistic refinement.
- **Tone Customization**: Allows selecting between friendly, professional, or exclusive tones (work in progress).
- **Highlighting & Readability Enhancements**: Organizes content with better structure and clarity.
- **SEO-Friendly Output**: Generates copy that performs well in online searches.

## Table of Contents

- [Installation](#installation)  
- [Usage](#usage)  
- [Examples](#examples)  
- [Development & Contribution](#development--contribution)  
- [Contact](#contact)

---

## Installation

1. Clone the repo:
   ```bash
   git clone https://github.com/sipocz/RevoText.git
   cd RevoText
   ```
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

---

## Usage

RevoText offers a simple interactive interface via Streamlit:

```bash
streamlit run streamlit_app.py
```

Then, open the provided local URL (typically `http://localhost:8501`) to interact with the UI. You can input draft descriptions and receive refined text outputs.

---

## Examples

**Input**  
```
3-room flat downtown. needs renovation, close to metro, good price.
```

**Output**  
```
Discover a charming 3-room apartment in the heart of downtown. Although it may require some renovation, its unbeatable location near the metro and excellent value make it a truly enticing opportunity.
```

---

## Development & Contribution

Feel free to enhance or contribute to the project! Some possible directions:

- Finalize the **tone choice** feature (friendly, professional, exclusive).
- Improve the **UI/UX**, e.g., live editing, preview panels, or batch processing.
- Add support for additional languages or custom template styles.
- Integrate with other platforms (e.g., publishing APIs or CRM systems).

### File Overview

- `streamlit_app.py` — Launches the main application.
- `requirements.txt` — Lists Python dependencies.
- `Zenga_download.ipynb`, `chat_GPT_API.ipynb` — Jupyter notebooks for data handling or experimentation.
- `.devcontainer`, Presentation files, and `images` folder — For development environment setup and visuals.

---

## Contact

Created by **Sipőcz László**  
Email: sipoczlaszlo@gmail.com  
LinkedIn: [Profile](https://linkedin.com/in/36204746473/)

---

## License

*(Add license information here, if available.)*

---

### Summary

RevoText is a polished, storyboard-ready AI assistant that elevates real estate advertising by automating text refinement and ensuring readability and SEO readiness—all within an easy-to-use Streamlit app. Its modular structure enables straightforward extension and improvement.
