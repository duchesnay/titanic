import os

import click
import pandas as pd
from sklearn.model_selection import train_test_split

from ramp_utils.datasets import fetch_from_osf
from ramp_utils.datasets import OSFRemoteMetaData

PATH_DATA = os.path.join(
    os.path.dirname(os.path.abspath(__file__)), "data"
)
OSF_ARCHIVE = [
    OSFRemoteMetaData(
        filename="test.csv",
        id="2jd4a",
        revision=1,
    ),
    OSFRemoteMetaData(
        filename="train.csv",
        id="6a2qt",
        revision=1,
    ),
]

@click.command()
@click.option(
    "--token",
    help="The OSF token to be able to fetch data from the private project"
)
def prepare_data(token):
    fetch_from_osf(path_data=PATH_DATA, metadata=OSF_ARCHIVE, token=token)

    # 1- load the data which are already split into train and test sets for
    # the private set
    df_train = pd.read_csv(os.path.join(PATH_DATA, 'train.csv'))
    df_test = pd.read_csv(os.path.join(PATH_DATA, 'test.csv'))
    # 2- the private train set is also the public set which we need to split
    # into a train and test set.
    random_state = 57
    df_public_train, df_public_test = train_test_split(
        df_train, test_size=0.2, random_state=random_state
    )

    # 3- save the public data in a corresponding folder
    public_dir = os.path.join(PATH_DATA, "public")
    if not os.path.exists(public_dir):
        os.makedirs(public_dir)
    df_public_train.to_csv(
        os.path.join(public_dir, "train.csv"),
        index=False,
    )
    df_public_test.to_csv(
        os.path.join(public_dir, "test.csv"),
        index=False,
    )


if __name__ == "__main__":
    prepare_data()
