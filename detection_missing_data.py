
"""
Technical test - Affluences
by Réda MAIZATE (28/05/2021)
"""

# Importation des librairies
import pandas as pd

# Création de la classe
class DetectMissingData():
    """
    Detect the missing data on sensors and logs data.
    """
    def __init__(self,
                 sensor_data="/data/sensor_data.csv",
                 timetables="/data/timetables.csv",
                 analyze_date='2021-05-06 15:00:00',
                 last_record_column_name="last_record_datetime",
                 opening_column_name="opening_datetime",
                 closing_column_name="closing_datetime"
                 ):
        """
        Constructor of the class.
        """
        self.sensor_data = sensor_data
        self.timetables = timetables
        self.analyze_date = analyze_date
        self.last_record_column_name = last_record_column_name
        self.opening_column_name = opening_column_name
        self.closing_column_name = closing_column_name

    def detect(self):
        """
        Apply all the functions to detect the missing data.

        Arguments:
        None

        Returns:
        None
        """
        sensor_df, tt_df = self.import_data()
        merged_df = self.merge_data(sensor_df, tt_df)
        converted_df = self.convert_to_datetime(merged_df)
        diff_df = self.inactivity_by_hours(converted_df)
        alerts_df = self.apply_filter(diff_df)
        d.printAlerts(alerts_df)

    def import_data(self):
        """
        Import the dataset containing the sensor and logs informations.

        Arguments:
        sensor_data -- path of the CSV file containing the sensor data.
        timetables -- path of the CSV file containing the logs data.

        Returns:
        sensor_data -- DataFrame containing the sensor data.
        timetables -- DataFrame containing the logs data.
        """
        try:
            return pd.read_csv(self.sensor_data), pd.read_csv(self.timetables)
        except FileNotFoundError:
            print("File(s) not found!")
            raise
        except ValueError:
            print("Type of path not supported!")
            raise

    def merge_data(self, sensor_df, tt_df):
        """
        Merge the two datasets on the column Site_id.

        Arguments:
        sensor_df -- DataFrame containing the sensor data.
        tt_df -- DataFrame containing the logs data.

        Returns:
        merged_df -- DataFrame containing all the data.
        """
        sensor_df_ = sensor_df.set_index("site_id")
        tt_df_ = tt_df.set_index("site_id")
        return tt_df_.merge(sensor_df_, left_index=True, right_index=True)


    def convert_to_datetime(self, df):
        """
        Convert the last_records, opening hours and closing hours to datetime.

        Arguments:
        df -- DataFrame containing all the data.
        last_record_column_name -- Name of the last_records column.
        opening_column_name -- Name of the opening hours column.
        closing_column_name -- Name of the closing hours column.

        Returns:
        df -- DataFrame containing the conversion to datetime.
        """
        df[self.last_record_column_name] = pd.to_datetime(df[self.last_record_column_name])
        df[self.opening_column_name] = pd.to_datetime(df[self.opening_column_name], errors="coerce")
        df[self.closing_column_name] = pd.to_datetime(df[self.closing_column_name], errors="coerce")
        return df

    def inactivity_by_hours(self, df):
        """
        Create two temporary columns to facilitate the compution of inactivity by hours.

        Arguments:
        last_record_column_name -- Name of the last_records column.

        Returns:
        df -- DataFrame containing the columns Datetime_now and Diff.
        """
        df["datetime_now"] = pd.to_datetime(self.analyze_date)
        df["diff"] = (df["datetime_now"] - df[self.last_record_column_name]) / pd.Timedelta(hours=1)
        return df

    def apply_filter(self, df):
        """
        Filter the dataset by taking the rows that are between the opening hour and the closing hour,
        keep only the rows who have more than 2 hours of inactivity,
        then, categorize the rows according to alert's levels
        and finally, return only the columns needed.

        Alert's levels:
        - level 3, if the inactivity is superior than 48 hours.
        - level 2, if the inactivity is superior than 24 hours.
        - level 1, if the inactivity is superior than 2 hours.

        Arguments:
        df -- DataFrame containing the columns Datetime_now and Diff.

        Returns:
        alerts_df -- DataFrame containing only the colums needed.
        """
        opened = df[((df[self.opening_column_name] <= df["datetime_now"]) & (df[self.closing_column_name] >= df["datetime_now"]))]
        alert = opened[opened["diff"] > 2].copy()
        alert["level"] = alert["diff"].apply( (lambda x: 3 if x > 48 else (2 if x > 24 else 1)) )
        return alert[["sensor_identifier", "sensor_name", "datetime_now", self.last_record_column_name, "level"]]

    def printAlerts(self, df):
        """
        Display all the alerts.

        Arguments:
        df -- DataFrame containing all the alerts.

        Returns:
        None
        """
        df.apply((lambda r: print(f"Sensor {r['sensor_name']} with identifier {r['sensor_identifier']} triggers an alert at {r['datetime_now']} with level {r['level']} with last data recorded at {r['last_record_datetime']}\n")), axis=1)

if __name__ == "__main__":
    d = DetectMissingData("data/data.csv", "data/timetables.csv")
    d.detect()
