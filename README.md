# Website Monitoring Console App
Console python app to report various stats on websites input by the user.

### Dependencies
- Python 3.7 (Anaconda distribution)
- [Freezegun](https://github.com/spulec/freezegun)
- [Httpx](https://www.python-httpx.org/)
- [Pytest](http://pytest.com/) *for testing*
- *Full requirements in requirements.txt


## Installation


1. **git clone https://github.com/DanielJohnHarty/website_monitoring_app.git**

2.  **pip install -r requirements.txt**

3.  **python web_monitoring_app.py**


## Usage

Follow the onscreen prompts to select websites to monitor and how often to ping them.

Reports appear every 10 seconds showing the dashboards from the last 10 minutes and every minute showing the data from the past hour.

These defaults can be changed in the python web_monitoring_app.py file (*the schedules dict*)