"""
Implementation of DB interface for the ETL and QA pipeline.

Import as:
import sorrentum_sandbox.projects.Issue22_Team3_Implement_sandbox_for_Coinmarketcap.db.py as ssan_cmc_db
"""

from typing import Optional

import pandas as pd
import pymongo

import helpers.hdbg as hdbg
import sorrentum_sandbox.common.client as ssanclie
import sorrentum_sandbox.common.download as ssandown
import sorrentum_sandbox.common.save as ssansave

# #############################################################################
# MongoDataSaver
# #############################################################################

class MongoDataSaver(ssansave.DataSaver):
    """
    Store data to MongoDB.
    """

    def __init__(self, mongo_client: pymongo.MongoClient, db_name: str):
        self.mongo_client = mongo_client
        self.db_name = db_name

    def save(self, data: ssandown.RawData, collection_name: str) -> None:
        data = data.get_data()
        if isinstance(data, pd.DataFrame):
            data = data.to_dict("records")
        # else:
        #     hdbg.dassert_isinstance(data, list, "This data type is not supported")
        db = self.mongo_client
        db[self.db_name][collection_name].insert_one(data)
    
    # get data from mongoDB
    def get_data(self, collection_name: str) -> pd.DataFrame:
        db = self.mongo_client
        data = list(db[self.db_name][collection_name].find())
        df = pd.DataFrame(data)
        return df

# #############################################################################
# MongoClient
# #############################################################################


class MongoClient(ssanclie.DataClient):
    """
    Load data located in MongoDB into the memory.
    """

    def __init__(self, mongo_client: pymongo.MongoClient, db_name: str):
        """
        Build Reddit MongoDB client.

        :param mongo_client: MongoDB client
        :param db_name: name of the database to connect to
        """
        self.mongo_client = mongo_client
        self.db_name = db_name

    def load(
        self,
        dataset_signature: str,
        *,
        start_timestamp: Optional[pd.Timestamp] = None,
        end_timestamp: Optional[pd.Timestamp] = None,
    ) -> pd.DataFrame:
        """
        Load data from MongoDB collection directory for a specified time
        period.

        The method assumes data having a 'timestamp' column.

        :param dataset_signature: collection name where data come from
        :param start_timestamp: beginning of the time period to load. If `None`,
            start with the earliest available data
        :param end_timestamp: end of the time period to load. If `None`, download
            up to the latest available data
        :return: loaded data
        """
        # Access the data.
        db = self.mongo_client[self.db_name]
        # Build the filter.
        timestamp_filter: dict = {"created": {}}
        if start_timestamp or end_timestamp:
            if start_timestamp:
                timestamp_filter["created"] = {
                    "$gte": start_timestamp.to_pydatetime()
                }
            if end_timestamp:
                timestamp_filter["created"].update(
                    {"$lt": end_timestamp.to_pydatetime()}
                )
        else:
            timestamp_filter = {}
        data = list(db[dataset_signature].find(timestamp_filter))
        # Convert the data to a dataframe.
        df = pd.DataFrame(data)
        return df
