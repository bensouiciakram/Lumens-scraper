# Lumens Scraper

This is a Scrapy-based Python project that scrapes various fields from the [Lumens](https://www.lumens.com) website.

## Features

The project extracts the following fields from the Lumens website:

- Name
- SKU
- GTIN
- Color
- Finish
- Price
- Product Description
- Technical Description
- Display Dimensions
- Length
- Width
- Height
- Depth
- Diameter
- Weight
- Arm Height
- Seat Height
- Table Clearance Height
- Images
- Swatch Images
- PDFs
- Installations
- Designer
- Collection
- Category
- Available Now
- Made In
- Voltage
- Bulb Type
- Bulb Text
- Canopy Dimensions
- UL Listed
- Certification
- Warranty Care
- Position
- Notes
- URL

## Getting Started

1. Clone this repository: `git clone https://github.com/bensouiciakram/Lumens-scraper.git`
2. Navigate to the project directory: `cd lumens-scraper`
3. Install the required dependencies: `pip install scrapy`
4. Configure the scraping settings in `settings.py` (e.g., user agents, request delays).
5. Run the scraper: `scrapy crawl infos`

## Usage

- Customize the spider (`infos.py`) to adapt to any changes in the website structure.
- Data is saved to CSV format by default. Modify the pipeline to use other storage options if needed.

## License

This project is licensed under the [MIT License](LICENSE).
