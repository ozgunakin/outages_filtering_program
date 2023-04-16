# Outages Filtering Program
A small program that filters outages of indicated sites and posts an enhanced versions of these outages with device info to the system.

## File Strucuture:
- main.py  
Python program to filter outages and post enhanced results.

- conf.py  
Where api urls and site_id and date filter are indicated. 
When the API endpoint or site_id is changed, the new endpoint and site_id should be changed in conf.py file. Date filter can also be changed in conf.py.

- requirements.txt  
Indicates required libraries for this program.

## How to run ?
After installing libraries indicated in requirements.txt, you can run the program using the command below.

```python
python3 main.py
```
