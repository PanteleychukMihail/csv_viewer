## CSV_VIEWER

#### csv_viewer is a service for reading csv_files and adding information to db.

## Project requires

- [Python 3.11](https://www.python.org/downloads/)
- [MongoDB]

## Installation

1. Clone the project
    ```bash
    https://github.com/PanteleychukMihail/csv_viewer.git
    ```

2. In the terminal choose the root directory of the project
 

3. Create and activate a virtual environment
   
    ```
    python -m venv myenv
    venv\Scripts\activate
    ```   
   
4. To install the required dependencies, run the following command:
    ```
   pip install -r requirements.txt   
   ```
5. Create and fill out the .env file according to the example, adding your values ​​for the variables 



## Running
#### Without Docker
```bash
python manage.py runserver      
```

## Tests

```bash
python3 -m pytest
```

## Screenshots 
1. ![Index](https://github.com/PanteleychukMihail/csv_viewer/blob/master/screenshots/Screenshot%20index.png)
2. ![Wrong file's type](https://github.com/PanteleychukMihail/csv_viewer/blob/master/screenshots/Screenshot%20wrong%20type.png)
3. ![File upload](https://github.com/PanteleychukMihail/csv_viewer/blob/master/screenshots/Screenshot%20file%20in%20db.png)
4. ![Working on/off columns](https://github.com/PanteleychukMihail/csv_viewer/blob/master/screenshots/Screenshot%20working%20filters.png)
5. ![Working filters](https://github.com/PanteleychukMihail/csv_viewer/blob/master/screenshots/Screenshot%20working%20many%20filters.png)
6. ![Collection list](https://github.com/PanteleychukMihail/csv_viewer/blob/master/screenshots/Screenshot%20collections%20list.png)
   
